---
title: Who Fills arXiv
subtitle: An interactive look at the growth of arXiv and the machine-learning conferences.
description: Who is behind the surge in arXiv and ML-conference submissions?
published: September 2026
disclaimer: This post reflects the personal views of the authors and not those of their employer.
authors:
  - name: Kyle Chickering
    url: https://kyrochi.github.io/
  - name: Dario Sučić
---

<!--
  Write prose in plain Markdown. Insert any figure with a token on its own line:
      {{fig:7f}}
  Available figure ids:
    1a 1b 1c 2 2cs 3 4 5            (arXiv overall + CS)
    6a 6b 6c 7 7c 7d 7e 7f          (conferences: region + seniority)
    8 9 10 11                       (mathematics)
    12 13                           (ICLR peer review)
    14a 14b 15 16                   (decomposition, 2026 YTD, LLM control)
  Rebuild with:  make post   (or  .venv/bin/python build_post.py )
  Only the figures you reference are shown.
-->

More than 60 thousand papers were submitted to ICLR in 2026 [LINK]. Naturally the association between the rise of LLMs and this increase in paper submissions is conspicuous. We asked each other a simple question: "Who are writing all of these papers!?".

Our initial hypothesis was that LLM assistance was leading to a dearth of solo-authored papers from non-affiliated researchers. Our follow-up question was then: "how are these researchers getting referrals for the arXiv?"

We set out to answer these questions by using metadata from arXiv, NeurIPS, ICLR, and ICML. What we found surprised us, although upon reflection this is not so surprising:

> The exponential growth in submitted papers tracks nearly perfectly an exponential growth in computer science PhD students in the United States and China. LLM assistance has not materially impacted the share of submissions from solo-authors. Most surprising of all, the introduction of LLM tools in 2022 has not increased the per-capita research productivity of PhD students (measured in first-author papers per year). Most surprising of all is that paper output by senior mathematicians has been steadily declining over the last two decades, and LLM use has not cause a boom in per-capita paper submissions. 

The remainder of this blog post walks through our findings with empirical support from our collected metadata datasets which are built on top of the excellent open source metadata datasets by ... We discuss our dataset collection and curation in the appendix. 

We conclude with some brief thoughts on the situation that computer science, and research in general, finds itself in.

# Who Submits to the Big-3 ML Conferences?

**Main Findings:**
- The vast majority of the exponential growth in submitted papers can be attributed to an exponential growth in the number of CS PhD students.
- First author papers per-capita has barely changed since the advent of LLM assistance. We conclude that LLM tools have not materially changed the number of papers PhD students are writing.
- The average papers submitted per-capita has risen. This reflects a trend towards larger author lists and increased collaboration. 

## An Exponential Growth in PhD Students
Our primary finding is that the exponential growth in papers (See Figure 17, left) is driven by a concomitant growth in the raw number of PhD students studying computer science (See Figure 17, right). In the period of time between 2021 and 2025, our data indicate that submissions to NeurIPS grew by $4.0\times$, from 2,708 to 10,761. ICLR submissions grew by $4.5\times$, from 3,014 in 2021 to 13,697 in 2025. During that same period of time, the number of unique PhD authors submitting to these conferences grew by $4.5\times$, from 3,938 in 2021 to 17,881 in 2025. ICLR submissions in particular have grown at the exact same rate as the growth in the number of PhD students!

{{fig:17}}

## LLM Use is Not Explanatory

This already suggests that LLM assistence may not be a significant contributing factor to the rise in paper submissions. We can provide further evidence in support of this conclusion by tracking the increase in first-author papers per-capita, sub-divided by seniority. Figure 7f shows that the mean first author submissions per-person per-year has risen between 2021 and 2025, but only modestly, from 0.721 to 0.768. 

{{fig:7f}}

When we look at submissions per-person per-year (i.e. not only first authorship), there is a notable increase in in submissions for **both** faculty and PhD students. Perhaps LLM use is increasing research lab's inclusion of lab-mates on the authorship list. However we think it is much more likely that the increase in PhD students is nearly fully explanatory in this case as well, and the fact that the number of CS PhD students began to take off in 2022 is a conincidence, although almost certainly a coincidence spurned by the introduction of chatGPT. This is clearly reflected in the data (see Figure 7g). Between 2021 and 2025 the mean number of authors per paper has risen from 4.3 to 5.3, a full additional author per paper, on average. 

{{fig:7g}}

## PhD Student Growth by Region

{{fig:6cb}}

{{fig:worldmap}}

The rate at which PhD students is being added has a clear geographic bias.

- US and China are dominating the growth of PhD students
- The rate of Chinese growth is outpacing the United States


# arXiv Submissions Have Been Increasing Exponentially
We now turn to analyzing trends based on arXiv metadata. The arXiv data is richer on the one hand since it spans multiple disciplines and has a larger share of historical data. On the other hand, arXiv does not allow public API calls to extract author email information, so we have less fine-grained metadata accessible to us.

