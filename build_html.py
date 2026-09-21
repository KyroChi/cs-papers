#!/usr/bin/env python3
"""Assemble the self-contained figures document.

Inlines the computed data (figures.json) and Chart.js into the HTML template so
the result renders offline with no external requests. Run build_figures.py first.

Reads the LATEST findings (results/figures.json) and the distill template, and
writes the self-contained page to distill/index.html.

Usage: python build_html.py [template.html] [figures.json] [out.html]
       (defaults: distill/template.html results/figures.json distill/index.html)
"""
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CHARTJS = "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"
CDN_TAG = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/'
           '4.4.4/chart.umd.min.js"></script>')


def main():
    a = sys.argv[1:]
    template = a[0] if len(a) > 0 else os.path.join(HERE, "distill", "template.html")
    figures = a[1] if len(a) > 1 else os.path.join(HERE, "results", "figures.json")
    out = a[2] if len(a) > 2 else os.path.join(HERE, "distill", "index.html")
    html = open(template).read()
    data = open(figures).read()

    cache = os.path.join(HERE, ".chartjs.cache")
    if not os.path.exists(cache):
        urllib.request.urlretrieve(CHARTJS, cache)
    chartjs = open(cache).read()

    assert "__FIGDATA__" in html and CDN_TAG in html, "template markers missing"
    html = html.replace("__FIGDATA__", data)
    html = html.replace(CDN_TAG, "<script>\n" + chartjs + "\n</script>")
    open(out, "w").write(html)
    print(f"Wrote {out} ({len(html)} bytes, cdnjs refs left: {html.count('cdnjs')})")


if __name__ == "__main__":
    main()
