# AGENTS.md — working in this repo

Orientation for coding agents. Human-facing overview is in `README.md`.

## What this is

An interactive [distill](https://distill.pub)-style blog post answering: who is
behind the rise in arXiv and ML-conference (NeurIPS · ICML · ICLR) submissions?
It is built from public **metadata** with a DuckDB → JSON → HTML pipeline.

The published artifact is `distill/index.html` (self-contained, interactive).

## Hard constraints

- **Never download arXiv's full-text corpus (~16 TiB).** Use only the ~1.6 GB
  metadata config (`secemp9/arxiv-complete`). All analysis is metadata-only.
- **Never hand-edit `distill/index.html`** — it is generated. Edit the sources
  and rebuild. The rendered page and `results/` (figures.json + archive) are
  **git-ignored, not committed**; `make` regenerates them. `distill/world.geo.json`
  is the exception: a committed static basemap (a build *input*, not output).
- DuckDB runs memory-capped (`memory_limit`, `threads=2`,
  `preserve_insertion_order=false`, `temp_directory='.duckdb_tmp'`); keep it
  capped — the machine has limited RAM.
- `data/` is git-ignored and re-downloaded by the `download_*.py` scripts; don't
  commit data. Self-collected data goes through Git LFS.

## Build pipeline

```
scripts/download_*.py  ->  data/        (external datasets, not committed)
sql/setup.sql, sql/conf_setup.sql        (DuckDB views over the parquet/json)
scripts/build_figures.py  ->  results/figures.json  (+ results/archive/)
scripts/build_post.py     ->  distill/index.html
```

- `make setup` — venv + deps. `make data` — download (~1.7 GB). `make figures` —
  recompute `results/figures.json`. `make post` — rebuild the page. `make all` —
  figures + post. The data is already present under `data/` in this workspace.
- Rebuild the page after editing prose or figures: `python3 scripts/build_post.py`.
- `scripts/run.py` is an ad-hoc DuckDB shell: `python3 scripts/run.py -f sql/queries/01_growth_by_year.sql`.

## The figure system (read before touching figures or numbers)

Three sources, one build step. **Figure numbers are computed, never stored.**

- **`distill/post.md`** — the prose (Markdown + YAML front-matter). Place a
  figure with a token on its own line, `{{fig:SLUG}}`; reference one in prose
  with `{{figref:SLUG}}`. The figure's number is its **order of first
  appearance in `post.md`** — this is the single source of truth for numbering.
- **`distill/figures.md`** — each figure's heading and caption, as
  `## fig:SLUG — Heading` followed by the caption lines. No numbers here.
- **`distill/template.html`** — the figure *library*: one `<figure>` block per
  figure (tagged `data-fig="SLUG"`) plus a single runtime `<script>` that draws
  every chart (Chart.js + d3). No numbers, no prose, no comments.
- **`build_post.py`** — assembles them: injects only the referenced figures,
  assigns `Figure N` from post order, resolves `{{figref:SLUG}}`, applies the
  `figures.md` heading/caption, inlines `figures.json` + Chart.js, emits a real
  distill page (`<d-article>` etc.).

`SLUG` is an opaque token shared by all three files (e.g. `arxiv-growth`,
`subs-per-person`, `worldmap`); it is **not** a figure number. A figure's chart
is drawn into a canvas/container id inside its `<figure>` block — some figures
reuse ids like `f5`/`f11` across subplots, so when editing the runtime script,
check which canvas ids a kept figure actually contains.

Colormap: every chart uses the first 80% of d3's plasma (`BL(t)` in the runtime
script); keep new charts on it for consistency.

## Verify changes

Build, then headless-render and check for JS errors and that charts drew:

```bash
python3 scripts/build_post.py
"<chrome>" --headless=new --disable-gpu --virtual-time-budget=7000 \
  --enable-logging=stderr "file://$PWD/distill/index.html" 2>&1 | grep -i 'Uncaught\|TypeError'
```

A clean build prints `12 figures` and no warnings; the render should log no
`Uncaught`/`TypeError`. The distill framework loads from distill.pub, so a real
browser (or headless Chrome) is needed — not the claude.ai sandbox.

## Methodology & caveats (these drive the analysis; preserve them)

- **No unique author ids.** Authors are parsed from the raw `authors` display
  string: strip a trailing `((1) affil …)` block and inline `(…)` parentheses,
  drop `et al`, split on `,` and ` and `. Common names (e.g. "Yang Liu") conflate
  many people, so arXiv author-level numbers are **directional, not exact**. The
  appendix in `post.md` lists the most common name strings.
- **Author count** = length of that parse. **Solo** = count 1. **Seniority** is
  proxied by career-total papers (cumulative); **established** ≈ ≥4 career
  papers, **novice** otherwise.
- **PhD-student proxy**: authors self-reporting "PhD student" in the OpenReview
  conference files; "new" PhD students = first year a name appears.
- **YTD cutoff** for 2026 comparisons: Jan 1–Aug 27, applied to *every* year so
  years are comparable (`month<8 OR (month=8 AND day<=27)`).
- **Excess** = actual − projection from each cell's **own** exponential trend
  (log-linear fit), i.e. growth beyond the already-exponential trend — not raw
  year-over-year change.
- Conference seniority convention (last author = senior) is a CS norm, not a
  rule; treat region/seniority splits as directional.

## Conventions

- Keep code comment-free; document rationale here or in `README.md` instead.
- Keep reproduction code intact (`scripts/build_figures.py`, `sql/queries/`,
  `sql/setup.sql`, `sql/conf_setup.sql`, `scripts/download_*.py`,
  `scripts/run.py`) so the post stays exactly reproducible from scratch.
- `distill/post.md` prose is the authors' own writing — fix typos, but don't
  rewrite voice or inject exposition unless asked.
