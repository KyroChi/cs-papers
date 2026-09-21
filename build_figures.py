#!/usr/bin/env python3
"""Compute the aggregate data for the interactive figures and dump figures.json.

Reads the arXiv metadata parquet (setup.sql views) and, for the region figure,
the conference data (conf_setup.sql). Output is small aggregates only — safe to
embed directly in the HTML document.
"""
import datetime
import glob
import json
import os
import sys

import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
# Findings are written to results/figures.json (the "latest", read by the
# distill build) and archived per-run under results/archive/ so every re-run
# is preserved.
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "figures.json")

# author-list expression (strip parenthetical affiliations, split on comma/"and")
AUTH = (r"list_filter(regexp_split_to_array(regexp_replace(authors,'\([^)]*\)','','g'),"
        r"',|\s+and\s+'), x -> trim(x) <> '')")


def main():
    con = duckdb.connect()
    con.execute(f"SET file_search_path = '{HERE}'")
    con.execute(open(os.path.join(HERE, "setup.sql")).read())
    if glob.glob(os.path.join(HERE, "data", "conf", "*.jsonl")):
        con.execute(open(os.path.join(HERE, "conf_setup.sql")).read())

    def rows(sql):
        r = con.sql(sql)
        cols = [d[0] for d in r.description]
        return [dict(zip(cols, row)) for row in r.fetchall()]

    fig = {}

    # ---- Figure 1a: raw growth in submissions across all of arXiv ----
    fig["f1a"] = rows("""
        SELECT year, count(*) AS papers
        FROM papers_enriched WHERE year BETWEEN 1991 AND 2025
        GROUP BY year ORDER BY year""")

    # ---- Figure 1b: relative distribution across major subjects (stacked) ----
    fig["f1b_groups"] = ['Computer Science','Physics','Mathematics','Statistics',
        'Elec Eng & Systems','Quantitative Biology','Economics','Quantitative Finance',
        'Other/Physics-misc']
    fig["f1b"] = rows("""
        SELECT year, subject_group, count(*) AS papers
        FROM papers_enriched WHERE year BETWEEN 1991 AND 2025
        GROUP BY year, subject_group ORDER BY year""")

    # ---- Figure 2: author-count buckets {1, 2-3, 4-5, 6-8, 9+} ----
    # (last bucket is >8; the given "8+"/"6-8" overlap is resolved non-overlapping)
    fig["f2_buckets"] = ['1','2-3','4-5','6-8','9+']
    fig["f2"] = rows("""
        SELECT year,
          count(*) FILTER (WHERE author_count=1)             AS "1",
          count(*) FILTER (WHERE author_count BETWEEN 2 AND 3) AS "2-3",
          count(*) FILTER (WHERE author_count BETWEEN 4 AND 5) AS "4-5",
          count(*) FILTER (WHERE author_count BETWEEN 6 AND 8) AS "6-8",
          count(*) FILTER (WHERE author_count > 8)           AS "9+"
        FROM papers_enriched WHERE year BETWEEN 1991 AND 2025 AND author_count>0
        GROUP BY year ORDER BY year""")

    # ---- Figure 2b: papers by number of authors, CS only ----
    fig["f2cs_buckets"] = ['1','2-3','4-5','6-8','9+']
    fig["f2cs"] = rows("""
        SELECT year,
          count(*) FILTER (WHERE author_count=1)             AS "1",
          count(*) FILTER (WHERE author_count BETWEEN 2 AND 3) AS "2-3",
          count(*) FILTER (WHERE author_count BETWEEN 4 AND 5) AS "4-5",
          count(*) FILTER (WHERE author_count BETWEEN 6 AND 8) AS "6-8",
          count(*) FILTER (WHERE author_count > 8)           AS "9+"
        FROM papers_enriched
        WHERE year BETWEEN 2000 AND 2025 AND author_count>0 AND primary_category LIKE 'cs.%'
        GROUP BY year ORDER BY year""")

    # ---- Figure 3: top-5 CS sub-disciplines in 2026, tracked over time ----
    top5 = [r["primary_category"] for r in rows("""
        SELECT primary_category, count(*) c FROM papers_enriched
        WHERE primary_category LIKE 'cs.%' AND year=2025
        GROUP BY 1 ORDER BY c DESC LIMIT 5""")]
    fig["f3_cats"] = top5
    inlist = ",".join(f"'{c}'" for c in top5)
    fig["f3"] = rows(f"""
        SELECT year, primary_category, count(*) AS papers
        FROM papers_enriched
        WHERE primary_category IN ({inlist}) AND year BETWEEN 2010 AND 2025
        GROUP BY year, primary_category ORDER BY year""")

    # ---- Figures 4 & 5: CS per-author annual output ----
    con.execute(f"""
        CREATE TEMP TABLE cs_annual AS
        WITH ev AS (
            SELECT trim(a) AS author, year
            FROM papers_enriched, UNNEST({AUTH}) AS t(a)
            WHERE primary_category LIKE 'cs.%' AND year BETWEEN 1991 AND 2025
              AND trim(a) <> ''
        )
        SELECT author, year, count(*) AS n FROM ev GROUP BY author, year""")

    # Fig 4: mean / std / median of annual output, per year
    fig["f4"] = rows("""
        SELECT year, round(avg(n),3) AS mean, round(stddev_samp(n),3) AS std,
               median(n) AS median, count(*) AS active_authors
        FROM cs_annual WHERE year BETWEEN 2005 AND 2025
        GROUP BY year ORDER BY year""")

    # Fig 5: same annual output, split by cumulative career-total bucket
    # buckets {1, 2-3, 4-8, 9-20, 21+} (non-overlapping resolution of 8-20/20+)
    fig["f5_buckets"] = ['1','2-3','4-8','9-20','21+']
    fig["f5"] = rows("""
        WITH cum AS (
            SELECT author, year, n,
                   sum(n) OVER (PARTITION BY author ORDER BY year) AS total
            FROM cs_annual
        ), b AS (
            SELECT year, n,
                CASE WHEN total=1 THEN '1'
                     WHEN total BETWEEN 2 AND 3 THEN '2-3'
                     WHEN total BETWEEN 4 AND 8 THEN '4-8'
                     WHEN total BETWEEN 9 AND 20 THEN '9-20'
                     ELSE '21+' END AS bucket
            FROM cum
        )
        SELECT year, bucket, round(avg(n),3) AS mean_output, count(*) AS author_years
        FROM b WHERE year BETWEEN 2005 AND 2025
        GROUP BY year, bucket ORDER BY year""")

    # ==== Mathematics — mirror of the CS figures (8-11) ====
    fig["m2_buckets"] = ['1','2','3','4','5','6+']
    fig["m2"] = rows("""
        SELECT year,
          count(*) FILTER (WHERE author_count=1) AS "1",
          count(*) FILTER (WHERE author_count=2) AS "2",
          count(*) FILTER (WHERE author_count=3) AS "3",
          count(*) FILTER (WHERE author_count=4) AS "4",
          count(*) FILTER (WHERE author_count=5) AS "5",
          count(*) FILTER (WHERE author_count>5) AS "6+"
        FROM papers_enriched
        WHERE year BETWEEN 2000 AND 2025 AND author_count>0 AND primary_category LIKE 'math.%'
        GROUP BY year ORDER BY year""")
    mtop5 = [r["primary_category"] for r in rows("""
        SELECT primary_category, count(*) c FROM papers_enriched
        WHERE primary_category LIKE 'math.%' AND year=2025
        GROUP BY 1 ORDER BY c DESC LIMIT 5""")]
    fig["m3_cats"] = mtop5
    minlist = ",".join(f"'{c}'" for c in mtop5)
    fig["m3"] = rows(f"""
        SELECT year, primary_category, count(*) AS papers FROM papers_enriched
        WHERE primary_category IN ({minlist}) AND year BETWEEN 2010 AND 2025
        GROUP BY year, primary_category ORDER BY year""")
    con.execute(f"""
        CREATE TEMP TABLE math_annual AS
        WITH ev AS (
            SELECT trim(a) AS author, year
            FROM papers_enriched, UNNEST({AUTH}) AS t(a)
            WHERE primary_category LIKE 'math.%' AND year BETWEEN 1991 AND 2025 AND trim(a)<>''
        )
        SELECT author, year, count(*) AS n FROM ev GROUP BY author, year""")
    fig["m4"] = rows("""
        SELECT year, round(avg(n),3) AS mean, round(stddev_samp(n),3) AS std,
               median(n) AS median, count(*) AS active_authors
        FROM math_annual WHERE year BETWEEN 2005 AND 2025 GROUP BY year ORDER BY year""")
    fig["m5_buckets"] = ['1','2-3','4-8','9-20','21+']
    fig["m5"] = rows("""
        WITH cum AS (
            SELECT author, year, n, sum(n) OVER (PARTITION BY author ORDER BY year) AS total
            FROM math_annual
        ), b AS (
            SELECT year, n,
                CASE WHEN total=1 THEN '1' WHEN total BETWEEN 2 AND 3 THEN '2-3'
                     WHEN total BETWEEN 4 AND 8 THEN '4-8' WHEN total BETWEEN 9 AND 20 THEN '9-20'
                     ELSE '21+' END AS bucket
            FROM cum
        )
        SELECT year, bucket, round(avg(n),3) AS mean_output, count(*) AS author_years
        FROM b WHERE year BETWEEN 2005 AND 2025 GROUP BY year, bucket ORDER BY year""")

    # ---- Figure 16: first-author papers per person (LLM control, deep history) ----
    # Controls for team-size growth by counting only first-authorships. Flat
    # pre-2023 baseline; watch for a post-ChatGPT uptick.
    fig["faperson"] = rows(f"""
        WITH base AS (
          SELECT lower(trim(list_extract({AUTH}, 1))) AS fa, year, primary_category
          FROM papers_enriched WHERE year BETWEEN 2005 AND 2025 AND authors IS NOT NULL
        ),
        a AS (SELECT year, fa, count(*) n FROM base WHERE fa<>'' GROUP BY year, fa),
        c AS (SELECT year, fa, count(*) n FROM base WHERE fa<>'' AND primary_category LIKE 'cs.%' GROUP BY year, fa),
        m AS (SELECT year, fa, count(*) n FROM base WHERE fa<>'' AND primary_category LIKE 'math.%' GROUP BY year, fa)
        SELECT y.year,
          (SELECT round(avg(n),3) FROM a WHERE a.year=y.year) AS all_fields,
          (SELECT round(avg(n),3) FROM c WHERE c.year=y.year) AS cs,
          (SELECT round(avg(n),3) FROM m WHERE m.year=y.year) AS math
        FROM (SELECT DISTINCT year FROM base) y ORDER BY y.year""")

    # ---- Figure 6: region (China / US / Other), conference submissions ----
    if "conf_paper_region" in [r["name"] for r in rows("SHOW TABLES")]:
        fig["f6"] = rows("""
            SELECT year,
              count(*) FILTER (WHERE majority_region='China') AS china,
              count(*) FILTER (WHERE majority_region='US')    AS us,
              count(*) FILTER (WHERE majority_region='Other') AS other
            FROM conf_paper_region WHERE year BETWEEN 2021 AND 2025
            GROUP BY year ORDER BY year""")

        # Figure 7: FIRST-AUTHOR seniority of submissions, finest grain
        # (year x venue x region x seniority) so the page can filter/aggregate.
        # Each paper counts once, by its first author's self-reported position.
        fig["f7_order"] = ['PhD student','Junior student (MS/UG)','Postdoc','Faculty',
            'Researcher (unspecified)','Industry/research staff','Other']
        fig["fa"] = rows("""
            SELECT year, venue, region, seniority, count(*) AS n
            FROM conf_authors
            WHERE author_no = 1 AND seniority <> 'Unknown' AND year BETWEEN 2021 AND 2025
            GROUP BY year, venue, region, seniority ORDER BY year""")
        # all-author-instances basis (every authorship counted, incl. PIs on
        # many papers) — the earlier metric; kept alongside first-author.
        fig["fa_all"] = rows("""
            SELECT year, venue, region, seniority, count(*) AS n
            FROM conf_authors
            WHERE seniority <> 'Unknown' AND year BETWEEN 2021 AND 2025
            GROUP BY year, venue, region, seniority ORDER BY year""")

        # Figure 7c: NEW PhD-student first-authors per year, by region.
        # debut = first year a profile appears as a PhD-student first author
        # (proxy for new publishing PhD students). 2021 is left-censored.
        fig["newphd"] = rows("""
            WITH p AS (
              SELECT or_profile, year, region FROM conf_authors
              WHERE author_no=1 AND seniority='PhD student' AND or_profile<>''
                AND region IN ('China','US','Other')
            ), deb AS (
              SELECT or_profile, min(year) AS debut, arg_min(region, year) AS region
              FROM p GROUP BY or_profile
            )
            SELECT debut AS year, region, count(*) AS n
            FROM deb GROUP BY debut, region ORDER BY year""")

        # Figure 7d: mean/median submissions per person per year, by seniority.
        # subs = distinct papers a profile is an author on that year.
        fig["f7d"] = rows("""
            WITH pp AS (
              SELECT year, seniority, or_profile, count(DISTINCT id) AS subs
              FROM conf_authors WHERE or_profile<>'' AND seniority<>'Unknown'
                AND year BETWEEN 2021 AND 2025
              GROUP BY year, seniority, or_profile
            )
            SELECT year, seniority, round(avg(subs),3) AS mean, median(subs) AS median,
                   count(*) AS people
            FROM pp GROUP BY year, seniority ORDER BY year""")

        # Figure 14: PhD-student output decomposed — headcount, all-authorship
        # per student, and FIRST-AUTHOR-only papers per student.
        fig["phddec"] = rows("""
            WITH s AS (
              SELECT year, or_profile, count(DISTINCT id) AS subs
              FROM conf_authors WHERE seniority='PhD student' AND or_profile<>''
              GROUP BY year, or_profile
            ), sg AS (SELECT year, count(*) AS students, avg(subs) AS pps FROM s GROUP BY year),
            fa AS (
              SELECT year, or_profile, count(DISTINCT id) AS fsub
              FROM conf_authors WHERE author_no=1 AND seniority='PhD student' AND or_profile<>''
              GROUP BY year, or_profile
            ), fag AS (SELECT year, count(*) AS fa_students, avg(fsub) AS faps FROM fa GROUP BY year)
            SELECT sg.year, sg.students, round(sg.pps,3) AS papers_per_student,
                   fag.fa_students, round(fag.faps,3) AS fa_per_student
            FROM sg JOIN fag USING(year)
            WHERE sg.year BETWEEN 2021 AND 2025 ORDER BY sg.year""")

    # ---- Figures 12/13: ICLR acceptance over time (berenslab decisions) ----
    dec = glob.glob(os.path.join(HERE, "data", "iclr_decisions", "*.parquet"))
    if dec:
        best = max(dec, key=lambda p: con.sql(
            f"SELECT count(*) FROM read_parquet('{p}')").fetchone()[0])
        fig["acc"] = rows(f"""
            SELECT year,
              count(*) AS submissions,
              count(*) FILTER (WHERE lower(decision) LIKE 'accept%') AS accepted,
              count(*) FILTER (WHERE lower(decision) LIKE '%reject%') AS rejected,
              count(*) FILTER (WHERE lower(decision) LIKE '%withdraw%'
                 OR (lower(decision) NOT LIKE 'accept%'
                     AND lower(decision) NOT LIKE '%reject%')) AS withdrawn_other
            FROM read_parquet('{best}')
            WHERE year BETWEEN 2017 AND 2025
            GROUP BY year ORDER BY year""")

    # ---- 2026 so far: year-to-date pace vs prior years (same Jan–cutoff window) ----
    cutoff = con.sql("SELECT max(month(first_version_date)) FROM papers "
                     "WHERE year(first_version_date)=2026").fetchone()[0]
    fig["ytd_month"] = cutoff
    fig["ytd"] = rows(f"""
        SELECT year(first_version_date) AS year, count(*) AS ytd_papers,
          count(*) FILTER (WHERE primary_category LIKE 'cs.%') AS ytd_cs
        FROM papers
        WHERE month(first_version_date) <= {cutoff}
          AND year(first_version_date) BETWEEN 2019 AND 2026
        GROUP BY 1 ORDER BY 1""")

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(fig, f, default=float)
    # archive a timestamped copy so every re-run is preserved
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_dir = os.path.join(os.path.dirname(OUT) or ".", "archive")
    os.makedirs(archive_dir, exist_ok=True)
    archive = os.path.join(archive_dir, f"figures-{stamp}.json")
    with open(archive, "w") as f:
        json.dump(fig, f, default=float)
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes); archived -> {archive}")
    for k, v in fig.items():
        print(f"  {k}: {len(v) if isinstance(v, list) else v}")


if __name__ == "__main__":
    main()