- Also exponential!
- Mathematicians have seen a decline in papers submitted by the most senior authors.
- Computer science specifically is driving the growth


# The Slop-Cannon: Anecdotal Observations
- arXiv just posted their numbers, and they do claim that solo authorship has exploded in 2026. Our data don't capture this yet due to the metadata that we have.

# Where do we go From Here?

Recently arXiv released a blog post instituting a rate limit on paper submissions which cites AI assisted paper writing as a cause of the exponential growth in submissions. Our data does not cover the last 6 months, so it's possible that these trends have been amplified by the rapid rate of LLM assisted writing in the last 6 months. Regardless, the exponential growth in graduate students will surely continue to drive a large portion of the increase in papers. 

# Acknowledgements

# References

# Appendix: Data Collection & Curation

All of our findings are built from public metadata — we never needed paper
contents. Aggregates are computed with [DuckDB](https://duckdb.org) over the
files below and emitted as JSON that the figures read directly. The collection
scripts, queries, and build pipeline are open source at
[github.com/KyroChi/cs-papers](https://github.com/KyroChi/cs-papers); external
data is re-downloaded by those scripts rather than committed.

## arXiv metadata

The arXiv figures come from the `metadata` configuration of the
[`secemp9/arxiv-complete`](https://huggingface.co/datasets/secemp9/arxiv-complete)
dataset on Hugging Face — a single ~1.6 GB Parquet file with one row per paper,
covering 3.15M papers. (The full dataset bundles PDFs and LaTeX source and runs
to roughly 16 TiB; we deliberately pulled only the metadata config, since every
question we ask is answerable from metadata alone.) arXiv metadata is
distributed by Cornell under CC0.

We use a handful of fields: the raw `authors` string, `categories` /
`primary_category`, and `first_version_date`. A few choices worth stating:

- **Submission year.** Each paper is dated by the year of its *first* version
  (`first_version_date`), i.e. the original submission, not later revisions.
  1991–2025 are complete years; 2026 is year-to-date through August and is
  always shown separately.
- **Author counts.** arXiv stores authors as a single display string, so we
  count authors by splitting on commas and the word "and" (after stripping
  parenthetical affiliations such as "(MIT)"). A named collaboration (e.g.
  "ATLAS Collaboration") counts as one author. This is a standard proxy and is
  imperfect for unusually formatted lists.
- **Author identity.** This metadata carries no stable author identifier, so we
  identify authors by their name string. Common names collide — "Y. Wang"
  merges thousands of distinct people — so per-author arXiv figures are
  directional, not exact.
- **Subjects.** We collapse arXiv's fine-grained categories into coarse groups
  (Computer Science, Physics, Mathematics, Statistics, Electrical Engineering &
  Systems Science, …) by primary category; sub-discipline figures use the raw
  `primary_category`.
- **No affiliations.** arXiv's public metadata strips submitter emails and has
  no affiliation field, so the arXiv analyses are necessarily blind to
  institution and region. For those questions we turn to the conference data.

## Conference metadata (NeurIPS, ICML, ICLR)

The conference figures come from [Paper Copilot](https://papercopilot.com)'s
OpenReview archive (see [arXiv:2510.13201](https://arxiv.org/abs/2510.13201)) —
specifically its per-paper author files for NeurIPS, ICML, and ICLR. Each row
is one paper, with per-author fields joined by semicolons: author name,
OpenReview profile id (`or_profile`), institution (`aff`), institutional email
domain (`aff_domain`), and self-reported `position`.

- **Author identity.** Unlike arXiv, OpenReview assigns a stable profile id, so
  we de-duplicate people reliably: "unique PhD students" counts distinct
  `or_profile` values, not authorships.
- **Seniority.** The `position` field is self-reported ("PhD student", "Full
  Professor", "Postdoc", …), which we map to tiers. It is *not* inferred from
  output, so a prolific student is still counted as a PhD student. For
  paper-level seniority we attribute each paper to its *first author's* position.
- **Region.** We read each author's country from their institutional email
  **domain** (OpenReview masks the local part but exposes the domain): `.cn` and
  the major Chinese firms map to China, `.edu` and US firms to the US, other
  country-code TLDs to their country, and personal-mail domains (gmail, qq, …)
  to "unknown". Company domains resolve to a company's *headquarters*, not the
  author's office — a Google-Beijing author counts as US — so region is
  approximate, and about 11% of domains are unclassifiable. Paper-level region
  uses the author-majority country, with ties broken by a deterministic hash.
- **Coverage.** Affiliation and position data is only populated from roughly
  2021 onward. ICLR publishes *all* submissions (including rejected) on
  OpenReview; NeurIPS and ICML expose mostly accepted papers plus opt-in
  rejections. Pooled conference counts therefore mix submissions and
  acceptances, and we treat each file as one conference-year.