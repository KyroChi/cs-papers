#!/usr/bin/env python3
"""Download the berenslab/iclr-dataset parquets — ICLR SUBMISSIONS incl. rejected,
with an accept/reject `decision` label and reviewer `scores`.

This is the rejection-inclusive dataset: `decision` in {Reject, Withdrawn, Desk
rejected, Accept (Poster/Spotlight/Oral)...}. Join to our conference author data
by `id` (OpenReview forum id). NeurIPS/ICML rejected submissions are not public,
so this covers ICLR only. Saved to data/iclr_decisions/.

Usage: python download_iclr_decisions.py [--force]
"""
import argparse
import json
import os
import urllib.request

TREE = "https://api.github.com/repos/berenslab/iclr-dataset/git/trees/main?recursive=1"
RAW = "https://raw.githubusercontent.com/berenslab/iclr-dataset/main/"
DEST = os.path.join(os.path.dirname(__file__), "data", "iclr_decisions")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    os.makedirs(DEST, exist_ok=True)
    with urllib.request.urlopen(TREE) as r:
        tree = json.load(r)["tree"]
    files = [x["path"] for x in tree
             if x["type"] == "blob" and x["path"].startswith("data/")
             and x["path"].endswith(".parquet")]
    print(f"Found {len(files)} parquet files.")
    for p in files:
        out = os.path.join(DEST, os.path.basename(p))
        if os.path.exists(out) and not args.force:
            continue
        urllib.request.urlretrieve(RAW + p, out)
        print(f"  {os.path.getsize(out)/1e6:6.2f} MB  {os.path.basename(out)}")
    print(f"Done -> {DEST}")

if __name__ == "__main__":
    main()
