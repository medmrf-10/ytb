#!/usr/bin/env python3
"""P1 — Comprehensive Inventory (tools/inventory.py).

Scans all five lecture stores plus special stores and artifacts:
- Generates ytb/_meta/inventory.jsonl (one record per text file)
- Generates ytb/_meta/INVENTORY.json (per-store summary, unique hashes, bytes, sheikh coverage)
- Generates ytb/_meta/row_map.json (merged row identity map)
- Generates ytb/_meta/sheikh_map.json (sheikh attribution map)
- Generates ytb/_meta/excluded.json (excluded corpora accounting)
"""

import collections
import hashlib
import json
import os
import sys
import time

# Add tools dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (
    W, HAW, DES, IRTH, YTB, META_DIR,
    STORE_DIRS, SPECIAL_STORES, EXCLUDED_DES_CORPORA,
    TR_EXCLUDE, TR_FOLD, GEN_REDIRECTS, CREATED_ROWS,
    norm, clean_title, dump_atomic, dump_jsonl_atomic, load_json,
    get_git_commit_timestamps, extract_header_and_body, vid_of,
    HDR_VID, PL_RE, NUM_RE, NAYT_RE
)


def build_row_map():
    """Build canonical row mapping by merging hawshat row_ids, muarchiv, redirects, and constants."""
    row_ids = load_json(os.path.join(HAW, "playlists", "data", "row_ids.json"))
    muarchiv = load_json(os.path.join(HAW, "playlists", "data", "muarchiv_slug_rowid.json"))
    redirects = load_json(os.path.join(HAW, "playlists", "data", "redirects.json"))

    row_map = {}
    # Flatten row_ids
    for sh, m in row_ids.items():
        for k, v in m.items():
            row_map[k] = v

    # Add muarchiv aliases
    for k, v in muarchiv.get("alias_keys", {}).items():
        row_map.setdefault(k, v)

    for k, v in muarchiv.get("slug_to_rowid", {}).items():
        row_map.setdefault("s:" + k, v)
        row_map.setdefault(k, v)

    # Merge redirects
    all_redirects = dict(redirects)
    all_redirects.update(GEN_REDIRECTS)

    # Add TR_FOLD
    for (sh, key), target_mut in TR_FOLD.items():
        all_redirects[f"t:{sh}-{key}"] = f"k:{target_mut}"

    # Add Created rows (11 mutalaa + durus 37)
    for row_num, canon_rid in CREATED_ROWS.items():
        row_map[f"k:{row_num}"] = canon_rid
        row_map[f"m:{row_num}"] = canon_rid
        row_map[row_num] = canon_rid

    # Resolve all destinations through redirects chain
    def resolve_canon(rid):
        seen = set()
        while rid in all_redirects and rid not in seen:
            seen.add(rid)
            rid = all_redirects[rid]
        return rid

    final_row_map = {}
    for k, v in row_map.items():
        resolved = resolve_canon(v)
        final_row_map[k] = resolved

    # Also map all direct redirect entries
    for k, v in all_redirects.items():
        final_row_map[k] = resolve_canon(v)

    return final_row_map


def build_sheikh_map():
    """Build sheikh lookup table: normalized arabic names + aliases + irth speakers -> canonical slug."""
    sheikhs_data = load_json(os.path.join(HAW, "playlists", "data", "sheikhs.json")).get("sheikhs") or []
    sheikh_map = {}

    # irth speakers
    irth_speakers = {
        "bouti": "said-bouti",
        "alamri": "ali-mahmoud-alomari",
        "alsayed": "ahmed-alsayed",
        "fadel": "fadhel-sulaiman",
        "alasri": "saif-alasri",
        "abdelwahid": "muhammad-abdelwahid-hanbali",
        "abdelmonem": "ahmed-abdelmonem",
        "aouni": "hatem-alaouni",
    }
    for spk, slug in irth_speakers.items():
        sheikh_map[spk] = slug

    for s in sheikhs_data:
        slug = s["slug"]
        sheikh_map[slug] = slug
        names = [s.get("name"), s.get("name_display")] + list(s.get("aliases") or [])
        for name in names:
            if name:
                n_raw = name.strip()
                n_norm = norm(n_raw)
                sheikh_map[n_raw] = slug
                sheikh_map[n_norm] = slug

    # Fixed canonical overrides from plan (Section 1.2)
    sheikh_map["البردوني"] = "bardouni-husaymi"
    sheikh_map[norm("البردوني")] = "bardouni-husaymi"
    sheikh_map["الحسيمي_تجربة"] = "bardouni-husaymi"
    sheikh_map[norm("الحسيمي_تجربة")] = "bardouni-husaymi"
    sheikh_map["محمد متولي الشعراوي"] = "sharawi"
    sheikh_map[norm("محمد متولي الشعراوي")] = "sharawi"
    sheikh_map["مكتبة المتون والشروح المفرغة"] = "maktaba"
    sheikh_map[norm("مكتبة المتون والشروح المفرغة")] = "maktaba"

    # Incorporate ytb-build/registry.json if present
    reg_path = os.path.join(W, "ytb-build", "registry.json")
    if os.path.exists(reg_path):
        reg = load_json(reg_path)
        for reg_s in reg.get("sheikhs") or []:
            r_slug = reg_s.get("slug")
            r_name = reg_s.get("name_ar")
            canon_slug = sheikh_map.get(norm(r_name)) if r_name else None
            if canon_slug and r_slug:
                sheikh_map[r_slug] = canon_slug
                for al in reg_s.get("aliases") or []:
                    if al:
                        sheikh_map[al.strip()] = canon_slug
                        sheikh_map[norm(al.strip())] = canon_slug

    return sheikh_map


