#!/usr/bin/env python3
"""Download per-author affiliation files for NeurIPS, ICML, ICLR.

Source: Paper Copilot's OpenReview archive (github.com/papercopilot/openreview),
the `authors/<venue>/<venue><year>.jsonl` files. Each row is one paper with
per-author fields joined by ';' — notably `aff_domain` (institutional email
domain), `aff` (institution name), and `position` (e.g. "PhD student").

Small (~70 MB total). Saved to data/conf/. Cite arXiv:2510.13201.

Usage: python download_conf_data.py [--force]
"""
import argparse
import json
import os
import urllib.request

VENUES = ("nips", "icml", "iclr")  # nips == NeurIPS in this archive
TREE_API = "https://api.github.com/repos/papercopilot/openreview/git/trees/main?recursive=1"
RAW = "https://raw.githubusercontent.com/papercopilot/openreview/main/"
DEST = os.path.join(os.path.dirname(__file__), "data", "conf")


def list_author_files():
    with urllib.request.urlopen(TREE_API) as r:
        tree = json.load(r)["tree"]
    return [
        x["path"] for x in tree
        if x["type"] == "blob"
        and any(x["path"].startswith(f"authors/{v}/") for v in VENUES)
        and x["path"].endswith(".jsonl")
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    os.makedirs(DEST, exist_ok=True)
    paths = list_author_files()
    print(f"Found {len(paths)} author files for {', '.join(VENUES)}.")
    for p in paths:
        out = os.path.join(DEST, p.replace("authors/", "").replace("/", "_"))
        if os.path.exists(out) and not args.force:
            continue
        urllib.request.urlretrieve(RAW + p, out)
        print(f"  {os.path.getsize(out) / 1e6:6.2f} MB  {os.path.basename(out)}")
    print(f"Done -> {DEST}")


if __name__ == "__main__":
    main()
