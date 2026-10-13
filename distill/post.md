---
title: Who Fills arXiv
subtitle: An interactive look at the growth of arXiv and the machine-learning conferences.
description: Who is behind the surge in arXiv and ML-conference submissions?
published: October 13, 2026
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
    6a 6b 6c 6cb 7 7c 7d 7e 7f 7g   (conferences: region + seniority)
    8 9 10 11                       (mathematics)
    12 13                           (ICLR peer review)
    14a 14b 15 16 17 worldmap       (decomposition, PhD base, 2026 YTD)
    sen tenure ridge                (2026 solo-authorship analysis)
  Rebuild with:  make post   (or  .venv/bin/python build_post.py )
  Only the figures you reference are shown.
-->

More than 60 thousand papers were submitted to [ICLR in 2026](https://openreview.net/group?id=ICLR.cc/2027/Conference). Naturally the association between the rise of LLMs and this increase in paper submissions is conspicuous. We asked each other a simple question: "Who is writing all of these papers!?".

Our initial hypothesis was that LLM assistance was leading to a dearth of solo-authored papers from non-affiliated (novice) researchers. However the data does not seem to support this conclusion. While we did find a substantial increase in solo-authored papers being submitted to the arXiv, this increase only began in 2026. This increase does not come anywhere close to explaining the exponential growth in arXiv and conference submissions over the last seven years. What does seem explanatory is simply a massive growth in the number of computer science PhD students, who submit papers as part of their technical training. Prior to 2026 it seems that nearly 100% of the exponential growth in paper submissions can be attributed simply to an expanding pool of PhD students. In the specific case of senior mathematicians we actually found that paper submissions have been declining, and that prior to 2026 LLM use did not seem to reverse this trend.

Using metadata from arXiv, NeurIPS, ICLR, and ICML we set out to understand these recent trends in paper submissions.

The remainder of this blog post walks through our findings with empirical support from two public metadata collections:
- The [`secemp9/arxiv-complete`](https://huggingface.co/datasets/secemp9/arxiv-complete) dataset for arXiv papers.
- [Paper Copilot](https://papercopilot.com)'s
  OpenReview author files for NeurIPS, ICML, and ICLR
  ([arXiv:2510.13201](https://arxiv.org/abs/2510.13201)).

All of the code for this blog post, including download scripts, data queries, and the text itself, is open source and available at [github.com/KyroChi/cs-papers](https://github.com/KyroChi/cs-papers). If you have suggestions or ideas for further analysis, please submit a PR on GitHub. Older versions of this article can be found in the code-repo's git history. 

<p class="warn">⚠️ The arXiv results are confounded by the fact that we do not have access to unique author identifiers, only author names. Thus, common names like "John Smith" will look far more prolific than uncommon names like "Kyle Chickering" and "Dario Sučić". We include the most common names in the appendix and note that these names still only represent a tiny fraction of the papers on the arXiv. Thus we do not believe that our results will substantially change with unique author names for arXiv.</p>

# Who Submits to the Big-3 ML Conferences?
We begin by trying to understand the massive increase in the number of submissions to the "Big-3" ML conferences: NeurIPS, ICML, and ICLR. We do not yet have data for the 2026 conferences, so we restrict our analysis to papers submitted prior to 2026. We look at both conference submission data and data on arXiv submissions.  

**Main Findings:**
- The vast majority of the exponential growth prior to 2026 in submitted papers can be attributed to an exponential growth in the number of CS PhD students.
- Prior to 2026, first-author papers per capita have barely changed since the advent of LLM assistance.
- The average papers submitted per capita has risen. This reflects a trend towards larger author lists and increased collaboration.
- 2026 really is different. The anecdotal feeling that there is a massive increase in solo-authored papers, especially in CS, is supported by the data.

### An Exponential Growth in PhD Students
We found that the exponential growth in papers (see Figure 17, left) is primarily driven by a concomitant growth in the raw number of PhD students studying computer science (see Figure 17, right). In the period of time between 2021 and 2025, our data indicate that submissions to NeurIPS grew by $4.0\times$, from 2,708 to 10,761. ICLR submissions grew by $4.5\times$, from 3,014 in 2021 to 13,697 in 2025. During that same period of time, the number of unique PhD authors submitting to these conferences grew by $4.5\times$, from 3,938 in 2021 to 17,881 in 2025. ICLR submissions in particular have grown at the exact same rate as the growth in the number of PhD students!

{{fig:17}}

### LLM Use is Not Explanatory

This already suggests that LLM assistance may not be a significant contributing factor to the rise in paper submissions. We can provide further evidence in support of this conclusion by tracking the increase in first-author papers per-capita, sub-divided by seniority. Figure 7f shows that the mean first author submissions per-person per-year has risen between 2021 and 2025, but only modestly, from 0.721 to 0.768. 

{{fig:7f}}

When we look at submissions per-person per-year (i.e. not only first authorship), there is a notable increase in submissions for **both** faculty and PhD students. Perhaps LLM use is increasing research lab's inclusion of lab-mates on the authorship list. However we think it is much more likely that the increase in PhD students is nearly fully explanatory in this case as well, and the fact that the number of CS PhD students began to take off in 2022 is a coincidence, although almost certainly a coincidence spurred by the introduction of ChatGPT (i.e. we don't think that the ability to use AI to help write papers caused more students to pursue PhDs, but it's probably likely that increased excitement about AI led to universities increasing their CS program sizes). This is clearly reflected in the data (see Figure 7g). Between 2021 and 2025 the mean number of authors per paper has risen from 4.3 to 5.3, a full additional author per paper, on average. 

{{fig:7g}}

### PhD Student Growth by Region

{{fig:6cb}}

{{fig:worldmap}}

We are able to quantify the number of new PhD students in CS-adjacent fields by looking at the increase in the number of authors to big-3 conferences who are graduate students. We choose to attribute this growth to "new" PhD students (unique new authors each year), and ignore potential confounds, like students from other fields submitting to these conferences at a higher rate. 

The rate at which PhD students is being added has a clear geographic bias. Both the United States and China are adding massive numbers of PhD students. In the period between 2021 and 2025, the United States added 20,094 graduate students and China added 9,592. While the US and China do not necessarily have the highest growth rates in PhD students world-wide, their growth rate remains significant, especially given how large these two countries are. China between 2021 and 2025 grew at a rate of 10.34x, while the United States grew at a rate of 3.72x.

{{fig:7c}}

The rest of the world is not far behind. The UK, Germany, South Korea, and Hong Kong lead in the addition of graduate students. However the rate of growth in the number of graduate students in China is far outpacing the rate of growth in the number of graduate students in the United States or the rest of the world. Should these rates continue we expect the United States and China to have roughly the same number of graduate students submitting to the Big-3 conferences sometime in 2027.


# arXiv Submissions Have Been Increasing Exponentially
We now turn to analyzing trends based on arXiv metadata. The arXiv data is richer on the one hand since it spans multiple disciplines and has a larger share of historical data. On the other hand, arXiv does not allow public API calls to extract author email information, so we have less fine-grained author metadata accessible to us.

The first obvious feature is that arXiv submissions have also risen exponentially in recent years. Further analysis quickly reveals that this is due largely to a massive growth in submitted CS papers.

{{fig:1a}}
{{fig:1b}}

This trend is captured by comparing the year-over-year growth rates between the three most popular arXiv fields: CS, physics, and mathematics. Computer science is consistently growing about 6 to 20 percent faster than physics and math. Math in particular outpaced the growth of physics between 2005 and 2019, but CS outpaced both with the exception of 2011.

Another salient feature we found was that there is more collaboration, measured by the length of author lists, than there has ever been before. Broadly across both CS and mathematics, author lists have grown.

{{fig:2}}

We explore the number of papers submitted to the arXiv by seniority. Here we measure "seniority" by counting the number of papers submitted by a given author. Here there is a noticeable difference between computer science and mathematics.

For computer science (Figure, left) we can see that authors with more than 21 papers have seen a steady increase in the number of submitted papers per year since around 2015. Mathematics, on the other hand (Figure, right) has seen a stable number of submitted papers and if anything a slight decline over the same period.

{{fig:sen}}

We conjecture that this is a consequence of the pigeon-hole principle: since the rate of graduate students in CS is growing so rapidly, the number of professors cannot keep up. Thus, campus labs grow. Since most PhD students will lead one or two projects a year, and there are more PhD students, the PI's see their paper counts increase. 

# 2026 is Different
The numbers for 2026 aren't in yet, but we can analyze arXiv submissions through the end of August. 2026 shows a conspicuous increase both in the overall number of submitted papers and in the number of first author papers submitted per-person. It is apparently true that LLMs are beginning to cause a measurable uptick in the number of papers submitted per-person, and they are also causing an increase in solo-authorship.

To investigate who is contributing to the recent spike likely caused by sophisticated LLM assistance, we break-down the excess papers by author category. To ensure that we do not bias the data against 2026, we set an August cutoff period for our analysis and apply this cutoff to all years. Thus, the numbers reported below are for each year, excluding the months of September-December. By excess papers we mean the papers which exceed the predicted number of papers when fitting the growth trend to an exponential. The table below categorizes the predicted vs. actual number of papers by arXiv category, with the excess measured as a percentage and in raw papers

| group | own trend | exp 2026 | actual | excess | % over trend |
|---|---|---|---|---|---|
| Mathematics | 3.9%/yr | 27,261 | 35,304 | +8,043 | +29.5% |
| Statistics | 8.3%/yr | 4,654 | 5,813 | +1,159 | +24.9% |
| Physics | 3.7%/yr | 53,036 | 63,670 | +10,634 | +20.0% |
| Computer Science | 22.4%/yr | 101,053 | 108,228 | +7,175 | +7.1% |

Notably, cs.AI was 168% over trend, indicating that investment into AI papers specifically is exploding at a phenomenal rate. 

We next investigate who specifically is responsible for the excess papers themselves. For both math and CS, while as a group, new solo authors are submitting vastly over-trend, the bulk of the excess submissions comes from established authors.

All arXiv (sum-of-cells excess = +37,753):

| cell | own trend | excess | % over trend | % of excess |
|---|---|---|---|---|
| solo · novice | 2.0%/yr | +4,055 | +94% | 10.7% |
| solo · established | 3.0%/yr | +10,176 | +74% | 27.0% |
| team · novice | 9.5%/yr | +6,027 | +11% | 16.0% |
| team · established | 12.0%/yr | +17,495 | +15% | 46.3% |

Computer Science (sum-of-cells excess = +3,946):

| cell | own trend | excess | % over trend | % of excess |
|---|---|---|---|---|
| solo · novice | 8.9%/yr | +2,287 | +164% | 58.0% |
| solo · established | 11.7%/yr | +3,482 | +132% | 88.2% |
| team · novice | 17.6%/yr | +967 | +3% | 24.5% |
| team · established | 27.8%/yr | −2,790 | −4% | −70.7% |

Mathematics (sum-of-cells excess = +7,846):

| cell | own trend | excess | % over trend | % of excess |
|---|---|---|---|---|
| solo · novice | −0.9%/yr | +953 | +58% | 12.1% |
| solo · established | 2.4%/yr | +3,092 | +54% | 39.4% |
| team · novice | 2.3%/yr | +922 | +21% | 11.8% |
| team · established | 6.0%/yr | +2,879 | +18% | 36.7% |

For all of arXiv, nearly half of the excess submitted papers come from established teams, while only 10% come from novice solo authors. However, established solo authors are indeed writing an increasing number of papers. In both mathematics and computer science, the established authors have seen a dramatic increase in solo-authorship. In computer science specifically, established teams have actually written fewer papers than would be predicted by extrapolation, and established solo authorship accounts for a staggering 88.2% of the excess papers published in Computer Science! Mathematicians have nearly 40% of the excess papers written by established solo authors.

We further break down the seniority of the authors into buckets to determine if experienced authors who had a career before AI are submitting the excess papers, or if it is mostly novices submitting a lot of papers in the last year. We find a mix of both. There is a bimodal distribution in papers submitted by career seniority for both math and CS, with the CS distribution skewing towards junior authors and the math distribution skewing towards senior authors (figure below).

{{fig:tenure}}

This is perhaps unsurprising, given the number of young people pouring into CS PhD programs compared to math PhD programs. It is notable however that junior authors in both fields **are** submitting an increasing number of solo-authored papers. 

We further break down the buckets by number of years on the arXiv to control for a flood of novice authors who have submitted more than 31 papers in 2026 alone. We find (thankfully) that this distribution skews upwards as the number of submitted papers increases. This tells us that "experienced authors" really are career computer scientists and mathematicians who are accounting for the increase in submitted papers and the increase is not due soley to junior authors flooding the arXiv with papers.

{{fig:ridge}}

Regardless of how we look at the data, it is clear that there has been a massive sea-change in authorship norms in computer science. 

# What's Next

Recently arXiv released a blog post instituting a rate limit on paper submissions which cites AI assisted paper writing as a cause of the exponential growth in submissions. This is certainly one solution, but it is a solution targeted specifically at the use of LLMs. Thus, it will only address the "excess" paper submissions, and not the broader trend driven by an exponential growth in the number of CS PhD students! We predict that the rate limit will do very little to quell the growing tsunami landing upon our academic shores.

# Acknowledgements

# References
- arXiv. "Attention Authors: Updated Practice for Review Articles and Position Papers in arXiv CS Category." arXiv blog, October 31, 2025. <https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/>
- secemp9. "arxiv-complete" (metadata config). Hugging Face Datasets. <https://huggingface.co/datasets/secemp9/arxiv-complete>
- Jing Yang, Qiyao Wei, and Jiaxin Pei. "Paper Copilot: Tracking the Evolution of Peer Review in AI Conferences." arXiv:2510.13201, 2025. <https://arxiv.org/abs/2510.13201>. Data: <https://github.com/papercopilot/openreview>
- ICLR 2027 submission count (≈62,288 registered abstracts, by max OpenReview submission ID as of Sept 21, 2026). <https://reviewer3.com/evidence/iclr-submissions-2027> · primary: <https://openreview.net/group?id=ICLR.cc/2027/Conference>

# Appendix A: LLM Use Statement
We used Claude Opus 4.8 and Claude Opus 5.5 to manage the generation of queries. Figures were specified in natural language and plotted using LLMs. We did not use LLMs for drafting or editing the write-up presented here (other than finding typos).

# Appendix B: The Most Common Names on the arXiv

| # | name string | papers | % all | 92–94 | 95–97 | 98–00 | 01–03 | 04–06 | 07–09 | 10–12 | 13–15 | 16–18 | 19–21 | 22–24 | 25–27 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Yang Liu | 3,048 | 0.10% | – | – | – | – | 0.00 | 0.01 | 0.02 | 0.03 | 0.04 | 0.09 | 0.15 | 0.20 |
| 2 | Y. Zhang | 2,823 | 0.09% | – | 0.01 | 0.01 | 0.02 | 0.01 | 0.03 | 0.06 | 0.14 | 0.14 | 0.10 | 0.11 | 0.08 |
| 3 | Wei Wang | 2,494 | 0.08% | 0.02 | 0.01 | – | 0.00 | 0.02 | 0.03 | 0.03 | 0.03 | 0.05 | 0.08 | 0.10 | 0.15 |
| 4 | Y. Wang | 2,375 | 0.08% | – | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.03 | 0.04 | 0.06 | 0.10 | 0.10 | 0.11 |
| 5 | Lei Zhang | 2,239 | 0.07% | – | – | – | – | 0.00 | 0.01 | 0.01 | 0.03 | 0.03 | 0.07 | 0.11 | 0.14 |
| 6 | Takashi Taniguchi | 2,164 | 0.07% | – | – | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.02 | 0.05 | 0.10 | 0.11 | 0.11 |
| 7 | Kenji Watanabe | 2,106 | 0.07% | – | – | – | – | – | – | 0.00 | 0.01 | 0.05 | 0.10 | 0.11 | 0.10 |
| 8 | Y. Li | 2,071 | 0.07% | – | – | 0.00 | 0.00 | 0.01 | 0.01 | 0.02 | 0.13 | 0.10 | 0.06 | 0.06 | 0.08 |
| 9 | Wei Zhang | 1,989 | 0.06% | – | – | 0.00 | 0.00 | 0.01 | 0.02 | 0.02 | 0.03 | 0.05 | 0.06 | 0.08 | 0.12 |
| 10 | Xin Wang | 1,864 | 0.06% | – | – | – | 0.00 | 0.00 | 0.00 | 0.01 | 0.02 | 0.04 | 0.06 | 0.08 | 0.12 |
| 11 | Yu Zhang | 1,863 | 0.06% | – | 0.02 | 0.00 | – | 0.00 | 0.01 | 0.01 | 0.02 | 0.05 | 0.07 | 0.08 | 0.11 |
| 12 | Z. Wang | 1,813 | 0.06% | – | 0.00 | 0.01 | 0.01 | 0.02 | 0.01 | 0.02 | 0.03 | 0.05 | 0.08 | 0.09 | 0.08 |
| 13 | Wei Chen | 1,694 | 0.05% | 0.08 | 0.02 | 0.01 | 0.00 | 0.01 | 0.01 | 0.02 | 0.04 | 0.05 | 0.06 | 0.07 | 0.09 |
| 14 | L. Sun | 1,677 | 0.05% | – | – | – | – | 0.00 | 0.00 | 0.01 | 0.05 | 0.07 | 0.07 | 0.07 | 0.07 |
| 15 | X. Liu | 1,650 | 0.05% | – | – | – | 0.01 | 0.03 | 0.02 | 0.01 | 0.04 | 0.09 | 0.08 | 0.07 | 0.05 |
