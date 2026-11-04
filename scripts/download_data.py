#!/usr/bin/env python3
"""Download ONLY the arXiv metadata from the HF `arxiv-complete` dataset.

The full dataset is ~16 TiB (PDFs, LaTeX source, PostScript). We want none
of that. The repo exposes a separate `metadata` config — a single 1.6 GB
parquet with every field we need (authors, categories, first_version_date,
n_versions, ...). This script fetches just that file.

Usage:
    python download_data.py            # download if missing
    python download_data.py --force    # re-download
"""
import argparse
import os
import sys
import urllib.request

URL = (
    "https://huggingface.co/datasets/secemp9/arxiv-complete/"
    "resolve/main/metadata/train-00000-of-00001.parquet"
)
DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "arxiv_metadata.parquet")

def _progress(block_num, block_size, total_size):
    done = block_num * block_size
    if total_size > 0:
        pct = min(100, done * 100 // total_size)
        sys.stdout.write(
            f"\r  {pct:3d}%  {done / 1e9:5.2f} / {total_size / 1e9:5.2f} GB"
        )
        sys.stdout.flush()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    if os.path.exists(DEST) and not args.force:
        size = os.path.getsize(DEST) / 1e9
        print(f"Already downloaded: {DEST} ({size:.2f} GB). Use --force to refresh.")
        return

    print(f"Downloading arXiv metadata (~1.6 GB) ->\n  {DEST}")
    urllib.request.urlretrieve(URL, DEST, _progress)
    print(f"\nDone: {os.path.getsize(DEST) / 1e9:.2f} GB")

if __name__ == "__main__":
    main()
