#!/usr/bin/env python3
"""apply.py - Materialise the ytb tree, metadata files, variants, and accounting ledger.

P4: Copies winner files to ytb/<target> and writes <stem>.meta.json.
P5: Copies losing variant files to _variants/<stem>.<store>.txt for the 43 conflicts.
Writes _meta/ledger.jsonl for all 9,085 inventory records.
Stdlib only, idempotent and resumable.
"""

import hashlib
import json
import os
import sys

# Directory paths
W = "/root/workspace"
YTB = os.path.join(W, "ytb")
META_DIR = os.path.join(YTB, "_meta")
PLAN_FILE = os.path.join(META_DIR, "plan.jsonl")
RESOLVE_FILE = os.path.join(META_DIR, "RESOLVE.json")
CONFLICTS_FILE = os.path.join(META_DIR, "conflicts.jsonl")
INVENTORY_FILE = os.path.join(META_DIR, "inventory.jsonl")
SOURCE_HEADS_FILE = os.path.join(META_DIR, "source_heads.json")
LEDGER_FILE = os.path.join(META_DIR, "ledger.jsonl")
STOP_FILE = os.path.join(META_DIR, "STOP.md")


def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def write_atomic_bytes(content_bytes, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(content_bytes)
    os.replace(tmp_path, target_path)


def write_atomic_json(obj, target_path):
    tmp_path = target_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp_path, target_path)


