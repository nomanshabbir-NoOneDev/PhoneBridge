#!/usr/bin/env python3
"""Puts raw screenshots into device frames for the README.

  1. Save your screenshots in assets/raw/ with the names listed in assets/raw/README.txt (png or jpg).
  2. Run:  python3 tools/frame_screenshots.py        (needs Pillow:  pip install pillow)
  3. Framed images appear in assets/screens/ (transparent background, soft shadow) and the README picks them up.

Tall images get a phone frame (a camera island for names starting with "web-iphone", a punch-hole camera otherwise);
wide images get a browser-window frame. Optional: pass another source folder as the first argument."""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets" / "raw"
OUT = ROOT / "assets" / "screens"
K = 2  # draw at 2x, shrink at the end: smooth edges


def mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=r, fill=255)
    return m


def shadow(canvas, box, r):
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((box[0], box[1] + 28 * K, box[2], box[3] + 28 * K), radius=r, fill=(0, 0, 0, 90))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26 * K)))


def phone(shot, island):
    sw = 540 * K
    shot = shot.convert("RGB").resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
    bez, pad = 16 * K, 44 * K
    w, h = shot.width + 2 * bez, shot.height + 2 * bez
    canvas = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    box = (pad, pad, pad + w, pad + h)
    r = 74 * K
    shadow(canvas, box, r)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((box[0] - 3 * K, box[1] - 3 * K, box[2] + 3 * K, box[3] + 3 * K), radius=r + 3 * K, fill=(154, 163, 178))  # metal rim
    d.rounded_rectangle(box, radius=r, fill=(10, 10, 13))  # bezel
    for y0, y1 in ((h * 0.20, h * 0.20 + 34 * K), (h * 0.20 + 46 * K, h * 0.20 + 80 * K)):  # volume keys
        d.rounded_rectangle((box[0] - 7 * K, box[1] + y0, box[0] - 2 * K, box[1] + y1), radius=2 * K, fill=(107, 114, 128))
    d.rounded_rectangle((box[2] + 2 * K, box[1] + h * 0.30, box[2] + 7 * K, box[1] + h * 0.30 + 60 * K), radius=2 * K, fill=(107, 114, 128))  # power
    canvas.paste(shot, (pad + bez, pad + bez), mask(shot.size, r - bez))
    cx = canvas.width // 2
    top = pad + bez + 14 * K
    if island:
        d.rounded_rectangle((cx - 80 * K, top, cx + 80 * K, top + 44 * K), radius=22 * K, fill=(5, 5, 8))
    else:
        d.ellipse((cx - 10 * K, top + 4 * K, cx + 10 * K, top + 24 * K), fill=(5, 5, 8))
    return canvas


def browser(shot):
    sw = 1100 * K
    shot = shot.convert("RGB").resize((sw, round(shot.height * sw / shot.width)), Image.LANCZOS)
    bar, pad, r = 44 * K, 44 * K, 22 * K
    w, h = shot.width, shot.height + bar
    canvas = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    box = (pad, pad, pad + w, pad + h)
    shadow(canvas, box, r)
    win = Image.new("RGBA", (w, h), (30, 33, 40, 255))
    d = ImageDraw.Draw(win)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((20 * K + i * 26 * K, 14 * K, 36 * K + i * 26 * K, 30 * K), fill=c)
    d.rounded_rectangle((w // 2 - 220 * K, 8 * K, w // 2 + 220 * K, bar - 8 * K), radius=14 * K, fill=(48, 52, 62))
    win.paste(shot, (0, bar))
    canvas.paste(win, (pad, pad), mask(win.size, r))
    return canvas


OUT.mkdir(parents=True, exist_ok=True)
files = sorted(p for p in SRC.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
if not files:
    sys.exit(f"No screenshots in {SRC}")
for f in files:
    im = Image.open(f)
    out = browser(im) if im.width > im.height else phone(im, f.stem.startswith("web-iphone"))
    out = out.resize((out.width // K, out.height // K), Image.LANCZOS)
    out.save(OUT / f"{f.stem}.png", optimize=True)
    print(f"{f.name} -> assets/screens/{f.stem}.png")