def load_read_indexes():
    """Load hawshat/playlists/data/read/*.json files."""
    read_dir = os.path.join(HAW, "playlists", "data", "read")
    read_by_file = {}  # (row_id, filename) -> item
    read_by_base_file = {}  # (base, filename) -> item
    read_by_vid = {}  # vid -> item

    if os.path.isdir(read_dir):
        for f in os.listdir(read_dir):
            if f.endswith(".json"):
                row_id = f[:-5]
                items = load_json(os.path.join(read_dir, f), [])
                for it in items:
                    fname = it.get("file")
                    base = it.get("base", "")
                    if fname:
                        read_by_file[(row_id, fname)] = it
                        read_by_base_file[(base, fname)] = it
                        read_by_file[fname] = it
                    if it.get("vid"):
                        read_by_vid[it["vid"]] = it

    return read_by_file, read_by_base_file, read_by_vid


def load_series_cards():
    """Load series card json files."""
    ser_dir = os.path.join(HAW, "playlists", "series")
    cards = {}
    if os.path.isdir(ser_dir):
        for f in os.listdir(ser_dir):
            if f.endswith(".json") and f != "index.json":
                d = load_json(os.path.join(ser_dir, f))
                slug = d.get("slug") or f[:-5]
                cards[slug] = d
    return cards


