#!/usr/bin/env python3
"""Shared definitions and helper functions for ytb consolidation tools."""

import collections
import hashlib
import json
import os
import re
import subprocess
import time

# Directory constants
W = "/root/workspace"
HAW = os.path.join(W, "hawshat")
DES = os.path.join(W, "des")
IRTH = os.path.join(W, "irth")
YTB = os.path.join(W, "ytb")
META_DIR = os.path.join(YTB, "_meta")
TOOLS_DIR = os.path.join(YTB, "tools")

# Regexes
HDR_VID = re.compile(r"(?:youtu\.be/|watch\?v=|/shorts/)([A-Za-z0-9_-]{11})")
PL_RE = re.compile(r"list=([A-Za-z0-9_-]+)")
CONTAM_RE = re.compile(r"^(thought\b|Now let\'s\b|<thought>|Thinking Process:)", re.I | re.M)
NUM_RE = re.compile(r"^(\d{1,4})")
NAYT_RE = re.compile(r"NA_([A-Za-z0-9_-]{11})")
AR_DIAC = re.compile(r"[ً-ْٰ]")
CTL_RE = re.compile(r"[‎-‏⁦-⁩­]")

# Stores configuration
STORE_DIRS = [
    ("hw-tr", os.path.join(HAW, "transcripts"), ".txt"),
    ("hw-ls", os.path.join(HAW, "playlists", "lessons"), ".txt"),
    ("irth", os.path.join(IRTH, "content", "tube"), "transcript.txt"),
    ("des-mut", os.path.join(DES, "mutalaa", "data", "txt"), ".txt"),
    ("des-dur", os.path.join(DES, "durus", "transcripts"), ".txt"),
]

SPECIAL_STORES = [
    ("maktaba", os.path.join(HAW, "transcripts", "maktaba"), ".txt"),
    ("irth-sim", os.path.join(HAW, "irth-simulation", "content", "tube"), "transcript.txt"),
    ("inbox", os.path.join(HAW, "inbox"), ""),
]

EXCLUDED_DES_CORPORA = [
    ("des/shami", "كتب الشامي (book corpus)"),
    ("des/nusus", "نصوص وكتب (book corpus)"),
    ("des/kutub", "كتب (book corpus)"),
    ("des/manzuma", "منظومات وشروح (book corpus)"),
    ("des/jadid2", "كوربوس إنجليزي/جديد (book corpus)"),
]

# gen_stats constants
TR_EXCLUDE = {
    ("bouti", "tawba"), ("bouti", "rihab"), ("bouti", "hikam"), ("bouti", "tafsir"),
    ("sariri", "manhaj-muntakhab"), ("maktaba", "book-um_baraheen_d1")
}

TR_FOLD = {
    ("bardouni", "ajhuri"): "10",
    ("jifri", "insaniyya"): "117"
}

GEN_REDIRECTS = {
    "said-bouti--bouti-tawba": "said-bouti--356",
    "said-bouti--bouti-rihab": "said-bouti--337",
    "said-bouti--bouti-hikam": "said-bouti--386",
    "said-bouti--bouti-tafsir": "said-bouti--414",
    "said-bouti--bouti-mut-353": "said-bouti--353",
    "said-bouti--bouti-tazkiya": "said-bouti--415",
    "said-bouti--bouti-sahaba": "said-bouti--387",
    "said-bouti--bouti-ibada": "said-bouti--416",
    "said-bouti--bouti-mut-386": "said-bouti--386",
    "said-bouti--bouti-dayoon": "said-bouti--365",
    "habib-ali-aljifri--jifri-mut-123": "habib-ali-aljifri--123",
    "ahmed-alsayed--alsayed-mut-672": "ahmed-alsayed--672",
    "ahmed-alsayed--alsayed-mut-686": "ahmed-alsayed--686",
    "bardouni-husaymi--ajhuri": "bardouni-husaymi--10",
    "said-bouti--bardouni-ajhuri": "bardouni-husaymi--10",
    "habib-ali-aljifri--jifri-insaniyya": "habib-ali-aljifri--117",
    "said-bouti--bouti-muhammad": "said-bouti--366",
    "ali-gomaa--gomaa-mut-822": "ali-gomaa--822",
    "ali-gomaa--mut-822": "ali-gomaa--822",
    "ali-gomaa--gomaa-khawarij": "ali-gomaa--822",
    "ali-gomaa--khawarij": "ali-gomaa--822",
    "bardouni-husaymi--iqbar-intisar": "bardouni-husaymi--994",
    "bardouni-husaymi--bardouni-iqbar-intisar": "bardouni-husaymi--994",
    "bardouni-husaymi--sharh-risala-2": "bardouni-husaymi--1003",
    "bardouni-husaymi--bardouni-sharh-risala-2": "bardouni-husaymi--1003",
}

