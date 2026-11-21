#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Renders a 1024x1024 broadsheet front page with Pillow and the Liberation
fonts: masthead, date banner, two lead panels with shape pictograms, a
grid of eight stories and an IN BRIEF strip. No network, no randomness,
no timestamps in the output, so repeated runs are byte-identical.
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/liberation/"

PAGE = 1024
PAPER = (247, 245, 240)
CARD = (255, 253, 247)
INK = (17, 17, 17)
MUTED = (96, 92, 80)
RED = (178, 34, 34)
NAVY = (27, 58, 88)
STEEL = (120, 138, 158)
FAINT = (205, 198, 180)
BANNER = (27, 58, 88)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, font, width):
    """Split text into lines that fit width, word by word."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def block(draw, x, y, text, font, fill, width, max_lines, leading):
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, font, width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def radar(draw, box):
    """Concentric sweep rings, a short incoming trajectory, an impact star."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    radius = min(x1 - x0, y1 - y0) // 2 - 6
    for step in range(3):
        r = radius - step * radius // 3
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=STEEL, width=2)
    tip_x, tip_y = cx + radius // 2, cy - radius // 2
    draw.line([x0 + 10, y0 + 8, tip_x, tip_y], fill=RED, width=3)
    draw.polygon(
        [(tip_x, tip_y), (tip_x - 12, tip_y - 2), (tip_x - 4, tip_y + 10)],
        fill=RED,
    )
    ix, iy = cx - radius // 2, cy + radius // 2
    for dx, dy in ((-13, 0), (13, 0), (0, -13), (0, 13), (-9, -9), (9, 9),
                   (-9, 9), (9, -9)):
        draw.line([ix, iy, ix + dx, iy + dy], fill=RED, width=2)
    draw.ellipse([ix - 4, iy - 4, ix + 4, iy + 4], fill=RED)


def chart(draw, box):
    """Two numeric callouts above a stepped market decline."""
    x0, y0, x1, y1 = box
    draw.text((x0 + 6, y0), "NASDAQ  -5.28%",
              font=load(SANS_B, 24), fill=RED)
    right_text = "NVIDIA  -14%"
    rw = draw.textlength(right_text, font=load(SANS_B, 24))
    draw.text((x1 - rw - 4, y0), right_text,
              font=load(SANS_B, 24), fill=RED)
    top = y0 + 34
    base = y1 - 6
    draw.line([x0 + 6, top, x0 + 6, base], fill=STEEL, width=2)
    draw.line([x0 + 6, base, x1 - 6, base], fill=STEEL, width=2)
    pts = []
    w = (x1 - x0 - 24) // 5
    for i, drop in enumerate((0, 1, 1, 2, 3, 4)):
        px = x0 + 10 + i * w
        py = top + 4 + drop * (base - top - 12) // 4
        pts.append((px, py))
    for i in range(len(pts) - 1):
        draw.line([pts[i][0], pts[i][1], pts[i + 1][0], pts[i][1]],
                  fill=RED, width=3)
        draw.line([pts[i + 1][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]],
                  fill=RED, width=3)
    for px, py in pts[1:]:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)


LEADS = [
    {
        "kicker": "POLAND  ·  NATO",
        "headline": "Russian missiles land in Poland",
        "summary": ("Two missiles and a drone crash in the south-east during a "
                    "huge barrage on Ukraine. PM Tusk calls it a deliberate "
                    "provocation; NATO chief Rutte calls it a grave violation "
                    "and visits Warsaw today."),
        "art": radar,
    },
    {
        "kicker": "MARKETS",
        "headline": "Wall Street rout as AI sell-off deepens",
        "summary": ("The S&P 500 and Dow enter correction; the Nasdaq falls "
                    "5.28% and Nvidia drops 14%. Tokyo's Nikkei slides "
                    "5.06% and gold falls about 4%."),
        "art": chart,
    },
]

GRID = [
    ("THE HAGUE", "World Court: Myanmar committed genocide",
     "ICJ rules 9-6 over the Rohingya; a first for a state."),
    ("SHENZHEN", "Summit ends with little to show",
     "Joint declaration issued, few concrete results."),
    ("MEDICINE", "Pill hailed as cancer breakthrough",
     "Tumours stop growing in nearly all patients."),
    ("INDIA", "Cyclone Akvan hits Odisha coast",
     "Storm crosses near Gopalpur; 300,000 evacuated."),
    ("BRUSSELS", "UK and EU sign three deals",
     "Food trade, carbon markets, youth mobility."),
    ("RIYADH", "Houthi missiles intercepted",
     "Three ballistic missiles downed; Hodeidah struck."),
    ("CLIMATE", "COP31 enters final stretch",
     "Fossil-fuel wording split as talks near a deal."),
    ("COPENHAGEN", "Denmark foils Russian plot",
     "Plan to kill rapper Kyivstoner was stopped."),
]

