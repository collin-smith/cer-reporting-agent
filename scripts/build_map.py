"""Build the CER incident overview map (draft) from the raw CSV.

Usage: python3 -I code/scripts/build_map.py
Reads input/cer/pipeline-incidents-comprehensive-data.csv + input/cer/canada.geojson,
writes output/cer-incident-map.html (data embedded; no external tiles).
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RAW = PROJECT / "input" / "cer"
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
    g = json.load(open(path))
    out = []
    for f in g["features"]:
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
        out.append({"type": "Feature", "properties": {"name": f["properties"]["name"]},
                    "geometry": {"type": "MultiPolygon", "coordinates": keep}})
    return {"type": "FeatureCollection", "features": out}


def main():
    rows = list(csv.DictReader(open(RAW / "pipeline-incidents-comprehensive-data.csv", encoding="latin-1")))
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
        recs.append([
            round(float(r["Longitude"]), 3), round(float(r["Latitude"]), 3),
            int(r["Year"]), group(bits), 1 if r["Significant"] == "Yes" else 0, bits,
            prov(r["Province"]), subst(r["Substance"]), vol, centre(r["Nearest Populated Centre"]),
            what(r["What happened category"]), why(r["Why it happened category"]),
            r["Incident Number"], r["Reported Date"],
        ])
    data = {"recs": recs, "prov": prov.items, "subst": subst.items, "centre": centre.items,
            "what": what.items, "why": why.items}
    geo = simplify_geo(RAW / "canada.geojson")
    tpl = (HERE / "map-template.html").read_text()
    html = (tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
               .replace("/*__GEO__*/null", json.dumps(geo, separators=(",", ":"))))
    (OUT / "cer-incident-map.html").write_text(html)
    print(len(recs), "incidents;", len(html) // 1024, "KB")


if __name__ == "__main__":
    main()
