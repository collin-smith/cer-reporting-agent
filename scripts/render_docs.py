"""Render about 30 test cases as documents for the Textract slice (D24). $0, no AWS calls.

Each chosen case is rendered three ways, from the same report text:
  form   a filled-in field incident form, as a born-digital PDF (reportlab)
  scan   the report printed and scanned: grayscale, slight skew, blur, noise, JPEG artefacts
  photo  the printout photographed on a desk: perspective, uneven light, more blur, JPEG

The form adds only labels and the case's operator, reporter role and channel, never a fact the report doesn't state
(D30), so any accuracy drop against the text arm comes from OCR, not from extra or missing information.

Cases come from the dev and test splits only (never held-out), stratified by kind, with a fixed seed. Renders are
deterministic for a given Pillow/reportlab version. The images are not committed (about 10 MB); the manifest is, with
each file's SHA-256, so the OCR cache (cer_agent.ocr) knows when a render has changed.

Run from code/:  uv run --extra render python -I scripts/render_docs.py
Writes code/evals/renders/<id>-<form|scan|photo>.<pdf|jpg> and code/evals/renders/manifest.json.
"""

from __future__ import annotations

import collections
import hashlib
import io
import json
import pathlib
import random
import sys

CODE = pathlib.Path(__file__).resolve().parents[1]
CASES = CODE / "evals" / "cases" / "cases.jsonl"
OUT = CODE / "evals" / "renders"
SEED = 24  # D24
PER_KIND = {"clear-cut": 13, "judgment": 10, "not-reportable": 4, "adversarial": 3}  # ~ dev+test mix, 30 in all
FORMATS = ("form", "scan", "photo")
FONT = pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
FONT_BOLD = pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
CHANNEL = {
    "an email to the compliance inbox": "Email",
    "a phone call written up by the on-call": "Phone call (on-call write-up)",
    "text messages from the field": "Text messages",
}


def choose(cases: list[dict]) -> list[dict]:
    """Stratified by kind from dev + test, fixed seed, sorted by ID."""
    rng = random.Random(SEED)
    pool = collections.defaultdict(list)
    for c in cases:
        if c["split"] in ("dev", "test"):
            pool[c["kind"]].append(c)
    chosen = []
    for kind, n in PER_KIND.items():
        chosen += rng.sample(sorted(pool[kind], key=lambda c: c["id"]), n)
    return sorted(chosen, key=lambda c: c["id"])


# --- form: born-digital PDF ---


def render_form(case: dict) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    if "DejaVu" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("DejaVu", str(FONT)))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_BOLD)))
    buf = io.BytesIO()
    w, h = letter
    c = canvas.Canvas(buf, pagesize=letter, invariant=1)  # invariant: no timestamp, so the bytes are repeatable
    m = 54
    c.setFont("DejaVu-Bold", 15)
    c.drawString(m, h - 60, "FIELD INCIDENT REPORT")
    c.setFont("DejaVu", 8)
    c.drawRightString(w - m, h - 60, "Form FIR-1 (rev. 2026-03)")
    y = h - 92
    for label, value in (("Operator", case["operator"]), ("Reported by", case["reporter"].capitalize()),
                         ("Received via", CHANNEL.get(case["style"], case["style"]))):  # fmt: skip
        c.rect(m, y - 6, w - 2 * m, 22)
        c.setFont("DejaVu-Bold", 8)
        c.drawString(m + 4, y + 7, label.upper())
        c.setFont("DejaVu", 10)
        c.drawString(m + 100, y, value)
        y -= 22
    y -= 14
    c.setFont("DejaVu-Bold", 8)
    c.drawString(m, y, "DESCRIPTION OF THE EVENT (what happened, when, where, who, what was released)")
    top = y - 6
    c.setFont("DejaVu", 10)
    y = top - 16
    for para in case["report"].splitlines():
        for line in simpleSplit(para, "DejaVu", 10, w - 2 * m - 12) or [""]:
            c.drawString(m + 6, y, line)
            y -= 13.5
    c.rect(m, min(y, 160) - 4, w - 2 * m, top - min(y, 160) + 4)
    c.setFont("DejaVu-Bold", 8)
    c.drawString(m, 120, "SUPERVISOR REVIEW")
    c.rect(m, 70, w - 2 * m, 44)
    c.showPage()
    c.save()
    return buf.getvalue()


# --- scan and photo: a printout rasterised, then degraded ---

DPI = 150
PAGE = (int(8.5 * DPI), int(11 * DPI))


