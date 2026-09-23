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
Our primary finding is that the exponential growth in papers (See Figure ) is driven by a concomitant growth in the raw number of PhD students studying computer science (See Figure ).

{{fig:17}}

## LLM Use is Not Explanatory

## Paper Submissions by Career Seniority 

## PhD Student Growth by Region


# arXiv Submissions Have Been Increasing Exponentially 

# The Slop-Cannon: Anecdotal Observations

# Where do we go From Here?

# Acknowledgements

# References

# Appendix: Data Collection & Curation

## All of arXiv

_How much has arXiv grown, and how has its subject mix shifted?_

{{fig:1a}}

{{fig:1b}}

{{fig:1c}}

_Growth is collaborative, not solo — set up Figure 2._

{{fig:2}}

## Computer Science

_CS is the engine. Prose on the AI/ML subfields and team sizes._

{{fig:2cs}}

{{fig:3}}

## By region — NeurIPS · ICML · ICLR

_China vs US vs Other over time; what the affiliation domains show._

{{fig:6b}}

{{fig:6c}}

_Seniority: who leads the papers._

{{fig:7}}

{{fig:7f}}

## Is the surge just an LLM artifact?

_State the hypothesis, then the bounding argument._

{{fig:16}}

## Methods & data

_Sources, definitions, coverage windows, caveats._
