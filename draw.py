#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world
news of Friday 20 November 2026.

Pure Pillow drawing, no downloaded assets, so the image is entirely our
own work. Run: python3 draw.py
Writes entry.png next to this file (1024x1024, well under 1 MiB).

Every story was checked against news reports published on 20 November
2026 (The Hindu, Reuters, Nikkei Asia, Al Jazeera / CNA, ESPN, AP).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (18, 24, 38)
RED = (178, 24, 24)
MUTED = (96, 101, 114)
CARD = (255, 255, 255)
RULE = (203, 196, 180)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_KICKER = font("DejaVuSans-Bold.ttf", 21)
F_DATE = font("DejaVuSerif-Bold.ttf", 52)
F_DEK = font("DejaVuSerif.ttf", 22)
F_TAG = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSerif-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 16)

# (tag, chip colour, headline, summary)
STORIES = [
    ("WEATHER · INDIA", (21, 101, 150),
     "Cyclone Akvan bears down on India",
     "300,000 people evacuated to shelters ahead of landfall "
     "due at noon; winds gusting to 110 km/h."),
    ("DIPLOMACY · USA", (178, 24, 24),
     "Trump puts Iran decision off to 2027",
     "President says the US will \u201csee what happens\u201d after "
     "January 1, with no rush to decide."),
    ("BUSINESS · TECH", (23, 120, 70),
     "Anthropic\u2019s record IPO closes 17% up",
     "Shares end first day at $97.17 after pricing at $83; "
     "$81bn raised \u2014 the biggest IPO ever."),
    ("EUROPE · UKRAINE", (124, 58, 237),
     "Europe \u201cready to enter negotiations\u201d",
     "Berlin summit backs talks with Russia; Kushner says "
     "Moscow is \u201ccomfortable\u201d with NATO-style guarantees."),
    ("USA · SPORT", (154, 52, 18),
     "Trump pardons baseball legend Pete Rose",
     "Posthumous pardon for MLB\u2019s all-time hits leader "
     "\u2014 4,256 hits, banned since 1989."),
    ("WORLD · ANIMALS", (101, 67, 33),
     "Fiona the hippo dies at nine",
     "Cincinnati Zoo\u2019s beloved hippo dies after swallowing "
     "a visitor\u2019s hat; vets\u2019 efforts fail."),
]


def wrap(draw, text, font_obj, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font_obj) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 36
    x0, x1 = margin, W - margin

    # ---- Masthead ----
    y = 30
    d.text((x0, y), "THE WORLD IN ONE PAGE", font=F_KICKER, fill=RED)
    y += 30
    d.text((x0, y), "Friday, 20 November 2026", font=F_DATE, fill=INK)
    y += 66
    d.text((x0, y), "Six stories that defined the day, from New Delhi to Washington.",
           font=F_DEK, fill=MUTED)
    y += 34
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    y += 6
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 18

    # ---- Story grid: 2 columns x 3 rows ----
    gap = 20
    col_w = (x1 - x0 - gap) // 2
    row_h = 236
    footer_h = 44
    top = y
    for i, (tag, colour, head, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + gap)
        cy = top + row * (row_h + gap)
        d.rounded_rectangle([cx, cy, cx + col_w, cy + row_h],
                            radius=10, fill=CARD, outline=RULE, width=1)
        px = cx + 20
        py = cy + 16
        # tag chip
        chip_w = d.textlength(tag, font=F_TAG) + 18
        d.rounded_rectangle([px, py, px + chip_w, py + 28],
                            radius=6, fill=colour)
        d.text((px + 9, py + 5), tag, font=F_TAG, fill=WHITE)
        py += 42
        # headline, up to 2 lines
        for line in wrap(d, head, F_HEAD, col_w - 40)[:2]:
            d.text((px, py), line, font=F_HEAD, fill=INK)
            py += 36
        py += 6
        # summary, up to 3 lines
        for line in wrap(d, body, F_BODY, col_w - 40)[:3]:
            d.text((px, py), line, font=F_BODY, fill=MUTED)
            py += 27

    # ---- Footer ----
    fy = top + 3 * row_h + 2 * gap + 14
    d.line([(x0, fy), (x1, fy)], fill=RULE, width=1)
    d.text((x0, fy + 10),
           "Sources: The Hindu \u00b7 Reuters \u00b7 Nikkei Asia \u00b7 Al Jazeera \u00b7 ESPN \u00b7 AP  |  20 Nov 2026",
           font=F_FOOT, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