def printout(case: dict, size_px: int = 22):
    """The report as a plain printed page (an email or notes printout), white paper, black text."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("L", PAGE, 255)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT), size_px)
    m, y, lh = 120, 130, int(size_px * 1.45)
    width = PAGE[0] - 2 * m
    for para in case["report"].splitlines():
        line = ""
        for word in para.split(" "):
            trial = f"{line} {word}".strip()
            if font.getlength(trial) <= width:
                line = trial
                continue
            d.text((m, y), line, font=font, fill=20)
            y, line = y + lh, word
        d.text((m, y), line, font=font, fill=20)
        y += lh
    return img


def _noise(img, rng: random.Random, amp: float):
    """Add grain of +/- amp grey levels from the case's own seed (Image.effect_noise uses C rand(), so a render
    would depend on call order). The noise is centred on 128, so img + noise - 128 darkens and lightens."""
    from PIL import Image, ImageChops

    raw = Image.frombytes("L", img.size, rng.randbytes(img.size[0] * img.size[1]))
    grain = raw.point(lambda v: int(128 + (v - 128) * amp / 128))
    return ImageChops.add(img, grain, scale=1.0, offset=-128)


def _jpeg(img, quality: int) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=False)
    return buf.getvalue()


def render_scan(case: dict) -> bytes:
    from PIL import Image, ImageFilter

    rng = random.Random(f"{SEED}-scan-{case['id']}")
    img = printout(case)
    img = img.rotate(rng.uniform(-1.2, 1.2), resample=Image.BICUBIC, fillcolor=255, expand=False)
    img = img.filter(ImageFilter.GaussianBlur(0.7))
    img = _noise(img, rng, 30)
    img = img.point(lambda v: int(30 + v * 0.86))  # greyish paper, washed-out toner
    for _ in range(rng.randint(40, 120)):  # dust and speckle
        x, y = rng.randrange(PAGE[0]), rng.randrange(PAGE[1])
        img.putpixel((x, y), rng.randint(40, 120))
    return _jpeg(img, 55)


def render_photo(case: dict) -> bytes:
    from PIL import Image, ImageChops, ImageFilter

    rng = random.Random(f"{SEED}-photo-{case['id']}")
    paper = printout(case).convert("RGB")
    paper = ImageChops.multiply(paper, Image.new("RGB", PAGE, (250, 246, 236)))  # warm, off-white paper
    bw, bh = int(PAGE[0] * 1.18), int(PAGE[1] * 1.14)
    desk = Image.new("RGB", (bw, bh), (92, 74, 58))
    desk.paste(paper, ((bw - PAGE[0]) // 2, (bh - PAGE[1]) // 2))
    desk = desk.rotate(rng.uniform(-4, 4), resample=Image.BICUBIC, fillcolor=(92, 74, 58))

    def j(v: int, f: float) -> int:  # jitter a corner by up to f of the side
        return int(v + rng.uniform(-f, f) * bw)

    m = 0.04 * bw  # quad corners in the source: NW, SW, SE, NE; unequal jitter gives the perspective
    quad = (j(m, 0.03), j(m, 0.02), j(m, 0.02), j(bh - m, 0.03), j(bw - m, 0.05), j(bh - m, 0.02),
            j(bw - m, 0.02), j(m, 0.05))  # fmt: skip
    out = desk.transform((bw, bh), Image.QUAD, quad, resample=Image.BICUBIC)
    # Uneven light: a horizontal and vertical falloff from a random bright corner.
    # Rotate a gradient twice the size and keep the centre, so the rotation's fill corners never show.
    angle = rng.choice((0, 90, 180, 270)) + rng.uniform(-20, 20)
    light = Image.linear_gradient("L").resize((2 * bw, 2 * bh)).rotate(angle, resample=Image.BICUBIC)
    light = light.crop((bw // 2, bh // 2, bw // 2 + bw, bh // 2 + bh))
    light = light.point(lambda v: int(255 - v * 0.42)).convert("RGB")
    out = ImageChops.multiply(out, light)
    out = out.filter(ImageFilter.GaussianBlur(rng.uniform(0.9, 1.3)))
    out = out.resize((1200, int(1200 * bh / bw)), Image.LANCZOS)  # sent through a messaging app
    return _jpeg(out, 68)


RENDERERS = {"form": (render_form, "pdf"), "scan": (render_scan, "jpg"), "photo": (render_photo, "jpg")}


def main() -> int:
    if not FONT.exists():
        print(f"Font not found: {FONT} (install fonts-dejavu-core)")
        return 2
    cases = [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines()]
    chosen = choose(cases)
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in chosen:
        for fmt in FORMATS:
            fn, ext = RENDERERS[fmt]
            data = fn(case)
            name = f"{case['id']}-{fmt}.{ext}"
            (OUT / name).write_bytes(data)
            entries.append({"id": case["id"], "split": case["split"], "kind": case["kind"], "format": fmt,
                            "file": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                            "report_sha256": hashlib.sha256(case["report"].encode()).hexdigest()})  # fmt: skip
        print(f"{case['id']} {case['split']:4} {case['kind']}")
    manifest = {"seed": SEED, "per_kind": PER_KIND, "formats": list(FORMATS), "renders": entries}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    total = sum(e["bytes"] for e in entries)
    print(f"{len(chosen)} cases, {len(entries)} documents, {total / 1e6:.1f} MB -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
