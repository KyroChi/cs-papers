# Who Fills arXiv — cs-papers

Who is behind the dramatic rise in papers on arXiv and at the top machine-learning
conferences (NeurIPS · ICML · ICLR)? This repo builds an interactive
[distill](https://distill.pub)-style document from public metadata — **without
downloading arXiv's 16 TiB corpus** (we use only the ~1.6 GB metadata config).

**→ The document lives in [`distill/index.html`](distill/index.html)** — a
self-contained interactive page (open it in any browser, works offline). If
GitHub Pages is enabled for this repo, it is served at
`https://kyrochi.github.io/cs-papers/distill/`.

**Writing it:** [`distill/post.md`](distill/post.md) has a YAML front-matter
block (title, subtitle, authors, published, disclaimer) followed by plain
Markdown. Drop any figure with a token on its own line, e.g. `{{fig:7f}}`.
Rebuild with `make post`. `build_post.py` emits a genuine
[distill.pub](https://distill.pub) article (`<d-title>`/`<d-byline>`/`<d-article>`,
`template.v2.js` + MathJax), injects the referenced figures (interactive
Chart.js from `distill/template.html`), and inlines the latest data + Chart.js.
Figures you don't reference aren't shown.

**Viewing:** open `distill/index.html` in a browser (`open distill/index.html`)
or publish via GitHub Pages — both load the distill framework. Needs network
for `template.v2.js`/MathJax, like the blog itself.

## Findings in brief

- arXiv submissions grew **~9× since 2000** (≈31k → ≈284k in 2025) and are still accelerating.
- The rise is driven by **Computer Science** — specifically the AI/ML subfields — and by **teams, not solo authors**.
- At the top ML venues, **China's submission share rose steeply** (~13% → ~23% by 2025), driven mainly by a **~9× rise in the number of PhD-student first authors** — not students each writing more.
- Peer review **kept pace**: ICLR's acceptance rate held ~30–32% while submissions grew ~24×.
- The surge is **not primarily an LLM artifact**: even crediting the entire post-2022 per-person uptick to LLMs, that explains ≤ ~10–13% of recent CS growth; the rest is more people.

See the document's **Methods & data** section for definitions and caveats. All
findings are directional, not causal.

## Reproduce

```bash
make setup     # create .venv and install deps (needs Python 3.9+)
make data      # download external data (~1.7 GB, not committed)
make all       # compute results/figures.json and build distill/index.html
```

Or step by step:

```bash
.venv/bin/python download_data.py            # arXiv metadata (1.6 GB parquet)
.venv/bin/python download_conf_data.py       # NeurIPS/ICML/ICLR author files (~70 MB)
.venv/bin/python download_iclr_decisions.py  # ICLR accept/reject decisions
.venv/bin/python build_figures.py            # -> results/figures.json (+ archive/)
.venv/bin/python build_post.py               # distill/post.md + figures -> distill/index.html
```

Ad-hoc querying (DuckDB SQL over the metadata): `.venv/bin/python run.py -f queries/01_growth_by_year.sql`, or `run.py "<sql>"`, or `run.py` for a shell.

## Data

| Source | What | How to get it | Committed? |
|---|---|---|---|
| [secemp9/arxiv-complete](https://huggingface.co/datasets/secemp9/arxiv-complete) (`metadata` config) | 3.15M arXiv papers, Cornell/CC0 | `download_data.py` | No — re-download |
| Paper Copilot OpenReview archive ([arXiv:2510.13201](https://arxiv.org/abs/2510.13201)) | NeurIPS/ICML/ICLR author affiliations | `download_conf_data.py` | No — re-download |
| berenslab/iclr-dataset | ICLR submissions incl. rejected + decisions | `download_iclr_decisions.py` | No — re-download |

**Policy:** external data is git-ignored and re-downloaded with the scripts. Any
data we collect ourselves is versioned with **Git LFS** (see `.gitattributes`);
install it once with `git lfs install`. Currently all inputs are external, so no
LFS objects are stored yet.

## How the findings flow

`build_figures.py` runs the DuckDB queries (capped at ≤1 GiB RAM, spilling to
disk) and writes **`results/figures.json`** (the latest findings), plus a
timestamped copy in **`results/archive/`** so every re-run is preserved.
`build_post.py` renders `distill/post.md`, injects the referenced figures from
`distill/template.html`, and inlines the *latest* `results/figures.json` +
Chart.js into `distill/index.html`. So: `make figures` after new data, `make
post` after editing prose, or `make all` for both.

## Layout

```
distill/post.md      the prose (Markdown; edit this) with {{fig:ID}} tokens
distill/template.html figure library + render code (interactive Chart.js blocks)
distill/index.html   built, self-contained page (do not hand-edit)
results/             figures.json (latest findings) + archive/ (per-run history)
queries/             standalone DuckDB SQL for the arXiv metadata questions
setup.sql            DuckDB views over the arXiv parquet
conf_setup.sql       DuckDB views over the conference author files
build_figures.py     compute all figure aggregates (memory-capped)
build_post.py        Markdown prose + figures -> distill/index.html
build_html.py        render template.html directly (all figures, for previewing)
run.py               ad-hoc SQL runner / shell
download_*.py        fetch the external datasets
```

## Requirements

Python 3.9+, `duckdb` (`pip install -r requirements.txt`), and `git-lfs` for
contributing self-collected data. MIT licensed (see `LICENSE`).
