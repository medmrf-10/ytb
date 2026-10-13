#!/usr/bin/env python3
"""build_index.py - Generate and verify catalog.json, _index.json files, and COVERAGE.md.

Stdlib only, deterministic output.
Supports:
  python3 tools/build_index.py          # Builds all indexes and writes to disk
  python3 tools/build_index.py --check  # Verifies in-memory indexes match disk (exit code 0/1)
"""

import hashlib
import json
import os
import re
import sys

W = "/root/workspace"
YTB = os.path.join(W, "ytb")
META_DIR = os.path.join(YTB, "_meta")
SOURCE_HEADS_FILE = os.path.join(META_DIR, "source_heads.json")
EXCLUDED_FILE = os.path.join(META_DIR, "excluded.json")
REGISTRY_FILE = os.path.join(W, "ytb-build", "registry.json")
HAWSHAT_SHEIKHS_FILE = os.path.join(W, "hawshat", "playlists", "data", "sheikhs.json")

AR_DIAC = re.compile(r"[ً-ْٰ]")


def norm(s):
    """Normalize Arabic string for alias matching."""
    s = AR_DIAC.sub("", s or "")
    s = re.sub(r"[^\w\s]", "", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    s = s.replace("ؤ", "و").replace("ئ", "ي").replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"\s+", " ", s).strip().lower()


