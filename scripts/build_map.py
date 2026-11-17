"""Build the CER incident map, a standalone page for static hosting (S3 + CloudFront, code/infra-map/).

Usage: python3 -I code/scripts/build_map.py
Reads the CER snapshot (input/cer/pipeline-incidents-2026-10-28.csv), Canada's province and territory outlines from
Natural Earth (public domain; input/naturalearth/ne_50m_admin_1_states_provinces.geojson, from
https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_1_states_provinces.geojson)
and the series links (code/scripts/map-series.json; fill each url as the piece goes live).
Writes output/cer-incident-map.html (data embedded; no external tiles).
"""

import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RAW = PROJECT / "input" / "cer"
SNAPSHOT = RAW / "pipeline-incidents-2026-10-28.csv"
OUTLINES = PROJECT / "input" / "naturalearth" / "ne_50m_admin_1_states_provinces.geojson"
OUT = PROJECT / "output"

TYPE_BITS = {
    "Release of Substance": 1,
    "Operation Beyond Design Limits": 2,
    "Fire": 4,
    "Explosion": 8,
    "Serious Injury (as defined in the OPR)": 16,
    "Fatality": 32,
    "Adverse Environmental Effects": 64,
}


def group(bits):
    """One colour group per incident; most severe wins for multi-type incidents."""
    if bits & (16 | 32):
        return 3  # injury or fatality
    if bits & (4 | 8):
        return 1  # fire or explosion
    if bits & (1 | 64):
        return 0  # release / environmental
    return 2  # operation beyond design limits


class Lookup:
    def __init__(self):
        self.items, self.index = [], {}

    def __call__(self, s):
        s = (s or "").strip()
        if s not in self.index:
            self.index[s] = len(self.items)
            self.items.append(s)
        return self.index[s]


def simplify_geo(path):
    """Canada's provinces and territories from Natural Earth, coordinates rounded to 0.01°."""
    g = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    out = []
    for f in g["features"]:
        if f["properties"].get("adm0_a3") != "CAN":
            continue
        polys = f["geometry"]["coordinates"]
        if f["geometry"]["type"] == "Polygon":
            polys = [polys]
        keep = []
        for poly in polys:
            rings = []
            for ring in poly:
                pts, last = [], None
                for x, y in ring:
                    p = (round(x, 2), round(y, 2))
                    if p != last:
                        pts.append(list(p))
                        last = p
                if len(pts) >= 8:
                    rings.append(pts)
            if rings:
                keep.append(rings)
        out.append(
            {
                "type": "Feature",
                "properties": {"name": f["properties"]["name"]},
                "geometry": {"type": "MultiPolygon", "coordinates": keep},
            }
        )
    return {"type": "FeatureCollection", "features": out}


def main():
    with open(SNAPSHOT, encoding="latin-1", newline="") as f:  # the CER file isn't valid UTF-8
        rows = list(csv.DictReader(f))
    prov, subst, centre, what, why = Lookup(), Lookup(), Lookup(), Lookup(), Lookup()
    recs = []
    for r in rows:
        bits = 0
        for t in r["Incident Types"].split(","):
            bits |= TYPE_BITS.get(t.strip(), 0)
        try:
            vol = float(r["Approximate Volume Released (m3)"])
        except ValueError:
            vol = None
        recs.append(
            [
                round(float(r["Longitude"]), 3),
                round(float(r["Latitude"]), 3),
                int(r["Year"]),
                group(bits),
                1 if r["Significant"] == "Yes" else 0,
                bits,
                prov(r["Province"]),
                subst(r["Substance"]),
                vol,
                centre(r["Nearest Populated Centre"]),
                what(r["What happened category"]),
                why(r["Why it happened category"]),
                r["Incident Number"],
                r["Reported Date"],
            ]
        )
    data = {
        "recs": recs,
        "prov": prov.items,
        "subst": subst.items,
        "centre": centre.items,
        "what": what.items,
        "why": why.items,
    }
    geo = simplify_geo(OUTLINES)
    series = json.loads((HERE / "map-series.json").read_text(encoding="utf-8"))
    tpl = (HERE / "map-template.html").read_text(encoding="utf-8")
    html = (
        tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
        .replace("/*__GEO__*/null", json.dumps(geo, separators=(",", ":")))
        .replace("/*__SERIES__*/null", json.dumps(series, separators=(",", ":")))
    )
    (OUT / "cer-incident-map.html").write_text(html, encoding="utf-8")
    print(
        len(recs),
        "incidents,",
        sum(r[4] for r in recs),
        "Significant;",
        len(geo["features"]),
        "provinces;",
        len(html) // 1024,
        "KB",
    )


if __name__ == "__main__":
    main()
