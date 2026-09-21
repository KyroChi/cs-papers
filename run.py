#!/usr/bin/env python3
"""Run a SQL query against the arXiv metadata parquet with DuckDB.

The views in setup.sql are (re)created every run, so `papers` and
`papers_enriched` are always available to your query.

Usage:
    python run.py -f queries/01_growth_by_year.sql
    python run.py "SELECT count(*) FROM papers"
    python run.py            # drop into an interactive DuckDB SQL shell
"""
import argparse
import os
import sys

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "arxiv_metadata.parquet")


def connect():
    if not os.path.exists(DATA):
        sys.exit("Data not found. Run: python download_data.py")
    con = duckdb.connect()
    con.execute(f"SET file_search_path = '{HERE}'")
    with open(os.path.join(HERE, "setup.sql")) as fh:
        con.execute(fh.read())
    # Conference views (NeurIPS/ICML/ICLR) — only if that data is present.
    import glob
    if glob.glob(os.path.join(HERE, "data", "conf", "*.jsonl")):
        with open(os.path.join(HERE, "conf_setup.sql")) as fh:
            con.execute(fh.read())
    return con


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sql", nargs="?", help="inline SQL to run")
    ap.add_argument("-f", "--file", help="path to a .sql file to run")
    args = ap.parse_args()

    con = connect()

    if args.file:
        with open(args.file) as fh:
            sql = fh.read()
    elif args.sql:
        sql = args.sql
    else:
        # interactive shell
        print("arXiv DuckDB shell. Views: papers, papers_enriched. Ctrl-D to exit.")
        while True:
            try:
                line = input("duckdb> ")
            except EOFError:
                break
            if line.strip():
                try:
                    con.sql(line).show(max_rows=100)
                except Exception as e:  # noqa: BLE001
                    print("ERROR:", e)
        return

    # Support multi-statement .sql files: show each SELECT's result.
    # Strip line comments first so a ';' inside a comment doesn't split a
    # statement (our SQL has no '--' inside string literals).
    no_comments = "\n".join(line.split("--", 1)[0] for line in sql.splitlines())
    statements = [s.strip() for s in no_comments.split(";") if s.strip()]
    for stmt in statements:
        rel = con.sql(stmt)
        if rel is not None:
            rel.show(max_rows=200)


if __name__ == "__main__":
    main()
