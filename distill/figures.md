# Figure headings & captions

Edit figure **headings** and **captions** here — this file overrides whatever is
written in `template.html` at build time.

- Each figure is a section beginning `## fig:ID — Heading`.
- `ID` is an opaque token (e.g. `17`, `7f`, `worldmap`) that links this caption
  to the chart in `template.html` and the `{{fig:ID}}` tag in `post.md`. The
  digits in it are **not** a figure number — they're just part of the name.
- The figure's displayed number is assigned automatically from the order
  figures appear in `post.md`, so no number is written anywhere in this file.
- The text after the `—` is the heading (shown bold after "Figure N.").
- The lines under the heading, up to the next `## fig:`, are the caption (the
  smaller grey sub-line). Leave them blank for no caption.
- `**bold**` and raw `<b>…</b>` both work in captions.

Rebuild after editing:  `python3 build_post.py`

<!-- Sections are in the order figures currently appear in post.md. -->

## fig:conferences-and-phds — Big-3 submissions and the number of PhD-students
Left: papers submitted to NeurIPS, ICML, ICLR per year. Right: unique authors listing themselves as "PhD student" per year.

## fig:subs-per-person — Mean submissions per person per year, by seniority
Average papers per person in each self-reported position.

## fig:authors-per-conf-paper — Authors per paper at the big-3
Authors per paper at the big-3 (NeurIPS · ICML · ICLR, 2021–2025): mean (dot) with 25th–75th-percentiles as candles.

## fig:region-growth — Region growth and share
Left: submission growth indexed to 2021. Right: share of submissions by region.

## fig:worldmap — Unique PhD-student authors by country
Distinct authors listing themselves as "PhD student", by institution country (determined from email domains), per year. Colour = value on a log scale, **dark purple = lowest, bright orange = highest** (grey = no data). For the range, raw count sums 2021–2025. 

## fig:new-phds-by-region — New PhD-student first-authors per year, by region
First year each PhD-student profile appears as a first author.

## fig:arxiv-growth — Growth in submissions across all of arXiv
Papers by year of submission, 1991–2025.

## fig:subject-shares — Relative distribution of papers across major arXiv subjects


## fig:author-list-sizes — Papers by number of authors


## fig:sen — Annual output by career total — CS (left) vs Mathematics (right)
Mean papers/year, with authors bucketed by cumulative papers to date.

## fig:tenure — Are the 31+ solo authors veterans or newcomers?
Years since first-ever arXiv submission for 2026 solo authors with 31+ career papers. 

## fig:ridge — Distribution of years on the arXiv based on number of papers
Each row represents authors with that number of papers, and we plot the distribution of the years active on arXiv for authors with that many papers.
