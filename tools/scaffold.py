#!/usr/bin/env python3
"""scaffold.py - Generate _sheikh.json, _series.json, and README.md files across ytb.

Uses canonical metadata from registry.json and hawshat/playlists/data/sheikhs.json.
Stdlib only, idempotent and deterministic.
"""

import json
import os
import sys

W = "/root/workspace"
YTB = os.path.join(W, "ytb")
REGISTRY_FILE = os.path.join(W, "ytb-build", "registry.json")
HAWSHAT_SHEIKHS_FILE = os.path.join(W, "hawshat", "playlists", "data", "sheikhs.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_atomic_json(obj, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp_path, target_path)


def write_atomic_text(text, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp_path, target_path)


def main():
    print("=" * 60)
    print("ytb metadata scaffolding: Starting P3 (scaffold.py)")
    print("=" * 60)

    reg = load_json(REGISTRY_FILE)
    haw = load_json(HAWSHAT_SHEIKHS_FILE)

    # Sheikh lookup
    reg_sheikhs = {s["slug"]: s for s in reg.get("sheikhs", [])}
    haw_sheikhs = {s["slug"]: s for s in haw.get("sheikhs", [])}

    # Series lookup from registry
    by_slug = {}
    for s in reg.get("series", []):
        by_slug[s["slug"]] = s
        for h in s.get("hawshat_series_slugs", []):
            by_slug[h] = s
        for m in s.get("manifest_row_ids", []):
            by_slug[str(m)] = s
        for d in s.get("des_rows", []):
            by_slug[str(d)] = s

    # Discover sheikh folders
    sheikh_folders = []
    for entry in sorted(os.listdir(YTB)):
        p = os.path.join(YTB, entry)
        if os.path.isdir(p) and entry not in (".git", "_inbox", "_meta", "tools"):
            sheikh_folders.append(entry)

    print(f"Found {len(sheikh_folders)} sheikh folders in ytb tree.")

    sheikh_metas_written = 0
    series_metas_written = 0
    readmes_written = 0

    for sh in sheikh_folders:
        sh_dir = os.path.join(YTB, sh)
        r_sh = reg_sheikhs.get(sh, {})
        h_sh = haw_sheikhs.get(sh, {})

        if sh == "unattributed":
            sh_name = "غير منسوب"
            sh_display = "دروس غير منسوبة"
            sh_aliases = ["غير منسوب", "unattributed"]
        else:
            sh_name = h_sh.get("name") or r_sh.get("name_ar") or sh
            sh_display = h_sh.get("name_display") or r_sh.get("name_ar") or sh
            sh_aliases = h_sh.get("aliases") or r_sh.get("aliases") or []

        # Find series under this sheikh
        series_keys = []
        for sk in sorted(os.listdir(sh_dir)):
            sk_dir = os.path.join(sh_dir, sk)
            if os.path.isdir(sk_dir) and not sk.startswith((".", "_")):
                series_keys.append(sk)
            elif os.path.isdir(sk_dir) and sk == "_unsorted":
                series_keys.append(sk)

        total_sh_lessons = 0
        total_sh_chars = 0
        total_sh_with_vid = 0
        total_sh_unsorted = 0

        sheikh_series_cards = []

        for sk in series_keys:
            sk_dir = os.path.join(sh_dir, sk)

            # Collect lesson files and metas
            meta_files = [f for f in sorted(os.listdir(sk_dir)) if f.endswith(".meta.json")]
            txt_files = [f for f in sorted(os.listdir(sk_dir)) if f.endswith(".txt")]

            # Load lesson metas to collect stats
            lessons_info = []
            for mf in meta_files:
                with open(os.path.join(sk_dir, mf), "r", encoding="utf-8") as mff:
                    m_data = json.load(mff)
                    lessons_info.append(m_data)

            # Sort lessons by n
            lessons_info.sort(key=lambda x: (x.get("n") if x.get("n") is not None else 999999, x.get("lid", "")))

            # Match registry series
            s_obj = by_slug.get(sk) or by_slug.get(f"{sh}--{sk}")
            if not s_obj and sk.isdigit():
                s_obj = by_slug.get(sk)

            if s_obj:
                title = s_obj.get("name_ar", sk)
                playlists = [s_obj["youtube_playlist"]] if s_obj.get("youtube_playlist") else []
                declared_total = s_obj.get("declared_total")
                manifest_row_ids = s_obj.get("manifest_row_ids", [])
                hawshat_slugs = s_obj.get("hawshat_series_slugs", [])
                des_rows = s_obj.get("des_rows", [])
                irth_ids = s_obj.get("irth_lesson_ids", [])
                notes = s_obj.get("notes")
            else:
                if sh == "unattributed" or sk == "_unsorted":
                    title = "تفريغات متفرقة غير منسوبة" if sh == "unattributed" else f"دروس غير مفروزة ({sh_display})"
                else:
                    title = sk
                playlists = []
                declared_total = len(lessons_info)
                manifest_row_ids = []
                hawshat_slugs = []
                des_rows = []
                irth_ids = []
                notes = "Auto-generated"

            # Canonical row_id
            if lessons_info and lessons_info[0].get("row_id"):
                canonical_row_id = lessons_info[0]["row_id"]
            else:
                canonical_row_id = f"{sh}--{sk}"

            # Compute stats
            transcribed_count = len(lessons_info)
            s_chars = sum(l.get("chars", 0) for l in lessons_info)
            s_vids = sum(1 for l in lessons_info if l.get("vid"))

            total_sh_lessons += transcribed_count
            total_sh_chars += s_chars
            total_sh_with_vid += s_vids
            if sk == "_unsorted":
                total_sh_unsorted += transcribed_count

            # _series.json
            series_json = {
                "v": 1,
                "row_id": canonical_row_id,
                "key": sk,
                "sheikh": sh,
                "title": title,
                "playlists": playlists,
                "declared_total": declared_total,
                "row_keys": [sk] + [f"{sh}--{sk}"] + [str(r) for r in manifest_row_ids + des_rows],
                "provenance": {
                    "manifest_row_ids": manifest_row_ids,
                    "hawshat_series_slugs": hawshat_slugs,
                    "des_rows": des_rows,
                    "irth_lesson_ids": irth_ids,
                    "notes": notes
                },
                "lessons_count": transcribed_count
            }
            write_atomic_json(series_json, os.path.join(sk_dir, "_series.json"))
            series_metas_written += 1

            # Series README.md
            cov_str = f"{round((transcribed_count / declared_total) * 100, 1)}%" if (declared_total and declared_total > 0) else "غير محدد"
            dec_str = str(declared_total) if declared_total is not None else "غير محدد"

            series_readme_lines = [
                f"# {title}",
                "",
                f"- **الشيخ**: {sh_display}",
                f"- **معرّف السلسلة**: `{canonical_row_id}`",
                f"- **عدد الدروس المفرغة**: {transcribed_count}",
                f"- **الإجمالي المعلن**: {dec_str}",
                f"- **نسبة الإنجاز والتغطية**: {cov_str}",
                "",
                "## اصطلاح تسمية الملفات",
                "- `<NNN>_<vid>.txt`: النص الكامل للتفريغ الفائز (بايتات المصدر الأصلية دون تعديل).",
                "- `<NNN>_<vid>.meta.json`: بطاقة الهوية وحالة الجودة ومطابقة المصادر المتعددة.",
                "- `_variants/`: حفظ النصوص الخاسرة عند وجود تعارض نصي حقيقي.",
                "",
                "## قائمة المحاضرات المفرغة",
                "| # | عنوان الدرس | معرّف يوتيوب | الحجم (حرف) | الجودة |",
                "|---|---|---|---|---|"
            ]

            for l in lessons_info:
                n_val = f"{l.get('n'):03d}" if l.get("n") is not None else "—"
                l_title = l.get("title") or "—"
                l_vid = f"`{l['vid']}`" if l.get("vid") else "—"
                l_chars = f"{l.get('chars', 0):,}"
                l_qual = l.get("quality", "ok")
                series_readme_lines.append(f"| {n_val} | {l_title} | {l_vid} | {l_chars} | `{l_qual}` |")

            series_readme_lines.append("")
            write_atomic_text("\n".join(series_readme_lines), os.path.join(sk_dir, "README.md"))
            readmes_written += 1

            sheikh_series_cards.append({
                "key": sk,
                "row_id": canonical_row_id,
                "title": title,
                "transcribed": transcribed_count,
                "declared": dec_str,
                "coverage": cov_str
            })

        # Sheikh _sheikh.json
        sheikh_json = {
            "v": 1,
            "slug": sh,
            "name": sh_name,
            "name_display": sh_display,
            "aliases": sh_aliases,
            "series_count": len(series_keys),
            "lessons_count": total_sh_lessons,
            "counts": {
                "series": len(series_keys),
                "lessons": total_sh_lessons,
                "chars": total_sh_chars,
                "with_vid": total_sh_with_vid,
                "unsorted": total_sh_unsorted
            }
        }
        write_atomic_json(sheikh_json, os.path.join(sh_dir, "_sheikh.json"))
        sheikh_metas_written += 1

        # Sheikh README.md
        aliases_str = "، ".join(sh_aliases) if sh_aliases else "لا يوجد"
        sh_readme_lines = [
            f"# {sh_display} (`{sh}`)",
            "",
            f"- **الاسم الكامل**: {sh_name}",
            f"- **الألقاب والأسماء البديلة**: {aliases_str}",
            f"- **إجمالي السلاسل المفرغة**: {len(series_keys)}",
            f"- **إجمالي المحاضرات المفرغة**: {total_sh_lessons:,} درساً",
            f"- **إجمالي الحروف**: {total_sh_chars:,} حرفاً",
            "",
            "## السلاسل المتاحة",
            "| السلسلة | مجلد الحفظ | الدروس المفرغة | المعلن | التغطية |",
            "|---|---|---|---|---|"
        ]

        for sc in sheikh_series_cards:
            sh_readme_lines.append(f"| {sc['title']} | [`{sc['key']}/`](./{sc['key']}/) | {sc['transcribed']} | {sc['declared']} | {sc['coverage']} |")

        sh_readme_lines.extend([
            "",
            "## محتويات المجلد",
            "- `_sheikh.json`: البطاقة التعريفية للشيخ وألقابه وإحصاءات المحتوى.",
            "- `_index.json`: فهرس شامل لكافة السلاسل والدروس المولدة تلقائياً بواسطة أدوات الفهرسة.",
            "- `<series-dir>/`: مجلدات السلاسل وتحوي ملفات التفريغ النصية وبياناتها الوصفية.",
            ""
        ])
        write_atomic_text("\n".join(sh_readme_lines), os.path.join(sh_dir, "README.md"))
        readmes_written += 1

    print(f"Scaffolding completed:")
    print(f"  _sheikh.json written: {sheikh_metas_written}")
    print(f"  _series.json written: {series_metas_written}")
    print(f"  README.md written: {readmes_written}")


if __name__ == "__main__":
    main()
