"""Draws the home screen icon (a spool of filament on blue).
Run once: python collector/make_icons.py  (needs Pillow)."""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "docs" / "icons"
OUT.mkdir(parents=True, exist_ok=True)

S = 1024
BLUE, WHITE = (11, 99, 206), (255, 255, 255)
CX, CY = 452, 436          # spool centre, left of middle to leave room for the strand
W = 46                     # stroke width

img = Image.new("RGB", (S, S), BLUE)
d = ImageDraw.Draw(img)


def ring(r, width):
    d.ellipse((CX - r, CY - r, CX + r, CY + r), outline=WHITE, width=width)


def dot(x, y, r):
    d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)


def bezier(p0, p1, p2, steps=60):
    return [(round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]),
             round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
            for t in (i / steps for i in range(steps + 1))]


ring(300, W)               # the flange
ring(206, 30)              # the edge of the wound filament
dot(CX, CY, 84)            # the hub

# One strand running off the spool, down and to the right.
start = (CX + 228, CY + 195)
strand = bezier(start, (CX + 470, CY + 300), (CX + 400, CY + 520))
d.line(strand, fill=WHITE, width=38, joint="curve")
dot(*start, 19)
dot(*strand[-1], 19)

for size in (180, 192, 512):
    img.resize((size, size), Image.LANCZOS).save(OUT / f"icon-{size}.png",
                                                 optimize=True)
print("icons written to", OUT)
