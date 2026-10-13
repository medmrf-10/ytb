#!/usr/bin/env python3
"""ask.py - Query transcribed content for a given sheikh using only tree indexes.

Usage:
  python3 tools/ask.py البوطي
  python3 tools/ask.py said-bouti
  python3 tools/ask.py "أحمد السيد" --json
"""

import json
import os
import re
import sys

W = "/root/workspace"
YTB = os.path.join(W, "ytb")
CATALOG_FILE = os.path.join(YTB, "catalog.json")

AR_DIAC = re.compile(r"[ً-ْٰ]")


def norm(s):
    """Normalize Arabic string for robust alias matching."""
    s = AR_DIAC.sub("", s or "")
    s = re.sub(r"[^\w\s]", "", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    s = s.replace("ؤ", "و").replace("ئ", "ي").replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"\s+", " ", s).strip().lower()


def load_catalog():
    if not os.path.isfile(CATALOG_FILE):
        print(f"Error: catalog.json not found at {CATALOG_FILE}. Run tools/build_index.py first.", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_sheikh_slug(query, catalog):
    norm_q = norm(query)

    # 1. Exact alias / norm match from catalog index
    aliases_idx = catalog.get("aliases_index", {})
    if norm_q in aliases_idx:
        return aliases_idx[norm_q]

    # 2. Check exact slug
    for s in catalog.get("sheikhs", []):
        if s["slug"].lower() == query.strip().lower():
            return s["slug"]

    # 3. Partial / substring match on normalized names or aliases
    for s in catalog.get("sheikhs", []):
        if norm_q in norm(s["name"]) or norm_q in norm(s["name_display"]) or norm_q in norm(s["slug"]):
            return s["slug"]
        for a in s.get("aliases", []):
            if norm_q in norm(a):
                return s["slug"]

    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    json_mode = "--json" in sys.argv

    if not args:
        print("الاستخدام: python3 tools/ask.py <اسم_الشيخ_أو_المعرف> [--json]")
        print("مثال: python3 tools/ask.py البوطي")
        sys.exit(1)

    query = " ".join(args)
    catalog = load_catalog()

    slug = find_sheikh_slug(query, catalog)
    if not slug:
        if json_mode:
            print(json.dumps({"error": f"لم يتم العثور على الشيخ: {query}"}, ensure_ascii=False, indent=2))
        else:
            print(f"عذراً، لم يتم العثور على شيخ مطابق للبحث «{query}».")
            print("المشايخ المتاح لهم تفريغ في المستودع:")
            for s in catalog.get("sheikhs", []):
                if s["lessons"] > 0:
                    print(f"  - {s['name_display']} (`{s['slug']}`)")
        sys.exit(1)

    sheikh_meta = next((s for s in catalog["sheikhs"] if s["slug"] == slug), None)
    sheikh_index_path = os.path.join(YTB, slug, "_index.json")

    has_index = os.path.isfile(sheikh_index_path)
    sh_index = None
    if has_index:
        with open(sheikh_index_path, "r", encoding="utf-8") as sif:
            sh_index = json.load(sif)

    # Format source heads
    sh_heads = catalog.get("source_heads", {})
    heads_str = " · ".join(f"{repo}@{h}" for repo, h in sorted(sh_heads.items()))

    if json_mode:
        res = {
            "query": query,
            "slug": slug,
            "name": sheikh_meta["name"],
            "name_display": sheikh_meta["name_display"],
            "aliases": sheikh_meta.get("aliases", []),
            "has_content": has_index and sheikh_meta["lessons"] > 0,
            "series_count": sheikh_meta["series"],
            "lessons_count": sheikh_meta["lessons"],
            "source_heads": sh_heads,
            "series": sh_index.get("series", []) if sh_index else []
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Text mode output
    name_disp = sheikh_meta["name_display"]
    name_full = sheikh_meta["name"]
    aliases_str = "، ".join(sheikh_meta.get("aliases", [])) or "لا يوجد"

    if not has_index or sheikh_meta["lessons"] == 0:
        print("=" * 60)
        print(f"الشيخ: {name_full} (`{slug}`)")
        print(f"الاسم المعروض: {name_disp}")
        print(f"الألقاب: {aliases_str}")
        print("الحالة: مسجل في الدليل ولكن لا يتوفر له تفريغ حالياً في v1 (0 دروس).")
        print(f"رؤوس المصادر: {heads_str}")
        print("=" * 60)
        sys.exit(0)

    totals = sh_index.get("totals", {})
    chars = totals.get("chars", 0)
    with_vid = totals.get("with_vid", 0)

    print("=" * 70)
    print(f"الشيخ: {name_full} (`{slug}`)")
    print(f"الاسم المعروض: {name_disp}")
    print(f"الألقاب والأسماء البديلة: {aliases_str}")
    print(f"إجمالي السلاسل المفرغة: {sheikh_meta['series']} سلسلة")
    print(f"إجمالي الدروس المفرغة: {sheikh_meta['lessons']:,} درساً ({with_vid:,} برابط يوتيوب)")
    print(f"إجمالي الحجم النصي: {chars:,} حرفاً")
    print(f"آخر تحديث لرؤوس المصادر: {heads_str}")
    print("=" * 70)
    print("السلاسل المفرغة في مستودع ytb:")
    print(f"{'#':<3} | {'السلسلة':<40} | {'المفرغ':<7} | {'المعلن':<7} | {'نسبة التغطية':<12} | {'المجلد'}")
    print("-" * 85)

    for idx, s in enumerate(sh_index.get("series", []), 1):
        s_title = s.get("title", "")[:38]
        s_trans = s.get("transcribed", 0)
        dec = s.get("declared_total")
        s_dec = str(dec) if dec is not None else "غير محدد"
        cov = s.get("coverage")
        cov_pct = f"{round(cov * 100, 1)}%" if cov is not None else "غير محدد"
        s_dir = s.get("dir", "")
        print(f"{idx:<3} | {s_title:<40} | {s_trans:<7} | {s_dec:<7} | {cov_pct:<12} | {slug}/{s_dir}")

    print("=" * 70)


if __name__ == "__main__":
    main()
