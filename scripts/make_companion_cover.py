"""Cover image for the companion piece: every CER pipeline incident as a dot on a map of Canada, Significant ones in
orange.

Data drawn: incident latitude and longitude from the CER file (Open Government Licence - Canada) and province and
territory outlines from Natural Earth (public domain, ne_50m_admin_1_states_provinces). No basemap tiles, no logos.
The province outlines from `input/cer/canada.geojson` are not used: that file's licence isn't confirmed.

Projection: Lambert conformal conic with Statistics Canada's parameters (standard parallels 49° and 77°, origin
63.390675° N, 91.866667° W), so Canada has its familiar shape. The map is fitted to Canada's outline. Not-significant
incidents are drawn first, Significant on top. Palette: the dataviz reference palette, light surface, slots 1 (blue)
and 2 (orange); validated with validate_palette.js --mode light (all checks pass).

Usage (from the project root):
    code/.venv/bin/python -I code/scripts/make_companion_cover.py \
        input/cer/pipeline-incidents-2026-10-28.csv input/naturalearth/ne_50m_admin_1_states_provinces.geojson output/assets
Writes output/assets/companion-cover.svg and companion-cover.png (1600 x 900, about Medium's 16:9 cover ratio).
"""

import csv
import json
import math
import pathlib
import sys

import cairosvg

W, H = 1600, 900
SURFACE, TEXT, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
LAND, BORDER = "#efeeea", "#d3d1ca"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # not significant / Significant

# Lambert conformal conic, Statistics Canada parameters
P1, P2 = math.radians(49), math.radians(77)
LAT0, LON0 = math.radians(63.390675), math.radians(-91.866667)
N = math.log(math.cos(P1) / math.cos(P2)) / math.log(math.tan(math.pi / 4 + P2 / 2) / math.tan(math.pi / 4 + P1 / 2))
F = math.cos(P1) * math.tan(math.pi / 4 + P1 / 2) ** N / N
RHO0 = F / math.tan(math.pi / 4 + LAT0 / 2) ** N


def lcc(lat: float, lon: float) -> tuple[float, float]:
    rho = F / math.tan(math.pi / 4 + math.radians(lat) / 2) ** N
    t = N * (math.radians(lon) - LON0)
    return rho * math.sin(t), RHO0 - rho * math.cos(t)  # y grows northward


def load_incidents(path: pathlib.Path) -> list[tuple[float, float, bool]]:
    with open(path, encoding="latin-1", newline="") as fh:  # the CER file isn't valid UTF-8
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        try:
            lat, lon = float(r["Latitude"]), float(r["Longitude"])
        except ValueError:
            continue
        if 40 < lat < 75 and -145 < lon < -50:  # inside Canada's rough box
            out.append((lat, lon, r["Significant"].strip().lower() == "yes"))
    return out


def load_provinces(path: pathlib.Path) -> list[list[list[tuple[float, float]]]]:
    """Canada's provinces and territories as lists of rings of (lat, lon)."""
    g = json.loads(path.read_text(encoding="utf-8"))
    shapes = []
    for f in g["features"]:
        if f["properties"].get("adm0_a3") != "CAN":
            continue
        geom = f["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        shapes.append([[(lat, lon) for lon, lat in ring] for poly in polys for ring in poly])
    return shapes


def build(points: list[tuple[float, float, bool]], provinces: list) -> str:
    rings = [ring for shape in provinces for ring in shape]
    xs = [lcc(lat, lon)[0] for ring in rings for lat, lon in ring]
    ys = [lcc(lat, lon)[1] for ring in rings for lat, lon in ring]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    # Canada fills the image's height; the text sits bottom left, over the Pacific and the US
    px0, px1, py0, py1 = 40, W - 40, 20, H - 60
    s = min((px1 - px0) / (x1 - x0), (py1 - py0) / (y1 - y0))
    ox = px1 - (x1 - x0) * s  # right-aligned, leaving the open space on the left

    def xy(lat: float, lon: float) -> tuple[float, float]:
        x, y = lcc(lat, lon)
        return ox + (x - x0) * s, py0 + (y1 - y) * s

    land = []
    for shape in provinces:
        d = "".join("M" + "L".join(f"{xy(lat, lon)[0]:.1f},{xy(lat, lon)[1]:.1f}" for lat, lon in ring) + "Z"
                    for ring in shape)
        land.append(f'<path d="{d}" fill="{LAND}" stroke="{BORDER}" stroke-width="0.9" stroke-linejoin="round"/>')
    dots = []
    for sig in (False, True):
        colour, r, op = (ORANGE, 4.2, 0.95) if sig else (BLUE, 3.0, 0.75)
        for lat, lon, si in points:
            if si is sig:
                x, y = xy(lat, lon)
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{colour}" fill-opacity="{op}" '
                            f'stroke="{SURFACE}" stroke-width="0.8"/>')
    n, n_sig = len(points), sum(p[2] for p in points)
    font = 'font-family="Helvetica, Arial, sans-serif"'
    tx, ty = 50, 590
    text = f"""
<text x="{tx}" y="{ty}" {font} font-size="60" font-weight="700" fill="{TEXT}">{n:,} pipeline</text>
<text x="{tx}" y="{ty + 70}" {font} font-size="60" font-weight="700" fill="{TEXT}">incidents</text>
<text x="{tx}" y="{ty + 118}" {font} font-size="25" fill="{MUTED}">Canada Energy Regulator record, 2008–2026</text>
<circle cx="{tx + 14}" cy="{ty + 168}" r="9" fill="{ORANGE}"/>
<text x="{tx + 34}" y="{ty + 177}" {font} font-size="25" fill="{TEXT}">Significant ({n_sig:,})</text>
<circle cx="{tx + 14}" cy="{ty + 208}" r="7" fill="{BLUE}" fill-opacity="0.85"/>
<text x="{tx + 34}" y="{ty + 217}" {font} font-size="25" fill="{TEXT}">Other incidents</text>
<text x="{W - 40}" y="{H - 14}" text-anchor="end" {font} font-size="15" fill="{MUTED}">Each dot is one incident location. Incident data: Canada Energy Regulator, Open Government Licence – Canada. Boundaries: Natural Earth.</text>
"""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>{"".join(land)}{"".join(dots)}{text}</svg>')


def main() -> None:
    incidents, outlines, out = (pathlib.Path(a) for a in sys.argv[1:4])
    points, provinces = load_incidents(incidents), load_provinces(outlines)
    svg = build(points, provinces)
    (out / "companion-cover.svg").write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / "companion-cover.png"))
    print(f"plotted {len(points)} incidents ({sum(p[2] for p in points)} Significant) on {len(provinces)} provinces")


if __name__ == "__main__":
    main()
