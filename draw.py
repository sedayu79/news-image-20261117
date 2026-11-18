#!/usr/bin/env python3
"""Draw entry.png for the 17 November 2026 world-news image bounty.

A clean newspaper-style infographic: masthead with the day, six story
blocks across the Middle East, Europe and Asia, and an "in brief" strip.
Run: python3 draw.py  ->  writes entry.png (1024x1024) next to this file.
Only the Python standard library plus Pillow are used; the sandbox entry
point (main.py) is separate and only copies the finished image.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
CARD = (255, 255, 255)
CARD_LINE = (205, 198, 178)
RED = (166, 43, 31)
MUTE = (96, 90, 78)

TAG_COLORS = {
    "MIDDLE EAST": (140, 47, 57),
    "EUROPE": (31, 78, 121),
    "ASIA": (46, 107, 79),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


STORIES = [
    (
        "MIDDLE EAST",
        "Iran drones hit U.S. radar base in Bahrain",
        "Bahrain says it intercepted the attack; no casualties "
        "or damage reported.",
    ),
    (
        "MIDDLE EAST",
        "Iran \u2018dirty bomb\u2019 plot in Washington",
        "U.S. officials told CNN of plans to hit senior Trump "
        "officials. Unconfirmed.",
    ),
    (
        "EUROPE",
        "Ukraine badly damages Kerch bridge to Crimea",
        "Kerch bridge badly damaged, Ukraine says; Russia hit "
        "Kyiv\u2019s bridges, cutting heat, water, power.",
    ),
    (
        "ASIA",
        "Trump heads to Asia for APEC summit",
        "Trump travels to Shenzhen for the APEC summit; a meeting "
        "with Xi and Putin is set for 19 Nov.",
    ),
    (
        "MIDDLE EAST",
        "Third U.S. carrier reaches the Middle East",
        "USS Theodore Roosevelt is the third U.S. carrier here. "
        "A tanker was hit near the Strait of Hormuz.",
    ),
    (
        "EUROPE",
        "U.K. sanctions Israeli settlement builders",
        "Eight settlement builders blacklisted; a 72-year-old "
        "woman was killed near Jericho, officials say.",
    ),
]

IN_BRIEF = (
    "Also in brief \u2014 Japan scrambled jets as suspected Russian "
    "planes entered its airspace."
)


def draw_card(draw, x, y, w, h, tag, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=2)
    pad = 18
    tx, ty = x + pad, y + 12
    # tag chip
    chip = TAG_COLORS[tag]
    tf = font(SANS_B, 21)
    tw = draw.textlength(tag, font=tf)
    draw.rectangle([tx, ty, tx + tw + 18, ty + 30], fill=chip)
    draw.text((tx + 9, ty + 4), tag, font=tf, fill=(255, 255, 255))
    ty += 42
    # headline (29px serif bold)
    hf = font(SERIF, 29)
    head_lines = wrap(draw, headline, hf, w - 2 * pad)
    # body: 24px, shrink to 22px if the block would overflow the card
    for bsize in (24, 22):
        bf = font(SANS, bsize)
        body_lines = wrap(draw, body, bf, w - 2 * pad)
        need = 42 + len(head_lines) * 35 + 4 + len(body_lines) * (bsize + 6)
        if need <= h - 24 or bsize == 22:
            break
    for line in head_lines:
        draw.text((tx, ty), line, font=hf, fill=INK)
        ty += 35
    ty += 4
    for line in body_lines:
        draw.text((tx, ty), line, font=bf, fill=(48, 48, 48))
        ty += bsize + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead band ----
    draw.rectangle([0, 0, W, 160], fill=INK)
    draw.text(
        (W // 2, 22),
        "T H E   W O R L D   I N   O N E   D A Y",
        font=font(SANS_B, 25),
        fill=(214, 196, 160),
        anchor="ma",
    )
    draw.text(
        (W // 2, 56),
        "TUESDAY, 17 NOVEMBER 2026",
        font=font(SERIF, 52),
        fill=(255, 255, 255),
        anchor="ma",
    )
    draw.text(
        (W // 2, 118),
        "Six stories that defined the day \u2014 as reported",
        font=font(SERIF_REG, 24),
        fill=(200, 200, 200),
        anchor="ma",
    )
    draw.rectangle([0, 160, W, 166], fill=RED)

    # ---- story grid: 2 columns x 3 rows ----
    margin = 36
    gutter = 20
    col_w = (W - 2 * margin - gutter) // 2
    grid_top = 186
    grid_bottom = 900
    row_h = (grid_bottom - grid_top - 2 * gutter) // 3
    for i, (tag, headline, body) in enumerate(STORIES):
        cx = margin + (i % 2) * (col_w + gutter)
        cy = grid_top + (i // 2) * (row_h + gutter)
        draw_card(draw, cx, cy, col_w, row_h, tag, headline, body)

    # ---- in-brief strip ----
    by = 918
    draw.rectangle([margin, by, W - margin, by + 44], fill=(232, 226, 208))
    bf = font(SANS, 21)
    draw.text((margin + 14, by + 10), IN_BRIEF, font=bf, fill=INK)

    # ---- footer ----
    draw.text(
        (W // 2, 978),
        "Events of 17 November 2026, as reported that day. "
        "Claims marked \u2018officials say\u2019 are unconfirmed.",
        font=font(SANS, 20),
        fill=MUTE,
        anchor="ma",
    )

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
