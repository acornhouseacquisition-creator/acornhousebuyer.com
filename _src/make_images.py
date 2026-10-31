"""Makes the logo sizes, icons and the 1200x630 share image from _src/brand/logo-source.webp.
Needs Pillow (pip install pillow)."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
GOLD, BLACK = (244, 180, 20), (10, 10, 10)

src = Image.open(os.path.join(ROOT, "_src/brand/logo-source.webp")).convert("RGBA")
src = src.crop(src.getchannel("A").getbbox())
W, H = src.size


def light_version(im):
    """Black letters become white for dark backgrounds; the gold stays gold."""
    out = im.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and r < 120:
                px[x, y] = (255, 255, 255, a)
    return out


def sized(im, height):
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def save_png(im, name):
    im.save(os.path.join(ROOT, name), optimize=True)


light = light_version(src)
save_png(sized(src, 180), "assets/logo-header.png")  # shown at 60px tall, sharp on retina screens
save_png(sized(light, 180), "assets/logo-light.png")
save_png(sized(src, 400), "assets/logo.png")         # for Google business data

# Acorn cut from the logo: the columns around the stem, above the gold line
ACORN_BOX = (round(W * .405), 0, round(W * .605), round(H * .79))
acorn = src.crop(ACORN_BOX)
acorn = acorn.crop(acorn.getchannel("A").getbbox())


def icon(size, name):
    s = size * 4
    im = Image.new("RGBA", (s, s), (255, 255, 255, 255))
    a = sized(acorn, round(s * .84))
    im.alpha_composite(a, ((s - a.width) // 2, (s - a.height) // 2))
    save_png(im.convert("RGB").resize((size, size), Image.LANCZOS), name)


icon(32, "favicon-32.png")
icon(48, "favicon-48.png")
icon(180, "apple-touch-icon.png")
icon(512, "icon-512.png")

og = Image.new("RGBA", (1200, 630), BLACK + (255,))
d = ImageDraw.Draw(og)
logo = sized(light, 250)
og.alpha_composite(logo, ((1200 - logo.width) // 2, 55))
def centered(text, font, y, fill):
    d.text(((1200 - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)
centered("We Buy Houses for Cash in North Carolina", ImageFont.truetype(BOLD, 46), 345, (255, 255, 255))
centered("Any condition  •  No repairs  •  No commissions", ImageFont.truetype(REG, 32), 418, (225, 225, 225))
phone_font = ImageFont.truetype(BOLD, 36)
pw = d.textlength("(704) 246-3399", font=phone_font)
d.rounded_rectangle([(1200 - pw) / 2 - 30, 495, (1200 + pw) / 2 + 30, 565], radius=12, fill=GOLD)
centered("(704) 246-3399", phone_font, 510, BLACK)
save_png(og.convert("RGB"), "assets/og-image.png")
print("images done", src.size, "acorn", acorn.size)