def main():
    print("=" * 60)
    print("ytb materialization: Starting P4 & P5 (apply.py)")
    print("=" * 60)

    # Load source heads
    with open(SOURCE_HEADS_FILE, "r", encoding="utf-8") as f:
        source_heads = json.load(f)

    # Load resolve ledger
    print("Loading RESOLVE.json...")
    with open(RESOLVE_FILE, "r", encoding="utf-8") as f:
        resolve_data = json.load(f)
    ledger_entries = resolve_data["ledger"]

    # Load plan
    print("Loading plan.jsonl...")
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan_records = [json.loads(line) for line in f]

    total_lessons = len(plan_records)
    print(f"Total lessons to materialize: {total_lessons}")

    batch_size = 400
    copied_count = 0
    skipped_count = 0
    metas_written = 0

    # 1. Materialise tree and meta files
    for idx, p in enumerate(plan_records, 1):
        lid = p["lid"]
        target_rel = p["target"]
        target_full = os.path.join(YTB, target_rel)
        res_entry = ledger_entries[lid]

        winner_rel = res_entry["winner"]["path"]
        src_full = os.path.join(W, winner_rel)

        # Winner bytes
        with open(src_full, "rb") as sf:
            src_bytes = sf.read()
        src_sha = hashlib.sha256(src_bytes).hexdigest()

        expected_sha = res_entry["winner"]["sha256"]
        if src_sha != expected_sha:
            msg = f"ERROR: SHA mismatch on source file {src_full}: got {src_sha} vs expected {expected_sha}"
            with open(STOP_FILE, "w", encoding="utf-8") as stf:
                stf.write(msg + "\n")
            print(msg, file=sys.stderr)
            sys.exit(1)

        os.makedirs(os.path.dirname(target_full), exist_ok=True)

        # Idempotent write of content
        if os.path.isfile(target_full):
            cur_sha = get_file_sha256(target_full)
            if cur_sha == src_sha:
                skipped_count += 1
            else:
                msg = f"ERROR: Collision on target {target_full}: existing {cur_sha} != winner {src_sha}"
                with open(STOP_FILE, "w", encoding="utf-8") as stf:
                    stf.write(msg + "\n")
                print(msg, file=sys.stderr)
                sys.exit(1)
        else:
            write_atomic_bytes(src_bytes, target_full)
            copied_count += 1

        # Meta file
        meta_full = os.path.splitext(target_full)[0] + ".meta.json"

        # Determine git head
        repo_prefix = winner_rel.split("/")[0]
        repo_key = "des" if repo_prefix == "des" else ("irth" if repo_prefix == "irth" else "hawshat")
        head_commit = source_heads.get(repo_key, {}).get("head", "")[:7]

        # Variants list formatted as _variants/<basename>
        variants_list = []
        if res_entry.get("losing_variants"):
            for v in res_entry["losing_variants"]:
                v_base = os.path.basename(v["variant_path"])
                variants_list.append(f"_variants/{v_base}")

        # Meta content
        chars_count = len(src_bytes.decode("utf-8", errors="replace"))
        meta_obj = {
            "v": 1,
            "lid": res_entry["lid"],
            "vid": res_entry["vid"],
            "sheikh": res_entry["sheikh"],
            "row_id": res_entry["row_id"],
            "n": res_entry["n"],
            "n_src": res_entry["n_src"],
            "title": res_entry["title"],
            "title_src": res_entry["title_src"],
            "sha256": res_entry["winner"]["sha256"],
            "nh": res_entry["winner"]["nh"],
            "chars": chars_count,
            "quality": res_entry["winner"]["quality"],
            "winner": {
                "store": res_entry["winner"]["store"],
                "path": res_entry["winner"]["path"],
                "commit_ts": res_entry["winner"]["commit_ts"],
                "head": head_commit
            },
            "sources": [
                {
                    "store": s["store"],
                    "path": s["path"],
                    "sha256": s["sha256"],
                    "rel": s["rel"]
                }
                for s in res_entry["sources"]
            ],
            "variants": variants_list,
            "also_in": res_entry.get("also_in", [])
        }

        # Check if meta file matches or needs write
        need_meta_write = True
        if os.path.isfile(meta_full):
            try:
                with open(meta_full, "r", encoding="utf-8") as mf:
                    existing_meta = json.load(mf)
                if existing_meta == meta_obj:
                    need_meta_write = False
            except Exception:
                need_meta_write = True

        if need_meta_write:
            write_atomic_json(meta_obj, meta_full)
        metas_written += 1

        # Batch progress reporting
        if idx % batch_size == 0 or idx == total_lessons:
            batch_num = (idx - 1) // batch_size + 1
            total_batches = (total_lessons + batch_size - 1) // batch_size
            print(f"[Batch {batch_num:02d}/{total_batches:02d}] {idx:4d}/{total_lessons} lessons processed | "
                  f"newly copied: {copied_count}, verified/cached: {skipped_count}, metas written: {metas_written}")

    # 2. Materialise variants (P5)
    print("\nArchiving losing variants for 43 conflicting lessons...")
    with open(CONFLICTS_FILE, "r", encoding="utf-8") as f:
        conflicts = [json.loads(line) for line in f]

    variants_copied = 0
    variants_skipped = 0
    for c in conflicts:
        for loser in c["losers"]:
            v_src = os.path.join(W, loser["path"])
            v_target = os.path.join(YTB, loser["variant_path"])
            os.makedirs(os.path.dirname(v_target), exist_ok=True)

            with open(v_src, "rb") as vsf:
                v_bytes = vsf.read()
            v_sha = hashlib.sha256(v_bytes).hexdigest()

            if os.path.isfile(v_target):
                cur_v_sha = get_file_sha256(v_target)
                if cur_v_sha == v_sha:
                    variants_skipped += 1
                else:
                    write_atomic_bytes(v_bytes, v_target)
                    variants_copied += 1
            else:
                write_atomic_bytes(v_bytes, v_target)
                variants_copied += 1

    total_variants = variants_copied + variants_skipped
    print(f"Variants archived: {total_variants} files ({variants_copied} newly written, {variants_skipped} verified/cached)")

    # 3. Write accounting ledger (_meta/ledger.jsonl)
    print("\nGenerating source reconciliation ledger (_meta/ledger.jsonl)...")
    winner_paths = {}
    for lid, entry in ledger_entries.items():
        winner_paths[entry["winner"]["path"]] = (lid, entry["target"])

    loser_paths = {}
    for c in conflicts:
        for l in c["losers"]:
            loser_paths[l["path"]] = (c["lid"], l["variant_path"])

    all_sources = {}
    for lid, entry in ledger_entries.items():
        for s in entry["sources"]:
            all_sources[s["path"]] = (lid, s, entry)

    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        inv_records = [json.loads(line) for line in f]

    ledger_records = []
    for r in inv_records:
        p = r["path"]
        sha = r["sha256"]
        store = r["store"]

        if p in winner_paths:
            lid, target = winner_paths[p]
            decision = "copied"
            ytb_path = target
        elif p in loser_paths:
            lid, vpath = loser_paths[p]
            decision = "variant"
            ytb_path = vpath
        elif p in all_sources:
            lid, s, entry = all_sources[p]
            if s["rel"] in ("identical", "same-body"):
                decision = "duplicate"
                ytb_path = entry["target"]
            else:
                # duplicate of a variant
                matched_vpath = None
                for lv in entry.get("losing_variants", []):
                    if lv["sha256"] == sha:
                        matched_vpath = lv["variant_path"]
                        break
                decision = "duplicate"
                ytb_path = matched_vpath or entry["target"]
        elif store == "irth-sim":
            decision = "excluded"
            ytb_path = None
            lid = None
        elif store == "maktaba":
            decision = "excluded"
            ytb_path = None
            lid = None
        elif store == "inbox":
            decision = "deferred"
            ytb_path = None
            lid = None
        else:
            decision = "unknown"
            ytb_path = None
            lid = None

        ledger_records.append({
            "store": store,
            "path": p,
            "sha256": sha,
            "decision": decision,
            "ytb_path": ytb_path,
            "lid": lid
        })

    tmp_ledger = LEDGER_FILE + ".tmp"
    with open(tmp_ledger, "w", encoding="utf-8") as f:
        for lr in ledger_records:
            f.write(json.dumps(lr, ensure_ascii=False) + "\n")
    os.replace(tmp_ledger, LEDGER_FILE)

    from collections import Counter
    counts = Counter(lr["decision"] for lr in ledger_records)
    print(f"Ledger written: {len(ledger_records)} records total")
    print(f"  Breakdown: {dict(counts)}")
    print("Execution of apply.py finished successfully.")


if __name__ == "__main__":
    main()
