#!/usr/bin/env python3
"""Build a distill.pub article from Markdown prose + the figure library.

Write prose in `distill/post.md`: a YAML front-matter block (title, subtitle,
authors, published, disclaimer) followed by Markdown. Drop a figure anywhere
with a token on its own line, e.g. `{{fig:7f}}`.

This emits a genuine distill.pub page — `<d-front-matter>`, `<d-title>`,
`<d-byline>`, `<d-article>`, loading distill's `template.v2.js` and MathJax —
so it matches the kyrochi.github.io distill posts. The interactive figures
(Chart.js) and their render code are pulled from `distill/template.html`; the
latest findings (results/figures.json) and Chart.js are inlined.

Note: distill's framework loads from distill.pub, so the page needs network
for styling (like the real blog). It renders correctly locally and on GitHub
Pages; the claude.ai artifact sandbox blocks distill.pub, so use a browser.

Usage: python build_post.py            # distill/post.md -> distill/index.html
"""
import json as jsonlib
import os
import re
import sys
import urllib.request

import markdown
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "distill", "template.html")
POST = os.path.join(HERE, "distill", "post.md")
FIGURES = os.path.join(HERE, "results", "figures.json")
OUT = os.path.join(HERE, "distill", "index.html")
CHARTJS = "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"

CHART_CSS = """
:root{
  --ink:#000; --ink2:rgba(0,0,0,.72); --muted:rgba(0,0,0,.5);
  --grid:rgba(0,0,0,.1); --axis:rgba(0,0,0,.25); --surface:#fff; --ring:rgba(0,0,0,.12);
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
d-article figure{margin:1.6em auto;}
d-article figcaption{font-family:var(--sans); font-weight:600; font-size:15px; color:var(--ink); margin:0 0 2px;}
d-article figcaption b{font-weight:700;}
.sub{font-family:var(--sans); font-size:13px; color:var(--muted); margin:0 0 12px; line-height:1.5;}
.plot{position:relative; width:100%; height:360px;}
.plot.tall{height:400px;}
.subplots{display:flex; gap:16px; flex-wrap:wrap;}
.subplots>.plot{flex:1 1 320px; min-width:280px;}
.bar{display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:0 0 10px;}
.toggle{font-family:var(--sans); font-size:12px; color:var(--ink2); background:transparent;
  border:1px solid var(--ring); border-radius:999px; padding:4px 11px; cursor:pointer;}
.toggle[aria-pressed="true"]{background:var(--ink); color:#fff; border-color:var(--ink);}
.lbl{font-family:var(--sans); font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-right:2px;}
.disclaimer{color:var(--muted); font-style:italic; font-size:13px;}
.wm-wrap{display:flex; gap:16px; flex-wrap:wrap; align-items:flex-start;}
.wm-map{flex:1 1 440px; min-width:300px;}
.wm-map svg{width:100%; height:auto; display:block;}
.wm-map path{stroke:var(--surface); stroke-width:.3px;}
.wm-list{flex:0 1 230px; min-width:190px; max-height:390px; overflow-y:auto; border:1px solid var(--ring); border-radius:8px; padding:4px 0;}
.wm-row{display:flex; justify-content:space-between; gap:10px; font-family:var(--sans); font-size:12.5px; padding:3px 12px; color:var(--ink2);}
.wm-row:hover{background:var(--grid);}
.wm-row span:last-child{font-variant-numeric:tabular-nums; color:var(--ink);}
"""

MATHJAX = ('<script>MathJax={tex:{inlineMath:[[\'$\',\'$\']],'
           'displayMath:[[\'$$\',\'$$\']],tags:\'ams\'}};</script>\n'
           '<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>\n')
DISTILL = '<script src="https://distill.pub/template.v2.js"></script>\n'
D3 = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>\n'
GEO = os.path.join(HERE, "distill", "world.geo.json")


def parse_template(tpl):
    runtime = re.findall(r"<script>.*?</script>", tpl, re.S)[-1]  # render code
    figs = {}
    for block in re.findall(r"<figure\b.*?</figure>", tpl, re.S):
        m = re.search(r'id="f([\w-]+)"', block)
        if m:
            # distill: wide figures span the page column
            figs[m.group(1)] = block.replace('class="fig-wide"', 'class="l-page"')
    return runtime, figs


def front_matter(md):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    if m:
        return yaml.safe_load(m.group(1)) or {}, m.group(2)
    return {}, md


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    runtime, figs = parse_template(tpl)
    data = open(FIGURES, encoding="utf-8").read()

    raw = open(POST, encoding="utf-8").read()
    fm, md = front_matter(raw)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)         # drop authoring notes
    body = markdown.markdown(md, extensions=["extra", "sane_lists", "toc"])

    # inject figures
    missing, counts = [], {}
    for fid in re.findall(r"\{\{\s*fig:([\w-]+)\s*\}\}", body):
        counts[fid] = counts.get(fid, 0) + 1
    dups = [f for f, c in counts.items() if c > 1]
    if dups:
        print("WARNING: figure token used more than once (only the first renders):",
              ", ".join(sorted(dups)))

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

    title = fm.get("title", "Untitled")
    subtitle = fm.get("subtitle", "")
    disclaimer = fm.get("disclaimer", "")
    dmap = {"title": title, "description": fm.get("description", subtitle),
            "published": fm.get("published", ""), "authors": []}
    for a in fm.get("authors", []):
        dmap["authors"].append({
            "author": a.get("name", ""), "authorURL": a.get("url", ""),
            "affiliation": a.get("affiliation", ""), "affiliationURL": a.get("affiliationURL", "")})
    front_json = jsonlib.dumps(dmap, ensure_ascii=False)

    cache = os.path.join(HERE, ".chartjs.cache")
    if not os.path.exists(cache):
        urllib.request.urlretrieve(CHARTJS, cache)
    chartjs = open(cache, encoding="utf-8").read()
    runtime = runtime.replace("__FIGDATA__", data)
    world = open(GEO, encoding="utf-8").read() if os.path.exists(GEO) else "null"

    dtitle = f"<d-title>\n<h1>{title}</h1>\n"
    if subtitle:
        dtitle += f'<p class="l-body">{subtitle}</p>\n'
    if disclaimer:
        dtitle += f'<p class="l-body disclaimer">{disclaimer}</p>\n'
    dtitle += "</d-title>\n"

    out = f"""<!DOCTYPE html>
<html data-theme="light" lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{MATHJAX}{DISTILL}{D3}<script>
{chartjs}
</script>
<script>window.WORLD={world};</script>
<style>{CHART_CSS}</style>
</head>
<body>
<d-front-matter><script type="text/json" id="distill-front-matter">{front_json}</script></d-front-matter>
{dtitle}<d-byline></d-byline>
<d-article>
{body}
</d-article>
<d-appendix></d-appendix>
{runtime}
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(out)
    used = len(re.findall(r"<figure\b", body))
    print(f"Wrote {OUT} ({len(out)} bytes, {used} figures)")


if __name__ == "__main__":
    main()
