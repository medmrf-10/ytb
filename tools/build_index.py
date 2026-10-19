#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_index.py v2 — توليد والتحقق الحتمي من catalog.json وCOVERAGE.md وREADME.md وملفات _index.json في مستودع ytb.

يدعم هيكلة cheikh القياسية (_meta.json + .txt + .align.json + .meta.json):
  python3 tools/build_index.py          # يبني جميع الفهارس ويكتبها ذرياً على القرص
  python3 tools/build_index.py --check  # يتحقق من تطابق الفهارس على القرص وخلو المستودع من المخلفات (exit 0/1)
"""
import hashlib
import json
import os
import re
import sys

YTB = "/root/workspace/ytb"
CURATED_MAP_JSON = "/root/workspace/cheikh-exports/curated_full_mapping.json"
REGISTRY_FILE = "/root/workspace/ytb-build/registry.json"

SHEIKH_NAMES_AR = {
    "said-bouti": "محمد سعيد رمضان البوطي",
    "sharawi": "محمد متولي الشعراوي",
    "adham-alasimi": "أدهم العاسمي",
    "habib-ali-aljifri": "الحبيب علي الجفري",
    "ahmed-alsayed": "أحمد السيد",
    "fadhel-samarrai": "فاضل السامرائي",
    "habib-omar-ibn-hafiz": "الحبيب عمر بن حفيظ",
    "dhaker-alhashimi": "ذاكر الهاشمي",
    "bardouni-husaymi": "محمد البردوني الحسيمي",
    "ali-gomaa": "علي جمعة",
    "daddo": "محمد الحسن الددو",
    "ali-mahmoud-alomari": "علي محمود العمري",
    "mouloud-sariri": "مولود السريري",
    "ali-hani-aqrabawi": "علي هاني العقرباوي",
    "ayman-abdelrahim": "أيمن عبد الرحيم",
    "maath-hawa": "معاذ سعيد حوى",
    "said-kamali": "سعيد الكملي",
    "fadhel-sulaiman": "فاضل سليمان",
    "saif-alasri": "سيف العصري",
    "muhammad-abdelwahid-hanbali": "محمد عبد الواحد الحنبلي",
    "aboubakr-almashhour": "أبو بكر المشهور",
    "ahmed-abdelmonem": "أحمد عبد المنعم",
    "hatem-alaouni": "حاتم العوني",
    "bensaib": "بن صايب",
    "unattributed": "دروس غير منسوبة",
}


def dump_json_str(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_atomic_str(content, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp_path, target_path)


def build_indexes():
    curated_lookup = {}
    if os.path.isfile(CURATED_MAP_JSON):
        try:
            cdata = json.load(open(CURATED_MAP_JSON, encoding="utf-8"))
            for s in cdata.get("series", []):
                curated_lookup[(s["sheikh_slug"], s["s_code"])] = s
        except Exception:
            pass

    outputs = {}
    catalog_sheikhs = []
    coverage_sheikhs = []

    total_series = 0
    total_lessons = 0
    total_aligned = 0
    total_chars = 0

    sheikh_slugs = sorted(
        d for d in os.listdir(YTB)
        if os.path.isdir(os.path.join(YTB, d)) and d not in (".git", "_meta", "tools") and not d.startswith(".")
    )

    for slug in sheikh_slugs:
        sh_dir = os.path.join(YTB, slug)
        sh_json_p = os.path.join(sh_dir, "_sheikh.json")
        sh_info = {}
        if os.path.isfile(sh_json_p):
            try:
                sh_info = json.load(open(sh_json_p, encoding="utf-8"))
            except Exception:
                sh_info = {}
        name_display = SHEIKH_NAMES_AR.get(slug) or sh_info.get("name_display") or sh_info.get("name") or slug
        aliases = sh_info.get("aliases") or [name_display, slug]

        series_keys = sorted(
            sk for sk in os.listdir(sh_dir)
            if os.path.isdir(os.path.join(sh_dir, sk)) and not sk.startswith(".") and sk not in ("_variants", "_raw_preamble_backup", "_truncated_legacy_backup")
        )

        sh_lessons = 0
        sh_aligned = 0
        sh_chars = 0
        sh_series_list = []

        for sk in series_keys:
            sk_dir = os.path.join(sh_dir, sk)
            meta_p = os.path.join(sk_dir, "_meta.json")
            ser_p = os.path.join(sk_dir, "_series.json")
            c_ser = curated_lookup.get((slug, sk), {})

            s_meta = {}
            if os.path.isfile(meta_p):
                try:
                    s_meta = json.load(open(meta_p, encoding="utf-8"))
                except Exception:
                    s_meta = {}
            elif os.path.isfile(ser_p):
                try:
                    s_meta = json.load(open(ser_p, encoding="utf-8"))
                except Exception:
                    s_meta = {}

            title = c_ser.get("title") or s_meta.get("series") or s_meta.get("title") or sk
            series_id = c_ser.get("id") or s_meta.get("series_id") or f"{slug}__{sk}"
            category = c_ser.get("category") or s_meta.get("category") or ""
            videos = c_ser.get("lessons") or s_meta.get("videos") or []
            declared_total = len(videos) if videos else (s_meta.get("declared_total") or 0)

            files = sorted(os.listdir(sk_dir))
            txt_files = [f for f in files if f.endswith(".txt") and not f.startswith("_")]
            align_set = {f[:-11] for f in files if f.endswith(".align.json") and os.path.getsize(os.path.join(sk_dir, f)) > 200}

            lessons_list = []
            s_chars = 0
            for tf in txt_files:
                stem = tf[:-4]
                tp = os.path.join(sk_dir, tf)
                mp = os.path.join(sk_dir, stem + ".meta.json")
                ap = os.path.join(sk_dir, stem + ".align.json")
                chars = os.path.getsize(tp)
                try:
                    chars = len(open(tp, encoding="utf-8", errors="replace").read())
                except Exception:
                    pass
                s_chars += chars

                parts = stem.split("_", 1)
                n_val = int(parts[0]) if parts[0].isdigit() else None
                vid_val = parts[1] if len(parts) == 2 else None
                l_title = ""
                if os.path.isfile(mp):
                    try:
                        md = json.load(open(mp, encoding="utf-8"))
                        l_title = md.get("title") or ""
                        if n_val is None:
                            n_val = md.get("n")
                        if not vid_val:
                            vid_val = md.get("vid")
                    except Exception:
                        pass

                has_align = stem in align_set
                align_cov = None
                if has_align:
                    try:
                        ad = json.load(open(ap, encoding="utf-8"))
                        align_cov = ad.get("spoken_align_coverage")
                    except Exception:
                        pass

                lessons_list.append({
                    "n": n_val,
                    "vid": vid_val,
                    "title": l_title,
                    "file": tf,
                    "chars": chars,
                    "aligned": has_align,
                    "align_coverage": align_cov,
                })

            transcribed = len(lessons_list)
            aligned_cnt = sum(1 for l in lessons_list if l["aligned"])
            if declared_total < transcribed:
                declared_total = transcribed
            cov = round(transcribed / declared_total, 4) if declared_total > 0 else 1.0
            al_cov = round(aligned_cnt / transcribed, 4) if transcribed > 0 else 0.0

            series_index_obj = {
                "v": 2,
                "series_id": series_id,
                "sheikh": slug,
                "sheikh_name": name_display,
                "key": sk,
                "title": title,
                "category": category,
                "declared_total": declared_total,
                "transcribed": transcribed,
                "aligned": aligned_cnt,
                "coverage": cov,
                "aligned_ratio": al_cov,
                "lessons": lessons_list,
            }
            outputs[os.path.join(sk_dir, "_index.json")] = dump_json_str(series_index_obj)

            sh_lessons += transcribed
            sh_aligned += aligned_cnt
            sh_chars += s_chars
            sh_series_list.append({
                "key": sk,
                "series_id": series_id,
                "title": title,
                "category": category,
                "dir": f"{sk}/",
                "declared_total": declared_total,
                "transcribed": transcribed,
                "aligned": aligned_cnt,
                "coverage": cov,
                "coverage_pct": f"{round(cov * 100, 1)}%",
                "aligned_pct": f"{round(al_cov * 100, 1)}%",
            })

        sheikh_obj = {
            "v": 2,
            "slug": slug,
            "name": name_display,
            "name_display": name_display,
            "aliases": aliases,
        }
        outputs[sh_json_p] = dump_json_str(sheikh_obj)

        sheikh_index_obj = {
            "v": 2,
            "slug": slug,
            "name": name_display,
            "name_display": name_display,
            "totals": {
                "series": len(sh_series_list),
                "lessons": sh_lessons,
                "aligned": sh_aligned,
                "chars": sh_chars,
            },
            "series": sh_series_list,
        }
        outputs[os.path.join(sh_dir, "_index.json")] = dump_json_str(sheikh_index_obj)

        total_series += len(sh_series_list)
        total_lessons += sh_lessons
        total_aligned += sh_aligned
        total_chars += sh_chars

        catalog_sheikhs.append({
            "slug": slug,
            "name": name_display,
            "series": len(sh_series_list),
            "lessons": sh_lessons,
            "aligned": sh_aligned,
            "chars": sh_chars,
            "path": f"{slug}/",
        })
        coverage_sheikhs.append({
            "slug": slug,
            "name_display": name_display,
            "series_count": len(sh_series_list),
            "lessons_count": sh_lessons,
            "aligned_count": sh_aligned,
            "chars_count": sh_chars,
            "series_list": sh_series_list,
        })

    catalog_sheikhs.sort(key=lambda x: (-x["lessons"], x["slug"]))
    coverage_sheikhs.sort(key=lambda x: (-x["lessons_count"], x["slug"]))

    catalog_obj = {
        "v": 2,
        "totals": {
            "sheikhs": len(catalog_sheikhs),
            "series": total_series,
            "lessons": total_lessons,
            "aligned": total_aligned,
            "chars": total_chars,
        },
        "sheikhs": catalog_sheikhs,
    }
    outputs[os.path.join(YTB, "catalog.json")] = dump_json_str(catalog_obj)

    # COVERAGE.md
    cov_lines = [
        "# تقرير تغطية التفريغ والمحاذاة — مستودع `ytb`",
        "",
        f"- **إجمالي المشايخ:** {len(catalog_sheikhs)} شيخاً",
        f"- **إجمالي السلاسل المفرغة:** {total_series:,} سلسلة",
        f"- **إجمالي الدروس المفرغة نصياً (`.txt`):** {total_lessons:,} درساً ({total_chars:,} حرفاً)",
        f"- **إجمالي الدروس المحاذاة صوتياً (`.align.json`):** {total_aligned:,} درساً",
        "",
        "## 1. جدول المشايخ الإجمالي",
        "",
        "| # | الشيخ | المعرّف (`Slug`) | السلاسل | الدروس المفرغة | الدروس المحاذاة | المجلد |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    for idx, cs in enumerate(coverage_sheikhs, 1):
        cov_lines.append(
            f"| {idx} | {cs['name_display']} | `{cs['slug']}` | {cs['series_count']} | {cs['lessons_count']:,} | {cs['aligned_count']:,} | [`{cs['slug']}/`](./{cs['slug']}/) |"
        )

    cov_lines.extend(["", "---", "", "## 2. تفصيل السلاسل لكل شيخ", ""])
    for cs in coverage_sheikhs:
        cov_lines.extend([
            f"### {cs['name_display']} (`{cs['slug']}`)",
            f"- إجمالي الدروس المفرغة: **{cs['lessons_count']:,}** درساً (المحاذاة: **{cs['aligned_count']:,}**) في **{cs['series_count']}** سلسلة.",
            "",
            "| الكود | عنوان السلسلة | المفرغ | المعلن | نسبة التفريغ | المحاذاة |",
            "|---|---|---:|---:|---:|---:|",
        ])
        for s in cs["series_list"]:
            cov_lines.append(
                f"| [`{s['key']}`](./{cs['slug']}/{s['key']}/) | {s['title']} | {s['transcribed']} | {s['declared_total']} | {s['coverage_pct']} | {s['aligned']} ({s['aligned_pct']}) |"
            )
        cov_lines.append("")

    outputs[os.path.join(YTB, "COVERAGE.md")] = "\n".join(cov_lines) + "\n"

    # README.md
    readme_lines = [
        "# ytb — المستودع الموحّد لتفريغات ومحاذاة الدروس العلمية",
        "",
        "المستودع الرسمي الموحّد لجميع النصوص المفرّغة (`.txt`) وملفات المحاذاة الصوتية بالكلمة والثانية (`.align.json`) والبيانات الوصفية (`.meta.json`) وفق هيكلة `cheikh` القياسية.",
        "",
        "---",
        "",
        "## 1. الإحصاءات العامة",
        "",
        f"- **المشايخ ذوو المحتوى الفعلي:** {len(catalog_sheikhs)} شيخاً",
        f"- **السلاسل المفرّغة:** {total_series:,} سلسلة",
        f"- **الدروس المفرّغة نصياً (`.txt`):** {total_lessons:,} درساً",
        f"- **الدروس المحاذاة صوتياً (`.align.json`):** {total_aligned:,} درساً",
        f"- **إجمالي الحجم النصي:** {total_chars:,} حرفاً",
        "",
        "---",
        "",
        "## 2. جدول المشايخ",
        "",
        "| # | الشيخ | المعرّف (`Slug`) | السلاسل | الدروس المفرغة (`.txt`) | الدروس المحاذاة (`.align.json`) | المجلد |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    for idx, cs in enumerate(coverage_sheikhs, 1):
        readme_lines.append(
            f"| {idx} | {cs['name_display']} | `{cs['slug']}` | {cs['series_count']} | {cs['lessons_count']:,} | {cs['aligned_count']:,} | [`{cs['slug']}/`](./{cs['slug']}/) |"
        )
    readme_lines.extend([
        "",
        "> التفاصيل الكاملة لكل سلسلة داخل كل شيخ موجودة في [`COVERAGE.md`](./COVERAGE.md) وفي [`catalog.json`](./catalog.json).",
        "",
        "---",
        "",
        "## 3. هيكل المستودع القياسي",
        "",
        "```text",
        "ytb/",
        "  README.md                       # الواجهة الرئيسية والإحصاءات العامة",
        "  COVERAGE.md                     # تقرير التغطية التفصيلي لكل شيخ وسلسلة",
        "  catalog.json                    # الفهرس المركزي المهيكل",
        "  <sheikh-slug>/                  # مجلد الشيخ + _sheikh.json + _index.json",
        "    <s_code>/                     # مجلد السلسلة القياسي (مثل s001) + _meta.json + _index.json",
        "      <NNN>_<vid>.txt             # النص العربي المطهّر للمحاضرة",
        "      <NNN>_<vid>.align.json      # المحاذاة الصوتية الدقيقة (كلمة بكلمة بالثانية)",
        "      <NNN>_<vid>.meta.json       # البيانات الوصفية للمحاضرة",
        "  tools/                          # أدوات الفهرسة والتحقق (build_index.py)",
        "  _meta/                          # سجلات الجرد والتحقق المرجعية",
        "```",
        "",
    ])
    outputs[os.path.join(YTB, "README.md")] = "\n".join(readme_lines)
    return outputs


def main():
    check_mode = "--check" in sys.argv
    expected = build_indexes()
    if check_mode:
        mismatches = []
        for path, exp_content in expected.items():
            if not os.path.isfile(path):
                mismatches.append(f"Missing index file: {path}")
                continue
            cur = open(path, encoding="utf-8").read()
            if cur != exp_content:
                mismatches.append(f"Mismatch in: {path}")
        # Also verify zero backup directories, zero orphan .align.json, and coupled word-count equality (len(x) == len(txt.split()))
        for root, dirs, files in os.walk(YTB):
            if ".git" in dirs:
                dirs.remove(".git")
            for bad in ("_raw_preamble_backup", "_truncated_legacy_backup", "_archive_legacy", "_fix", "_inbox"):
                if bad in dirs:
                    mismatches.append(f"Forbidden backup/legacy dir inside repo: {os.path.join(root, bad)}")
            for fn in files:
                if fn.endswith(".align.json"):
                    stem = fn[:-len(".align.json")]
                    tf = os.path.join(root, stem + ".txt")
                    af = os.path.join(root, fn)
                    if not os.path.isfile(tf):
                        mismatches.append(f"Orphan .align.json without .txt: {af}")
                    else:
                        try:
                            ad = json.load(open(af, encoding="utf-8"))
                            aw = len(ad.get("x", ad.get("words", [])))
                            tw = len(open(tf, encoding="utf-8", errors="replace").read().split())
                            if aw != tw:
                                mismatches.append(f"Coupled word-count mismatch in {af}: txt={tw} vs align={aw}")
                        except Exception as e:
                            mismatches.append(f"Corrupt .align.json {af}: {e}")
        if mismatches:
            print(f"FAILED ({len(mismatches)} issues):", file=sys.stderr)
            for m in mismatches[:15]:
                print(" ", m, file=sys.stderr)
            sys.exit(1)
        print("OK: All index files and repository structure checks passed (0 errors).")
        sys.exit(0)

    for path, content in expected.items():
        write_atomic_str(content, path)
    cat = json.loads(expected[os.path.join(YTB, "catalog.json")])
    print(f"Generated {len(expected)} index files: {cat['totals']}")


if __name__ == "__main__":
    main()