def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def dump_json_str(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def write_atomic_str(content, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, target_path)


def build_indexes():
    """Build all index data structures in memory."""
    # Load source heads
    with open(SOURCE_HEADS_FILE, "r", encoding="utf-8") as f:
        sh_raw = json.load(f)
    source_heads = {
        k: v.get("head", "")[:7] if k in ("des", "irth") else v.get("head", "")[:8]
        for k, v in sh_raw.items()
    }

    # Load 29 sheikhs canonical registry
    with open(HAWSHAT_SHEIKHS_FILE, "r", encoding="utf-8") as f:
        haw_sheikhs = json.load(f).get("sheikhs", [])
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        reg_data = json.load(f)
        reg_sheikhs = {s["slug"]: s for s in reg_data.get("sheikhs", [])}

    # Discover sheikh folders on disk
    disk_sheikhs = set()
    for entry in os.listdir(YTB):
        p = os.path.join(YTB, entry)
        if os.path.isdir(p) and entry not in (".git", "_inbox", "_meta", "tools"):
            disk_sheikhs.add(entry)

    # Generated files map: path -> string content
    outputs = {}

    total_catalog_lessons = 0
    total_catalog_series = 0
    total_catalog_chars = 0
    sheikhs_with_content_count = 0

    catalog_sheikhs = []
    aliases_index = {}

    # Sheikh coverage rows for COVERAGE.md
    coverage_sheikhs_data = []

    # Map all 29 sheikhs in catalog
    all_slugs_ordered = [s["slug"] for s in haw_sheikhs]
    if "unattributed" in disk_sheikhs and "unattributed" not in all_slugs_ordered:
        all_slugs_ordered.append("unattributed")

    for slug in all_slugs_ordered:
        h_sh = next((s for s in haw_sheikhs if s["slug"] == slug), None)
        r_sh = reg_sheikhs.get(slug, {})

        if slug == "unattributed":
            name = "غير منسوب"
            name_display = "دروس غير منسوبة"
            aliases = ["غير منسوب", "unattributed"]
        elif h_sh:
            name = h_sh.get("name") or r_sh.get("name_ar") or slug
            name_display = h_sh.get("name_display") or r_sh.get("name_ar") or slug
            aliases = h_sh.get("aliases") or r_sh.get("aliases") or []
        else:
            name = r_sh.get("name_ar", slug)
            name_display = r_sh.get("name_ar", slug)
            aliases = r_sh.get("aliases", [])

        # Add aliases to index
        for alias in aliases + [name, name_display, slug]:
            norm_a = norm(alias)
            if norm_a and norm_a not in aliases_index:
                aliases_index[norm_a] = slug

        sh_dir = os.path.join(YTB, slug)
        has_content = os.path.isdir(sh_dir) and slug in disk_sheikhs

        if not has_content:
            catalog_sheikhs.append({
                "slug": slug,
                "name": name,
                "name_display": name_display,
                "aliases": aliases,
                "series": 0,
                "lessons": 0,
                "chars": 0,
                "path": None
            })
            coverage_sheikhs_data.append({
                "slug": slug,
                "name_display": name_display,
                "series_count": 0,
                "lessons_count": 0,
                "has_content": False,
                "series_list": []
            })
            continue

        sheikhs_with_content_count += 1

        # Check _sheikh.json
        sheikh_json_path = os.path.join(sh_dir, "_sheikh.json")
        if not os.path.isfile(sheikh_json_path):
            raise RuntimeError(f"Missing _sheikh.json in {sh_dir}")

        # Scan series folders
        series_keys = []
        for sk in sorted(os.listdir(sh_dir)):
            sk_dir = os.path.join(sh_dir, sk)
            if os.path.isdir(sk_dir) and not sk.startswith((".", "_")):
                series_keys.append(sk)
            elif os.path.isdir(sk_dir) and sk == "_unsorted":
                series_keys.append(sk)

        sh_totals_lessons = 0
        sh_totals_chars = 0
        sh_totals_with_vid = 0
        sh_totals_unsorted = 0

        sheikh_series_index_list = []
        sheikh_coverage_series = []

        for sk in series_keys:
            sk_dir = os.path.join(sh_dir, sk)
            series_json_path = os.path.join(sk_dir, "_series.json")
            if not os.path.isfile(series_json_path):
                raise RuntimeError(f"Missing _series.json in {sk_dir}")

            with open(series_json_path, "r", encoding="utf-8") as sjf:
                s_meta = json.load(sjf)

            # Lessons in series
            files = sorted(os.listdir(sk_dir))
            txt_files = [f for f in files if f.endswith(".txt")]
            meta_files = [f for f in files if f.endswith(".meta.json")]

            # Validate 1-to-1 match between txt and meta
            txt_stems = set(f[:-4] for f in txt_files)
            meta_stems = set(f[:-10] for f in meta_files)

            if txt_stems != meta_stems:
                diff = txt_stems.symmetric_difference(meta_stems)
                raise RuntimeError(f"Mismatch between .txt and .meta.json in {sk_dir}: {diff}")

            lessons_list = []
            for stem in sorted(txt_stems):
                meta_p = os.path.join(sk_dir, stem + ".meta.json")
                txt_p = os.path.join(sk_dir, stem + ".txt")

                with open(meta_p, "r", encoding="utf-8") as mf:
                    m = json.load(mf)

                # Validate sha256
                cur_sha = get_file_sha256(txt_p)
                if cur_sha != m["sha256"]:
                    raise RuntimeError(f"SHA mismatch in {txt_p}: on-disk {cur_sha} != meta {m['sha256']}")

                lessons_list.append({
                    "n": m.get("n"),
                    "vid": m.get("vid"),
                    "title": m.get("title"),
                    "file": stem + ".txt",
                    "chars": m.get("chars", 0),
                    "sha256": m.get("sha256"),
                    "quality": m.get("quality", "ok"),
                    "variants": len(m.get("variants", []))
                })

            lessons_list.sort(key=lambda x: (x["n"] if x["n"] is not None else 999999, x["file"]))

            transcribed = len(lessons_list)
            declared_total = s_meta.get("declared_total")
            coverage = round(transcribed / declared_total, 4) if (declared_total and declared_total > 0) else None

            # Series _index.json
            series_index_obj = {
                "v": 1,
                "row_id": s_meta.get("row_id"),
                "sheikh": slug,
                "title": s_meta.get("title"),
                "playlists": s_meta.get("playlists", []),
                "declared_total": declared_total,
                "transcribed": transcribed,
                "coverage": coverage,
                "lessons": lessons_list
            }
            outputs[os.path.join(sk_dir, "_index.json")] = dump_json_str(series_index_obj)

            # For sheikh _index.json
            sheikh_series_index_list.append({
                "key": sk,
                "row_id": s_meta.get("row_id"),
                "title": s_meta.get("title"),
                "dir": f"{sk}/",
                "transcribed": transcribed,
                "declared_total": declared_total,
                "coverage": coverage
            })

            s_chars = sum(l["chars"] for l in lessons_list)
            s_vids = sum(1 for l in lessons_list if l["vid"])

            sh_totals_lessons += transcribed
            sh_totals_chars += s_chars
            sh_totals_with_vid += s_vids
            if sk == "_unsorted":
                sh_totals_unsorted += transcribed

            sheikh_coverage_series.append({
                "key": sk,
                "title": s_meta.get("title"),
                "transcribed": transcribed,
                "declared_total": declared_total,
                "coverage_pct": f"{round(coverage * 100, 1)}%" if coverage is not None else "غير محدد"
            })

        # Sheikh _index.json
        sheikh_index_obj = {
            "v": 1,
            "slug": slug,
            "name": name,
            "name_display": name_display,
            "aliases": aliases,
            "totals": {
                "series": len(series_keys),
                "lessons": sh_totals_lessons,
                "chars": sh_totals_chars,
                "with_vid": sh_totals_with_vid,
                "unsorted": sh_totals_unsorted
            },
            "series": sorted(sheikh_series_index_list, key=lambda x: x["key"])
        }
        outputs[os.path.join(sh_dir, "_index.json")] = dump_json_str(sheikh_index_obj)

        total_catalog_lessons += sh_totals_lessons
        total_catalog_series += len(series_keys)
        total_catalog_chars += sh_totals_chars

        catalog_sheikhs.append({
            "slug": slug,
            "name": name,
            "name_display": name_display,
            "aliases": aliases,
            "series": len(series_keys),
            "lessons": sh_totals_lessons,
            "chars": sh_totals_chars,
            "path": f"{slug}/"
        })

        coverage_sheikhs_data.append({
            "slug": slug,
            "name_display": name_display,
            "series_count": len(series_keys),
            "lessons_count": sh_totals_lessons,
            "has_content": True,
            "series_list": sheikh_coverage_series
        })

    # Catalog.json
    catalog_obj = {
        "v": 1,
        "source_heads": source_heads,
        "totals": {
            "sheikhs_with_content": sheikhs_with_content_count,
            "series": total_catalog_series,
            "lessons": total_catalog_lessons,
            "chars": total_catalog_chars
        },
        "sheikhs": sorted(catalog_sheikhs, key=lambda x: (-x["lessons"], x["slug"])),
        "aliases_index": dict(sorted(aliases_index.items()))
    }
    outputs[os.path.join(YTB, "catalog.json")] = dump_json_str(catalog_obj)

    # COVERAGE.md
    with open(EXCLUDED_FILE, "r", encoding="utf-8") as exf:
        excluded_data = json.load(exf)

    cov_lines = [
        "# تقرير تغطية المحتوى والتفريغات — مستودع `ytb`",
        "",
        "> تقرير شامل مُولَّد آلياً يعرض محتوى كافة المشايخ الـ 29 والسلاسل المفرغة ونسبة التغطية مقارنة بالإجمالي المعلن.",
        "",
        "## 1. جدول المشايخ الإجمالي",
        "",
        "| # | الشيخ | Slug | السلاسل المفرغة | المحاضرات المفرغة | حالة المحتوى |",
        "|---|---|---|---:|---:|---|"
    ]

    for idx, cs in enumerate(sorted(coverage_sheikhs_data, key=lambda x: (-x["lessons_count"], x["slug"])), 1):
        status = f"[`{cs['slug']}/`](./{cs['slug']}/)" if cs["has_content"] else "لا تفريغ حالياً (0)"
        cov_lines.append(f"| {idx} | {cs['name_display']} | `{cs['slug']}` | {cs['series_count']} | {cs['lessons_count']:,} | {status} |")

    cov_lines.extend([
        "",
        "---",
        "",
        "## 2. تفاصيل السلاسل لكل شيخ",
        ""
    ])

    for cs in sorted(coverage_sheikhs_data, key=lambda x: (-x["lessons_count"], x["slug"])):
        if not cs["has_content"]:
            continue
        cov_lines.extend([
            f"### {cs['name_display']} (`{cs['slug']}`)",
            f"- إجمالي المحاضرات: **{cs['lessons_count']:,}** درس في **{cs['series_count']}** سلسلة.",
            "",
            "| السلسلة | مجلد الحفظ | المفرغ | المعلن | نسبة التغطية |",
            "|---|---|---:|---:|---:|"
        ])
        for s in cs["series_list"]:
            dec_val = str(s["declared_total"]) if s["declared_total"] is not None else "غير محدد"
            cov_lines.append(f"| {s['title']} | [`{s['key']}/`](./{cs['slug']}/{s['key']}/) | {s['transcribed']} | {dec_val} | {s['coverage_pct']} |")
        cov_lines.append("")

    cov_lines.extend([
        "---",
        "",
        "## 3. المجموعات المستبعدة من v1",
        "",
        "| المسار الأصلي | سبب الاستبعاد | عدد الملفات |",
        "|---|---|---:|"
    ])

    for ex in excluded_data:
        cov_lines.append(f"| `{ex['path_prefix']}` | {ex['reason']} | {ex['file_count']} |")

    cov_lines.append("")
    outputs[os.path.join(YTB, "COVERAGE.md")] = "\n".join(cov_lines)

    return outputs


def main():
    check_mode = "--check" in sys.argv

    if check_mode:
        print("Checking index files integrity...")
        try:
            expected_outputs = build_indexes()
        except Exception as e:
            print(f"FAILED to build indexes in memory: {e}", file=sys.stderr)
            sys.exit(1)

        mismatches = []
        for path, exp_content in expected_outputs.items():
            if not os.path.isfile(path):
                mismatches.append(f"Missing file on disk: {path}")
                continue
            with open(path, "r", encoding="utf-8") as f:
                cur_content = f.read()
            if cur_content != exp_content:
                mismatches.append(f"Content mismatch in: {path} (disk len {len(cur_content)} != exp len {len(exp_content)})")

        if mismatches:
            print(f"FAILED: {len(mismatches)} index mismatches detected:", file=sys.stderr)
            for m in mismatches[:10]:
                print(f"  {m}", file=sys.stderr)
            sys.exit(1)
        else:
            print("OK: All index files on disk match generated state perfectly.")
            sys.exit(0)

    print("=" * 60)
    print("ytb index building: Starting P6 (build_index.py)")
    print("=" * 60)

    outputs = build_indexes()

    for path, content in outputs.items():
        write_atomic_str(content, path)

    print(f"Successfully generated and wrote {len(outputs)} index files:")
    print(f"  - catalog.json")
    print(f"  - COVERAGE.md")
    print(f"  - per-sheikh _index.json files")
    print(f"  - per-series _index.json files")


if __name__ == "__main__":
    main()