def run_inventory():
    t0 = time.time()
    os.makedirs(META_DIR, exist_ok=True)

    print("Loading reference ground truth datasets...")
    row_map = build_row_map()
    dump_atomic(row_map, os.path.join(META_DIR, "row_map.json"))

    sheikh_map = build_sheikh_map()
    dump_atomic(sheikh_map, os.path.join(META_DIR, "sheikh_map.json"))

    v2p = load_json(os.path.join(HAW, "playlists", "data", "vid_plists.json"))
    ytt = load_json(os.path.join(HAW, "playlists", "data", "yt_titles.json"))
    ytv = ytt.get("v") or {}

    inv_pl = {}
    for vid, pls in v2p.items():
        for pl, pos, tot in pls:
            inv_pl[(pl, pos)] = vid

    series_cards = load_series_cards()
    read_by_file, read_by_base_file, read_by_vid = load_read_indexes()

    irth_vids = load_json(os.path.join(IRTH, "data", "tube", "videos.json")).get("rows") or []
    irth_id2yt = {v["id"]: v["yt"] for v in irth_vids if v.get("yt")}
    irth_id2speaker = {v["id"]: (v.get("speakers") or [""])[0] for v in irth_vids}

    manifest = load_json(os.path.join(DES, "mutalaa", "data", "manifest.json"), [])
    man_row_map = {str(r["id"]): r for r in manifest}

    print("Fetching git commit timestamps...")
    commit_timestamps = get_git_commit_timestamps()

    # Collect files
    print("Collecting files from stores...")
    lecture_files = []
    for st_code, st_root, ext in STORE_DIRS:
        if not os.path.isdir(st_root):
            continue
        for root, dirs, files in os.walk(st_root):
            for f in files:
                if st_code == "hw-tr" and "maktaba" in root.split(os.sep):
                    continue
                if (ext == "transcript.txt" and f == "transcript.txt") or (ext == ".txt" and f.endswith(".txt")):
                    lecture_files.append((st_code, os.path.join(root, f)))

    special_files = []
    # Maktaba
    maktaba_root = os.path.join(HAW, "transcripts", "maktaba")
    if os.path.isdir(maktaba_root):
        for root, dirs, files in os.walk(maktaba_root):
            for f in files:
                if f.endswith(".txt"):
                    special_files.append(("maktaba", os.path.join(root, f)))

    # Irth-simulation
    irth_sim_root = os.path.join(HAW, "irth-simulation", "content", "tube")
    if os.path.isdir(irth_sim_root):
        for root, dirs, files in os.walk(irth_sim_root):
            for f in files:
                if f == "transcript.txt":
                    special_files.append(("irth-sim", os.path.join(root, f)))

    # Inbox
    inbox_root = os.path.join(HAW, "inbox")
    if os.path.isdir(inbox_root):
        for root, dirs, files in os.walk(inbox_root):
            for f in files:
                special_files.append(("inbox", os.path.join(root, f)))

    all_files = lecture_files + special_files
    print(f"Total files to process: {len(all_files)} (lectures: {len(lecture_files)}, special: {len(special_files)})")

    records = []
    for st_code, full_path in all_files:
        rel_path = os.path.relpath(full_path, W)
        file_bytes = os.path.getsize(full_path)
        with open(full_path, "rb") as fh:
            raw_b = fh.read()
        sha = hashlib.sha256(raw_b).hexdigest()

        commit_ts = commit_timestamps.get(rel_path) or int(os.path.getmtime(full_path))

        # Check if text
        is_text = False
        try:
            txt = raw_b.decode("utf-8")
            is_text = True
        except Exception:
            try:
                txt = raw_b.decode("utf-8", errors="replace")
                is_text = True
            except Exception:
                txt = ""

        if is_text and st_code != "inbox":
            h_info, norm_body, nh, chars_body, quality = extract_header_and_body(txt)
        else:
            h_info = {"sheikh": None, "playlist": None, "vid": None}
            norm_body = ""
            nh = sha
            chars_body = len(raw_b)
            quality = "ok"

        fname = os.path.basename(full_path)
        parts = full_path.split(os.sep)

        # ID extraction
        fname_vid = vid_of(fname, v2p, ytv)
        read_vid = None
        card_vid = None
        irth_vid = None
        row_key_raw = None
        canon_row_id = None
        n_candidates = {"read": None, "card": None, "plpos": None, "mutfile": None, "lsfile": None, "trfile": None}

        # Candidate n from file names
        if st_code == "des-mut":
            row_key_raw = parts[-2]
            m = NUM_RE.match(fname)
            if m:
                n_candidates["mutfile"] = int(m.group(1))
            # Canon row
            canon_row_id = row_map.get(f"k:{row_key_raw}") or row_map.get(f"m:{row_key_raw}") or row_map.get(row_key_raw)
            # Read match
            read_item = read_by_file.get((canon_row_id, fname)) or read_by_file.get(fname)
            if read_item:
                read_vid = read_item.get("vid")
                n_candidates["read"] = read_item.get("n")
        elif st_code == "des-dur":
            row_key_raw = parts[-2]
            canon_row_id = row_map.get(f"k:{row_key_raw}") or row_map.get(f"m:{row_key_raw}") or row_map.get(row_key_raw)
            # des-dur file numbers are NOT lesson numbers (F5), leaving n_candidates empty for durfile
        elif st_code == "hw-tr":
            sheikh_dir = parts[-3] if len(parts) >= 3 else ""
            row_dir = parts[-2] if len(parts) >= 2 else ""
            row_key_raw = f"{sheikh_dir}/{row_dir}" if sheikh_dir else row_dir
            canon_row_id = (
                row_map.get(f"t:{sheikh_dir}-{row_dir}")
                or row_map.get(f"k:{row_dir}")
                or row_map.get(f"m:{row_dir}")
                or row_map.get(f"s:{row_dir}")
                or row_map.get(row_dir)
            )
            m = NUM_RE.match(fname)
            if m:
                n_candidates["trfile"] = int(m.group(1))
            read_item = read_by_file.get((canon_row_id, fname)) or read_by_file.get(fname)
            if read_item:
                read_vid = read_item.get("vid")
                n_candidates["read"] = read_item.get("n")
        elif st_code == "hw-ls":
            slug = parts[-2]
            row_key_raw = slug
            canon_row_id = row_map.get(f"s:{slug}") or row_map.get(slug)
            stem = fname.split(".")[0]
            if stem.isdigit():
                n_candidates["lsfile"] = int(stem)
            card = series_cards.get(slug)
            if card:
                n_val = n_candidates["lsfile"]
                if n_val is not None:
                    for l in card.get("lessons") or []:
                        if l.get("n") == n_val:
                            if l.get("video"):
                                card_vid = l["video"]
                            n_candidates["card"] = l.get("n")
                            break
            read_item = read_by_file.get((canon_row_id, fname)) or read_by_file.get(fname)
            if read_item:
                read_vid = read_item.get("vid")
                if read_item.get("n") is not None:
                    n_candidates["read"] = read_item.get("n")
        elif st_code == "irth":
            lesson_id = parts[-2]
            row_key_raw = lesson_id
            irth_vid = irth_id2yt.get(lesson_id)
            m = NUM_RE.search(lesson_id.rsplit("-", 1)[-1])
            if m:
                n_candidates["trfile"] = int(m.group(1))
        elif st_code == "irth-sim":
            lesson_id = parts[-2]
            row_key_raw = lesson_id
            irth_vid = irth_id2yt.get(lesson_id)

        # Playlist position check
        target_vid = h_info.get("vid") or fname_vid or read_vid or card_vid or irth_vid
        plist_id = h_info.get("playlist")
        if plist_id and "list=" in plist_id:
            m_pl = PL_RE.search(plist_id)
            if m_pl:
                plist_id = m_pl.group(1)

        if target_vid and plist_id:
            for p, pos, tot in v2p.get(target_vid, []):
                if p == plist_id:
                    n_candidates["plpos"] = pos
                    break

        rec = {
            "store": st_code,
            "path": rel_path,
            "bytes": file_bytes,
            "sha256": sha,
            "nh": nh,
            "chars_body": chars_body,
            "header": h_info,
            "fname_vid": fname_vid,
            "read_vid": read_vid,
            "card_vid": card_vid,
            "irth_vid": irth_vid,
            "row_key_raw": row_key_raw,
            "row_id": canon_row_id,
            "n_candidates": n_candidates,
            "commit_ts": commit_ts,
            "quality": quality,
        }
        records.append(rec)

    # Write inventory.jsonl
    inv_jsonl_path = os.path.join(META_DIR, "inventory.jsonl")
    dump_jsonl_atomic(records, inv_jsonl_path)
    print(f"Wrote {len(records)} records to {inv_jsonl_path}")

    # Build INVENTORY.json summary
    store_stats = {}
    for st_code, st_root, ext in STORE_DIRS + SPECIAL_STORES:
        store_recs = [r for r in records if r["store"] == st_code]
        if not store_recs:
            continue
        st_files = len(store_recs)
        st_bytes = sum(r["bytes"] for r in store_recs)
        st_hashes = len({r["sha256"] for r in store_recs})

        # Coverage by sheikh
        sheikh_counter = collections.Counter()
        for r in store_recs:
            sh = None
            if r["header"].get("sheikh"):
                sh = sheikh_map.get(norm(r["header"]["sheikh"])) or sheikh_map.get(r["header"]["sheikh"])
            if not sh and r["row_id"]:
                sh = r["row_id"].split("--")[0]
            if not sh and r["store"] == "irth":
                spk = irth_id2speaker.get(r["row_key_raw"])
                sh = sheikh_map.get(spk)
            if not sh and r["row_key_raw"] in man_row_map:
                m_sh = man_row_map[r["row_key_raw"]].get("sheikh")
                sh = sheikh_map.get(norm(m_sh)) or sheikh_map.get(m_sh)
            sheikh_counter[sh or "unattributed"] += 1

        store_stats[st_code] = {
            "files": st_files,
            "unique_hashes": st_hashes,
            "bytes": st_bytes,
            "coverage_by_sheikh": dict(sheikh_counter.most_common()),
        }

    # Count excluded des corpora
    excluded_counts = {}
    excluded_list = []
    for prefix, reason in EXCLUDED_DES_CORPORA:
        p_abs = os.path.join(W, prefix)
        cnt = 0
        if os.path.isdir(p_abs):
            for r, d, fs in os.walk(p_abs):
                cnt += len(fs)
        excluded_counts[prefix] = cnt
        excluded_list.append({
            "path_prefix": prefix,
            "reason": reason,
            "file_count": cnt
        })

    # Add special excluded collections to excluded_list
    excluded_list.insert(0, {
        "path_prefix": "hawshat/irth-simulation",
        "reason": "كلام عشوائي مُولَّد (synthetic text, no real lecture video)",
        "file_count": len([r for r in records if r["store"] == "irth-sim"])
    })
    excluded_list.insert(1, {
        "path_prefix": "hawshat/transcripts/maktaba",
        "reason": "كتب ومتون مفرغة وبعضها ملوّث بتفكير النموذج (books/matn)",
        "file_count": len([r for r in records if r["store"] == "maktaba"])
    })
    excluded_list.insert(2, {
        "path_prefix": "hawshat/inbox",
        "reason": "ملفات محاذاة فقط بلا نصوص تفريغ (align JSON only)",
        "file_count": len([r for r in records if r["store"] == "inbox"])
    })

    dump_atomic(excluded_list, os.path.join(META_DIR, "excluded.json"))

    inv_summary = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_records": len(records),
        "lecture_transcripts_count": len(lecture_files),
        "stores": store_stats,
        "excluded_corpora": excluded_counts,
    }
    inv_json_path = os.path.join(META_DIR, "INVENTORY.json")
    dump_atomic(inv_summary, inv_json_path)
    print(f"Wrote inventory summary to {inv_json_path}")
    print(f"P1 Inventory finished in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    run_inventory()