BRIEFS = [
    "Trump urges Nvidia to bring back Huang; board says no.",
    "Trump pardons baseball star Pete Rose posthumously.",
    "Senate rejects the Iran war-powers resolution, 51-48.",
    "US approves nearly 880,000 AI chip sales to China.",
    "Webb and Gemini North find the oldest close quasar pair.",
    "Gold hits a 14-month low, down 9.4% on the week.",
]


def draw_page():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    margin = 30
    right = PAGE - margin

    # Masthead.
    title = "THE WORLD IN ONE DAY"
    title_font = load(SERIF_B, 56)
    tw = d.textlength(title, font=title_font)
    d.text(((PAGE - tw) / 2, 24), title, font=title_font, fill=INK)
    d.line([margin, 92, right, 92], fill=INK, width=2)

    # Date banner.
    d.rectangle([margin, 102, right, 140], fill=BANNER)
    date_font = load(SANS_B, 27)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = d.textlength(date, font=date_font)
    d.text(((PAGE - dw) / 2, 108), date, font=date_font, fill=(255, 255, 255))
    d.line([margin, 148, right, 148], fill=RED, width=3)

    # Lead panels.
    top = 160
    height = 330
    gap = 20
    width = (right - margin - gap) // 2
    for i, lead in enumerate(LEADS):
        x = margin + i * (width + gap)
        d.rectangle([x, top, x + width, top + height], fill=CARD,
                    outline=FAINT, width=1)
        inner = x + 16
        iw = width - 32
        y = top + 14
        d.text((inner, y), lead["kicker"], font=load(SANS_B, 19), fill=RED)
        y += 30
        y = block(d, inner, y, lead["headline"], load(SERIF_B, 38), INK,
                  iw, 2, 44)
        y += 6
        art_top = y
        art_bottom = top + height - 116
        lead["art"](d, (inner, art_top, x + width - 16, art_bottom))
        y = art_bottom + 8
        block(d, inner, y, lead["summary"], load(SANS, 20), INK, iw, 4, 25)

    # Section label.
    y = 506
    d.text((margin, y), "MORE OF THE DAY", font=load(SANS_B, 20), fill=NAVY)
    d.line([margin + 168, y + 12, right, y + 12], fill=FAINT, width=1)

    # Story grid: two columns, four rows.
    gy = 536
    cell_w = (right - margin - gap) // 2
    cell_h = 76
    for i, (kicker, headline, summary) in enumerate(GRID):
        col = i % 2
        row = i // 2
        x = margin + col * (cell_w + gap)
        cy = gy + row * (cell_h + 4)
        d.text((x, cy), kicker, font=load(SANS_B, 16), fill=RED)
        block(d, x, cy + 20, headline, load(SERIF_B, 23), INK, cell_w, 1, 27)
        block(d, x, cy + 48, summary, load(SANS, 17), MUTED, cell_w, 1, 20)

    # IN BRIEF strip.
    by = 856
    d.line([margin, by, right, by], fill=INK, width=2)
    d.text((margin, by + 10), "IN BRIEF", font=load(SANS_B, 19), fill=NAVY)
    rows = 3
    for i, item in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x = margin + col * (cell_w + gap)
        yy = by + 38 + row * 26
        d.text((x, yy), "■  " + item, font=load(SANS, 18), fill=INK)

    # Footer.
    foot = ("All stories as reported on Saturday 21 November 2026  ·  "
            "Sources: AP, Reuters, BBC, The Guardian, PBS")
    foot_font = load(SANS, 15)
    fw = d.textlength(foot, font=foot_font)
    d.text(((PAGE - fw) / 2, 988), foot, font=foot_font, fill=MUTED)
    return img


def main():
    out_path = os.path.join(HERE, "entry.png")
    page = draw_page()
    page.save(out_path, format="PNG", optimize=True)
    data = open(out_path, "rb").read()
    print("wrote %s %d bytes sha256 %s" % (
        out_path, len(data), hashlib.sha256(data).hexdigest()))
    if len(data) > 1048576:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
