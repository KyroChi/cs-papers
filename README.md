# Who is driving the growth of arXiv?

Querying the metadata of **3.15M arXiv papers** to ask who is behind the
dramatic rise in submissions: solo authors or teams? which fields? early-career
researchers?

We do this **without downloading 16 TiB**. The full
[`secemp9/arxiv-complete`](https://huggingface.co/datasets/secemp9/arxiv-complete)
dataset bundles PDFs and LaTeX source, but it exposes a separate `metadata`
config — a single **1.6 GB parquet** with every field we need. We fetch only
that and query it locally with [DuckDB](https://duckdb.org).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python download_data.py                       # ~1.6 GB, metadata only
python run.py -f queries/01_growth_by_year.sql
python run.py                                 # interactive SQL shell
python run.py "SELECT count(*) FROM papers"   # or inline SQL
```

`setup.sql` builds two views, recreated on every run:
- **`papers`** — raw rows (title, authors, categories, primary_category,
  first_version_date, n_versions, comments, ...).
- **`papers_enriched`** — adds `year`, `author_count` (proxy), and a coarse
  `subject_group`.

## The queries

| File | Question |
|---|---|
| `queries/01_growth_by_year.sql` | Papers per year + YoY growth (the baseline) |
| `queries/02_solo_vs_group.sql` | Share of solo vs 2-3 / 4-6 / 7-10 / 11+ author papers |
| `queries/03_team_size_trend.sql` | Mean & median authors per paper over time |
| `queries/04_growth_by_subject.sql` | Growth by subject group and top categories |
| `queries/05_new_author_influx.sql` | First-time authors per year (early-career proxy) |
| `queries/06_decompose_the_surge.sql` | How much of the increase each field / team size added |
| `queries/07_last_author_seniority.sql` | CS last-author (senior) career age & output, by year and team size |
| `queries/08_affiliations_besteffort.sql` | Parenthetical affiliation tags — *documents why institution analysis fails here* |

## What the data says

Numbers below are from the Aug 2026 snapshot (2026 is partial/year-to-date).

**Submissions are accelerating.** ~30k papers in 2000 → 105k in 2015 → **284k in
2025**, with the fastest growth in the most recent years (+16% in both 2024 and
2025).

**The growth is teams, not solo authors.** Solo-authored papers fell from **44%
of arXiv in 1991 to ~11% in 2025**. Median authors per paper rose from 2 to 4;
the mean from under 2 to 6.3. In the last decade, papers with 4-6 authors added
the most volume of any team size.

**Computer Science is the engine.** CS went from **27 papers in 1995 to 128,856
in 2025**, overtaking physics to become the largest group. Of the ~180k papers
added per year between the mid-2010s and 2025, **CS accounts for the majority**
(≈113k of the added total), with EESS (signal processing / ML-adjacent) the
fastest-growing on a percentage basis.

**A widening base of new authors.** ~236k distinct author names *debuted* on
arXiv in 2025 alone, up from ~64k in 2010 — consistent with the surge being
fueled by a constantly expanding population of new (largely early-career)
researchers.

**CS growth is senior-led, i.e. labs.** In CS the last author is conventionally
the PI. Their median career age (years on arXiv) rose from ~0 in 2000 to **9
years in 2025**, while the share of papers whose last author is a first-timer
fell from 65% to ~12%. And seniority scales with team size: solo CS papers have
a median last-author career of 3 years / 8 papers; 7-10-author papers, **9 years
/ 72 papers**. The picture is established PIs running progressively larger groups
— consistent with growth driven by lab teams (senior author + more students).

### Institutions — not answerable from this metadata

Emails are stripped (71 of 3.1M author strings have an `@`) and there is no
affiliation field. Parenthetical lab tags exist for only ~2-6% of papers, are
mostly footnote markers (`1`, `2`), and skew heavily to one region — so
`queries/08` exists to *demonstrate* the dead-end, not to draw conclusions. For
real institution analysis, enrich by arXiv ID via **OpenAlex** or **Semantic
Scholar** (both expose affiliations through free APIs) — still no PDFs needed.

### The PhD-student question — read this caveat

Metadata has **no seniority or affiliation-role field**, so "is it PhD
students?" can't be answered directly. Query 05 uses *first appearance of an
author name* as an early-career proxy. Two limits:
- **Name collisions.** Initials merge distinct people ("Y. Wang" is thousands of
  authors), inflating some counts and undercounting debuts.
- **Author-count is a proxy too.** We split the raw `authors` string on commas
  and "and"; a named collaboration ("ATLAS Collaboration") counts as one author.

Treat the early-career findings as **directional**, not precise. For rigorous
seniority analysis you'd need author disambiguation (e.g. ORCID, Semantic
Scholar, or arXiv author IDs) — a possible next step, still without any PDFs.

## Data & licensing

- Data is **not** committed (see `.gitignore`); run `download_data.py` to fetch
  it. Source: `secemp9/arxiv-complete` on Hugging Face. arXiv metadata is
  distributed by Cornell under CC0.
- This code is released under the MIT License (see `LICENSE`).