# The 12 created rows (11 mutalaa + durus 37)
CREATED_ROWS = {
    "36": "mouloud-sariri--36",
    "37": "mouloud-sariri--37",
    "40": "mouloud-sariri--40",
    "112": "habib-ali-aljifri--112",
    "173": "habib-omar-ibn-hafiz--173",
    "344": "said-bouti--bouti-khutab-2010",
    "355": "said-bouti--bouti-muqtatafat-ulum",
    "743": "adham-alasimi--743",
    "871": "ali-gomaa--871",
    "985": "bardouni-husaymi--bardouni-mut-985",
    "995": "bardouni-husaymi--10",
}


def norm(s):
    """Normalize Arabic text for robust string matching."""
    s = AR_DIAC.sub("", s or "")
    s = re.sub(r"[^\w\s]", "", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    s = s.replace("ؤ", "و").replace("ئ", "ي").replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"\s+", " ", s).strip()


def clean_title(t):
    t = CTL_RE.sub("", t or "")
    t = re.sub(r"\s*English Subtitle\s*$", "", t, flags=re.I)
    t = t.replace("_", " ")
    return re.sub(r"\s+", " ", t).strip(" -–—|/\\")


def dump_atomic(obj, path, indent=1):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, path)


def dump_jsonl_atomic(records, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def load_json(p, default=None):
    if not os.path.exists(p):
        return default if default is not None else {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def get_git_commit_timestamps():
    """Retrieve the latest git commit timestamp for every source file."""
    subdirs = [
        ("hawshat", "transcripts"),
        ("hawshat", "playlists/lessons"),
        ("des", "mutalaa/data/txt"),
        ("des", "durus/transcripts"),
        ("irth", "content/tube"),
        ("hawshat", "irth-simulation"),
        ("hawshat", "inbox"),
    ]
    file_ts = {}
    for repo, subdir in subdirs:
        repo_path = os.path.join(W, repo)
        cmd = ["git", "-C", repo_path, "log", "--format=C %ct", "--name-only", "--", subdir]
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, errors="replace")
            cur_ts = 0
            for line in p.stdout:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("C "):
                    cur_ts = int(line[2:])
                else:
                    full_rel = os.path.join(repo, line)
                    if full_rel not in file_ts:
                        file_ts[full_rel] = cur_ts
            p.wait()
        except Exception:
            pass
    return file_ts


def extract_header_and_body(text):
    """
    Extract 3-line header (الشيخ / السلسلة / الفيديو) from first 400 chars,
    remove it, and compute normalized body.
    """
    lines = text.splitlines()
    header_info = {"sheikh": None, "playlist": None, "vid": None}
    header_indices = []
    seen_sheikh, seen_other = False, False

    for idx, line in enumerate(lines[:6]):
        s = line.strip()
        if not s:
            if header_indices:
                header_indices.append(idx)
                break
            continue
        if s.startswith("الشيخ:"):
            seen_sheikh = True
            header_info["sheikh"] = s[len("الشيخ:"):].strip()
            header_indices.append(idx)
        elif s.startswith("السلسلة:"):
            seen_other = True
            header_info["playlist"] = s[len("السلسلة:"):].strip()
            header_indices.append(idx)
        elif s.startswith("الفيديو:"):
            seen_other = True
            m = HDR_VID.search(s)
            if m:
                header_info["vid"] = m.group(1)
            header_indices.append(idx)
        else:
            break

    # سطر الشيخ: لا يُعتدّ به إلا إذا تبعه سطر السلسلة: أو الفيديو:
    if seen_sheikh and not seen_other:
        header_indices = []
        header_info = {"sheikh": None, "playlist": None, "vid": None}

    if header_indices:
        last_h = max(header_indices)
        body = "\n".join(lines[last_h + 1:])
    else:
        body = text

    norm_body = " ".join(body.split())
    nh = hashlib.sha256(norm_body.encode("utf-8")).hexdigest()
    chars_body = len(norm_body)

    if CONTAM_RE.search(text):
        quality = "contaminated"
    elif chars_body < 300:
        quality = "short"
    else:
        quality = "ok"

    return header_info, norm_body, nh, chars_body, quality


def vid_of(fname, v2p, ytv):
    """Extract YouTube video id from filename with ground truth check (gen_stats.py)."""
    b = os.path.basename(fname)
    m = NAYT_RE.search(b)
    if m:
        return m.group(1)
    m = re.search(r"[\-_]([A-Za-z0-9_\-]{11})\.txt$", b)
    if not m:
        return None
    v = m.group(1)
    if v not in v2p and v not in ytv:
        return None
    return v


def compute_jaccard_4gram(text_a, text_b):
    """Compute character 4-gram Jaccard similarity between two texts."""
    if text_a == text_b:
        return 1.0
    if len(text_a) < 4 or len(text_b) < 4:
        return 1.0 if text_a == text_b else 0.0
    grams_a = set(text_a[i:i + 4] for i in range(len(text_a) - 3))
    grams_b = set(text_b[i:i + 4] for i in range(len(text_b) - 3))
    union = grams_a | grams_b
    if not union:
        return 1.0
    return round(len(grams_a & grams_b) / len(union), 4)


class UF:
    """Disjoint Set / Union-Find with path compression."""

    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra
