# Who is Writing all Those Papers!?

The code behind the interactive blog post of the same name: who is behind the
surge in submissions to arXiv and the top machine-learning conferences (NeurIPS,
ICML, ICLR)? The whole analysis runs on public **metadata** — we never download
arXiv's 16 TiB full-text corpus, only the ~1.6 GB metadata config.

The post is an interactive [distill.pub](https://distill.pub)-style page built
from a DuckDB pipeline. You edit Markdown and a figure library; one command
rebuilds the page.

## Read the post

```bash
make            # builds distill/index.html
open distill/index.html
```

The page is self-contained and works offline (it does fetch the distill
framework and fonts from a CDN, like the live blog). It is **generated, so it is
not committed** — run `make` to produce it. Building from a fresh clone needs the
data first; see [Reproduce](#reproduce-from-scratch).

## What it finds

- Before 2026, arXiv's exponential growth tracks the exponential growth in the
  number of CS PhD students, not LLM use and not solo authors.
- First-author papers per person barely moved after ChatGPT. The rise in papers
  per person comes from longer author lists, i.e. more collaboration.
- 2026 breaks the pattern: a real jump in solo-authored papers, especially in
  CS. Most of it comes from established authors (about 88% of the CS excess).
- China is adding PhD-student authors far faster than the US and is on track to
  overtake it around 2027.

Numbers are directional, not causal; the post's **Methods & data** section and
[`AGENTS.md`](AGENTS.md) spell out the definitions and caveats.

## Edit the post

Three files, then `make` to rebuild:

- [`distill/post.md`](distill/post.md) — the prose. Front-matter (title,
  subtitle, authors, date) then Markdown. Drop a figure with a token on its own
  line, `{{fig:SLUG}}`, and cite its number in text with `{{figref:SLUG}}`.
  Figures are numbered by the order they appear here.
- [`distill/figures.md`](distill/figures.md) — each figure's heading and
  caption. No numbers; those are assigned at build time.
- `distill/template.html` — the figure library: one `<figure>` per chart plus
  the script that draws them (Chart.js + d3).

Run `make` and reload the page. Don't hand-edit `distill/index.html`; it is
overwritten on every build.

## Reproduce from scratch

```bash
make setup      # create .venv and install deps (Python 3.9+)
make data       # download the input datasets (~1.7 GB, not committed)
make            # compute results/figures.json, then build distill/index.html
```

| Dataset | What | Fetched by |
|---|---|---|
| [secemp9/arxiv-complete](https://huggingface.co/datasets/secemp9/arxiv-complete) (`metadata` config) | 3.15M arXiv papers (Cornell/CC0) | `scripts/download_data.py` |
| [Paper Copilot](https://papercopilot.com) OpenReview archive ([arXiv:2510.13201](https://arxiv.org/abs/2510.13201)) | NeurIPS/ICML/ICLR author affiliations | `scripts/download_conf_data.py` |
| berenslab/iclr-dataset | ICLR submissions incl. rejected + decisions | `scripts/download_iclr_decisions.py` |

Input data is git-ignored and re-downloaded by the scripts; nothing under
`data/` is committed. To explore the metadata directly, `scripts/run.py` is a
DuckDB shell: `.venv/bin/python scripts/run.py -f sql/queries/01_growth_by_year.sql`.

## For coding agents

Read [`AGENTS.md`](AGENTS.md) first. It covers the build pipeline, how figures
and numbering work, the methodology and caveats, and the hard rules (never
download the full corpus; never hand-edit the generated page).

## Repo layout

```
distill/      the post: post.md (prose), figures.md (captions),
              template.html (charts + render script), world.geo.json (basemap);
              index.html is the built page (generated, git-ignored)
scripts/      build_figures.py (-> results/figures.json),
              build_post.py (-> distill/index.html), build_geo.py,
              download_*.py (fetch the datasets), run.py (DuckDB shell)
sql/          setup.sql + conf_setup.sql (DuckDB views), queries/ (ad-hoc SQL)
results/      computed figure data (generated, git-ignored)
AGENTS.md     orientation for coding agents
```

## Requirements

Python 3.9+ and `duckdb` (`pip install -r requirements.txt`). Git LFS is set up
for any self-collected data, though all current inputs are external. MIT
licensed (see [`LICENSE`](LICENSE)).
