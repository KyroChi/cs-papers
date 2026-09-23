# Who Fills arXiv

<p class="authors">Kyle Chickering &amp; Dario Sučić</p>

<p class="byline">An interactive look at the growth of arXiv and the machine-learning conferences.</p>

<p class="disclaimer">This post reflects the personal views of the authors and not those of their employer.</p>

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

_Intro prose here — the question, the data, what we found in one paragraph._

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
