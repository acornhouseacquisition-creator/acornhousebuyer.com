"""Draws the PNG icons and the 1200x630 social share image. Needs Pillow (pip install pillow)."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GREEN, GREEN_D, ACORN, CAP, CREAM = (31, 77, 58), (22, 58, 44), (200, 134, 47), (232, 180, 106), (255, 248, 236)
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def acorn(d, x, y, s):
    """Acorn with a little house cut out, inside a box of size s at (x, y)."""
    u = s / 64
    d.rectangle([x + 29 * u, y + 7 * u, x + 35 * u, y + 15 * u], fill=CAP)
    d.chord([x + 10 * u, y + 11 * u, x + 54 * u, y + 39 * u], 180, 360, fill=CAP)
    d.pieslice([x + 12 * u, y + 0 * u, x + 52 * u, y + 54 * u], 0, 180, fill=ACORN)
    d.polygon([(x + 26 * u, y + 41 * u), (x + 32 * u, y + 36 * u), (x + 38 * u, y + 41 * u),
               (x + 38 * u, y + 49 * u), (x + 26 * u, y + 49 * u)], fill=CREAM)


def icon(size, name, rounded=True):
    im = Image.new("RGBA", (size * 4, size * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=size * 4 * 14 // 64 if rounded else 0, fill=GREEN)
    acorn(d, 0, size * 4 * 0.06, size * 4)
    im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name))


icon(32, "favicon-32.png")
icon(180, "apple-touch-icon.png", rounded=False)
icon(512, "icon-512.png")
icon(512, "assets/logo.png")

og = Image.new("RGB", (1200, 630), GREEN)
d = ImageDraw.Draw(og)
for i in range(630):  # soft diagonal gradient
    t = i / 630
    d.line([(0, i), (1200, i)], fill=tuple(int(GREEN_D[k] + (GREEN[k] - GREEN_D[k]) * t) for k in range(3)))
acorn(d, 80, 70, 150)
d.text((250, 105), "Acorn House Buyer", font=ImageFont.truetype(BOLD, 54), fill=(255, 255, 255))
d.text((250, 170), "acornhousebuyer.com", font=ImageFont.truetype(REG, 30), fill=CAP)
d.text((80, 270), "We Buy Houses for Cash", font=ImageFont.truetype(BOLD, 76), fill=(255, 255, 255))
d.text((80, 360), "in North Carolina", font=ImageFont.truetype(BOLD, 76), fill=CAP)
d.text((80, 470), "Any condition  •  No repairs  •  No commissions  •  Close on your date",
       font=ImageFont.truetype(REG, 30), fill=(230, 238, 233))
d.rounded_rectangle([80, 535, 470, 595], radius=12, fill=ACORN)
d.text((104, 548), "(704) 246-3399", font=ImageFont.truetype(BOLD, 34), fill=(255, 255, 255))
og.save(os.path.join(ROOT, "assets/og-image.png"), optimize=True)
print("images done")
