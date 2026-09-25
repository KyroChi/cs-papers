#!/usr/bin/env python3
"""Fetch + simplify world country borders into distill/world.geo.json.

Downloads Natural Earth 110m country polygons, keeps only NAME + ISO_A3, and
rounds coordinates to ~1 km so the file is small enough to embed in the page.
Run once; the output is committed (static map geometry, not analysis data).
"""
import json
import os
import urllib.request

URL = ("https://cdn.jsdelivr.net/gh/nvkelso/natural-earth-vector@master/"
       "geojson/ne_110m_admin_0_countries.geojson")
OUT = os.path.join(os.path.dirname(__file__), "distill", "world.geo.json")


def round_coords(x, nd=2):
    if isinstance(x, (int, float)):
        return round(x, nd)
    return [round_coords(v, nd) for v in x]


def main():
    print("downloading Natural Earth 110m…")
    with urllib.request.urlopen(URL) as r:
        gj = json.load(r)
    feats = []
    for f in gj["features"]:
        p = f.get("properties", {})
        name = p.get("ADMIN") or p.get("NAME") or p.get("name")
        iso = p.get("ISO_A3") or p.get("ISO_A3_EH") or p.get("ADM0_A3")
        if not f.get("geometry"):
            continue
        f["geometry"]["coordinates"] = round_coords(f["geometry"]["coordinates"])
        feats.append({"type": "Feature",
                      "properties": {"name": name, "iso": iso},
                      "geometry": f["geometry"]})
    out = {"type": "FeatureCollection", "features": feats}
    with open(OUT, "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1e3:.0f} KB, {len(feats)} countries)")


if __name__ == "__main__":
    main()
