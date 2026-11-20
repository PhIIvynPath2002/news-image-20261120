#!/usr/bin/env python3
"""Draw the improved (v2) entry.png for news-image-20261120.

A one-page newspaper front page summing up the world news of
Friday 20 November 2026, built from the full day's reporting:
the morning's stories corrected with their outcomes, plus the
daytime and evening stories the morning edition missed.

Layout: masthead, one full-width lead story, a 2x2 grid, and a
full-width bottom strip -- six verified stories in all.

Every story below was checked against reports published on
20 November 2026 (BBC / One Turn, Reuters, SCMP, IMD, NDTV,
France 24 / DW). Run: python3 draw.py
Writes entry.png next to this file (1024x1024, under 1 MiB).
Pure Pillow drawing, no downloaded assets.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 23, 37)
RED = (176, 23, 23)
MUTED = (94, 99, 112)
CARD = (255, 255, 255)
LEAD_CARD = (253, 246, 232)
RULE = (201, 194, 178)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_KICKER = font("DejaVuSans-Bold.ttf", 21)
F_DATE = font("DejaVuSerif-Bold.ttf", 50)
F_DEK = font("DejaVuSerif.ttf", 22)
F_TAG = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 33)
F_LEAD_BODY = font("DejaVuSans.ttf", 21)
F_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 20)
F_STRIP_HEAD = font("DejaVuSerif-Bold.ttf", 26)
F_STRIP_BODY = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 16)

LEAD = ("JUSTICE · THE HAGUE", (124, 58, 237),
        "World Court: Myanmar committed genocide",
        "The ICJ rules 9\u20136 that Myanmar\u2019s 2017 campaign against the "
        "Rohingya was genocide \u2014 the first such ruling against a state.")

# (tag, chip colour, headline, summary)
GRID = [
    ("WEATHER · INDIA", (21, 101, 150),
     "Cyclone Akvan makes landfall",
     "Storm crosses the coast near Gopalpur at 70\u201380 km/h after "
     "weakening; 300,000 evacuated, no major damage reported."),
    ("CONFLICT · UKRAINE", (178, 24, 24),
     "Russian barrage hits Kyiv embassies",
     "Daytime missiles damage a cathedral and the Austrian and Dutch "
     "missions; Brussels summons Moscow\u2019s envoy."),
    ("MIDDLE EAST · SAUDI ARABIA", (154, 52, 18),
     "Houthi missile hits Riyadh\u2019s tallest tower",
     "Windows blown out across eight floors of the PIF tower in the "
     "financial district; no injuries reported."),
    ("MARKETS · GLOBAL", (23, 120, 70),
     "Stocks slide as AI doubts spread",
     "Nikkei falls 4.8% and the S&P drops for a fifth day; Anthropic\u2019s "
     "record debut ends 17% up but fails to lift tech."),
]

STRIP = ("USA · CYBER", (21, 101, 150),
         "White House fires its cyber chief",
         "Cyber Director Sean Cairncross is out after a week of outages; "
         "Kirsten Davies steps in.")


def wrap(draw, text, font_obj, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
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


def chip(draw, x, y, tag, colour):
    """Draw a coloured tag chip; returns its width."""
    w = draw.textlength(tag, font=F_TAG) + 18
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=6, fill=colour)
    draw.text((x + 9, y + 5), tag, font=F_TAG, fill=WHITE)
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 36
    x0, x1 = margin, W - margin

    # ---- Masthead ----
    y = 28
    d.text((x0, y), "THE WORLD IN ONE PAGE", font=F_KICKER, fill=RED)
    y += 30
    d.text((x0, y), "Friday, 20 November 2026", font=F_DATE, fill=INK)
    y += 62
    d.text((x0, y), "The full day\u2019s news: the morning\u2019s stories, "
                    "and what the day added.",
           font=F_DEK, fill=MUTED)
    y += 34
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    y += 6
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # ---- Lead story, full width ----
    ly = y + 16
    lead_h = 188
    d.rounded_rectangle([x0, ly, x1, ly + lead_h],
                        radius=10, fill=LEAD_CARD, outline=RULE, width=1)
    px = x0 + 20
    py = ly + 16
    tag, colour, head, body = LEAD
    chip(d, px, py, tag, colour)
    py += 42
    for line in wrap(d, head, F_LEAD_HEAD, x1 - x0 - 40)[:1]:
        d.text((px, py), line, font=F_LEAD_HEAD, fill=INK)
        py += 42
    py += 4
    for line in wrap(d, body, F_LEAD_BODY, x1 - x0 - 40)[:2]:
        d.text((px, py), line, font=F_LEAD_BODY, fill=MUTED)
        py += 28

    # ---- 2x2 grid ----
    gap = 18
    col_w = (x1 - x0 - gap) // 2
    row_h = 228
    top = ly + lead_h + gap
    for i, (tag, colour, head, body) in enumerate(GRID):
        col = i % 2
        row = i // 2
        cx = x0 + col * (col_w + gap)
        cy = top + row * (row_h + gap)
        d.rounded_rectangle([cx, cy, cx + col_w, cy + row_h],
                            radius=10, fill=CARD, outline=RULE, width=1)
        px = cx + 20
        py = cy + 16
        chip(d, px, py, tag, colour)
        py += 42
        for line in wrap(d, head, F_HEAD, col_w - 40)[:2]:
            d.text((px, py), line, font=F_HEAD, fill=INK)
            py += 34
        py += 6
        for line in wrap(d, body, F_BODY, col_w - 40)[:3]:
            d.text((px, py), line, font=F_BODY, fill=MUTED)
            py += 27

    # ---- Bottom strip, full width ----
    sy = top + 2 * row_h + gap
    strip_h = 86
    d.rounded_rectangle([x0, sy, x1, sy + strip_h],
                        radius=10, fill=CARD, outline=RULE, width=1)
    px = x0 + 20
    py = sy + 14
    tag, colour, head, body = STRIP
    chip_w = chip(d, px, py, tag, colour)
    d.text((px + chip_w + 14, py + 2),
           head, font=F_STRIP_HEAD, fill=INK)
    d.text((px, py + 44), body, font=F_STRIP_BODY, fill=MUTED)

    # ---- Footer ----
    fy = sy + strip_h + 14
    d.line([(x0, fy), (x1, fy)], fill=RULE, width=1)
    d.text((x0, fy + 10),
           "Sources: BBC \u00b7 Reuters \u00b7 SCMP \u00b7 One Turn \u00b7 IMD \u00b7 NDTV  |  20 Nov 2026",
           font=F_FOOT, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
