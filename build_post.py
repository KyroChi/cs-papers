#!/usr/bin/env python3
"""Build the distill page from Markdown prose + the figure library.

Write prose in `distill/post.md` (plain Markdown). Drop a figure anywhere with a
token on its own line:

    {{fig:7f}}

The figure's interactive block (caption, controls, canvas) is pulled from
`distill/template.html` — the figure library / runtime, which Claude edits. This
script renders the Markdown, injects the requested figures, inlines the latest
findings (results/figures.json) and Chart.js, and writes a self-contained
`distill/index.html`. Figures you don't reference simply aren't shown (their
renderers no-op when the canvas is absent).

Usage: python build_post.py            # distill/post.md -> distill/index.html
"""
import os
import re
import sys
import urllib.request

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "distill", "template.html")
POST = os.path.join(HERE, "distill", "post.md")
FIGURES = os.path.join(HERE, "results", "figures.json")
OUT = os.path.join(HERE, "distill", "index.html")
CHARTJS = "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"
CDN_TAG = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/'
           '4.4.4/chart.umd.min.js"></script>')


def parse_template(tpl):
    style = re.search(r"<style>.*?</style>", tpl, re.S).group(0)
    # the render code is the only <script> with no attributes
    runtime = re.findall(r"<script>.*?</script>", tpl, re.S)[-1]
    figs = {}
    for block in re.findall(r"<figure\b.*?</figure>", tpl, re.S):
        m = re.search(r'id="f([\w-]+)"', block)
        if m:
            figs[m.group(1)] = block
    return style, runtime, figs


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    style, runtime, figs = parse_template(tpl)
    data = open(FIGURES, encoding="utf-8").read()

    md = open(POST, encoding="utf-8").read()
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)   # drop authoring comments
    title_m = re.search(r"^#\s+(.+)$", md, re.M)
    title = title_m.group(1).strip() if title_m else "Who Fills arXiv"
    body = markdown.markdown(md, extensions=["extra", "sane_lists", "toc"])

    # warn on repeated figure tokens — the same block twice means duplicate
    # canvas ids, so only the first instance renders.
    counts = {}
    for fid in re.findall(r"\{\{\s*fig:([\w-]+)\s*\}\}", body):
        counts[fid] = counts.get(fid, 0) + 1
    dups = [f for f, c in counts.items() if c > 1]
    if dups:
        print("WARNING: figure token used more than once (only the first will "
              "render — duplicate canvas ids):", ", ".join(sorted(dups)))

    # inject figures: {{fig:ID}} (optionally wrapped in a <p> by Markdown)
    missing = []

    def repl(m):
        fid = m.group(1)
        if fid not in figs:
            missing.append(fid)
            return f"<!-- unknown figure: {fid} -->"
        return figs[fid]

    body = re.sub(r"<p>\s*\{\{\s*fig:([\w-]+)\s*\}\}\s*</p>", repl, body)
    body = re.sub(r"\{\{\s*fig:([\w-]+)\s*\}\}", repl, body)
    if missing:
        print("WARNING: unknown figure tokens:", ", ".join(sorted(set(missing))))
        print("Available:", ", ".join(sorted(figs)))

    cache = os.path.join(HERE, ".chartjs.cache")
    if not os.path.exists(cache):
        urllib.request.urlretrieve(CHARTJS, cache)
    chartjs = open(cache, encoding="utf-8").read()

    runtime = runtime.replace("__FIGDATA__", data)
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Libre+Franklin:wght@400;500;600;700&display=swap">\n')
    out = ('<meta charset="utf-8">\n'
           f"<title>{title}</title>\n"
           f"{fonts}"
           f"<script>\n{chartjs}\n</script>\n"
           f"{style}\n"
           '<div class="controls"><button class="toggle" id="themeBtn">◐ theme</button></div>\n'
           f'<div class="wrap">\n{body}\n</div>\n'
           f"{runtime}\n")
    open(OUT, "w", encoding="utf-8").write(out)
    used = len(re.findall(r"<figure\b", body))
    print(f"Wrote {OUT} ({len(out)} bytes, {used} figures, cdnjs refs left: {out.count('cdnjs')})")


if __name__ == "__main__":
    main()
