#!/usr/bin/env python3
"""Draw the v2 front page: THE WORLD IN ONE DAY, Friday 21 November 2026.

Build-time script (PIL). Produces entry.png next to this file; the judged
program main.py only copies entry.png to /output. Design: v1 broadsheet
kept, leads replaced with the full day's news (NATO Article 4 + AI rout),
kickers on every headline, schematic Poland impact map, plunging market
chart, big stat callouts, Rutte pull quote, LATE EDITION footer.
Deterministic: no network, no randomness, no timestamps in the output.
"""
import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
M = 28
RIGHT = W - M

BG = (246, 241, 226)
PANEL = (253, 251, 245)
INK = (24, 24, 24)
GRAY = (92, 92, 92)
FAINT = (196, 188, 168)
GOLD = (176, 128, 10)
NATO = (42, 75, 141)
CRASH = (178, 34, 34)
CRASH_SOFT = (238, 183, 175)
TEAL = (0, 105, 105)
PURPLE = (95, 60, 140)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if tw(trial, font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, maxw, leading, fill=INK, max_lines=None):
    lines = wrap(text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(y, color=GOLD, width=2):
    d.line([(M, y), (RIGHT, y)], fill=color, width=width)


def kicker_bar(x, y, w, color, text):
    d.rectangle([x, y, x + w, y + 27], fill=color)
    d.text((x + 10, y + 5), text, font=F(SANS_B, 15), fill=(255, 255, 255))
    return y + 27


# ---------------------------------------------------------------- masthead
f_title = F(SERIF_B, 53)
title = "THE WORLD IN ONE DAY"
d.text(((W - tw(title, f_title)) / 2, 12), title, font=f_title, fill=INK)
rule(82, GOLD, 3)
rule(88, INK, 1)
f_date = F(SANS_B, 16)
d.text((M, 96), "FRIDAY, 21 NOVEMBER 2026", font=f_date, fill=INK)
mid = "ALL THE DAY'S NEWS ON ONE PAGE"
f_mid = F(SANS, 13)
d.text(((W - tw(mid, f_mid)) / 2, 98), mid, font=f_mid, fill=GRAY)
late = "LATE EDITION"
d.text((RIGHT - tw(late, f_date), 96), late, font=f_date, fill=CRASH)
rule(122, INK, 1)

# ---------------------------------------------------------------- lead one
LX, LW = M, 470
RX = 526
TOP = 134
d.line([(512, TOP), (512, 660)], fill=FAINT, width=1)

y = kicker_bar(LX, TOP, LW, NATO, "NATO ALERT - ARTICLE 4 INVOKED")
f_head = F(SANS_B, 37)
y = block(LX, y + 8, "RUSSIAN MISSILES FALL ON POLAND", f_head, LW, 41)
f_deck = F(SERIF, 18)
y = block(LX, y + 3, "Warsaw triggers NATO's Article 4 after the heaviest "
          "Russian strike of November", f_deck, LW, 22, fill=(60, 60, 60))

# schematic map of Poland with three impact points in the south-east
MAP_Y, MAP_H = 306, 190
d.rectangle([LX, MAP_Y, LX + LW, MAP_Y + MAP_H], fill=PANEL, outline=INK,
            width=1)
poly = [(70, 66), (150, 34), (252, 22), (348, 44), (414, 92), (428, 150),
        (382, 182), (286, 190), (188, 178), (112, 150), (58, 112)]
pts = [(LX + 16 + px * 0.98, MAP_Y + 6 + py) for px, py in poly]
d.polygon(pts, fill=(232, 236, 240), outline=NATO)
d.text((LX + 120, MAP_Y + 84), "POLAND", font=F(SANS_B, 17), fill=NATO)
d.text((LX + 414, MAP_Y + 138), "UKRAINE", font=F(SANS, 11), fill=GRAY)
# compass
cx, cy = LX + 40, MAP_Y + 30
d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=INK, width=1)
d.polygon([(cx, cy - 11), (cx - 4, cy + 2), (cx + 4, cy + 2)], fill=CRASH)
d.text((cx - 4, cy - 26), "N", font=F(SANS_B, 11), fill=INK)
# invasion arrow from the east
ay = MAP_Y + 96
d.line([(LX + LW - 4, ay), (LX + 372, ay)], fill=CRASH, width=3)
d.polygon([(LX + 372, ay), (LX + 388, ay - 6), (LX + 388, ay + 6)],
          fill=CRASH)
impacts = [(LX + 356, MAP_Y + 128), (LX + 392, MAP_Y + 148),
           (LX + 330, MAP_Y + 156)]
for ix, iy in impacts:
    d.ellipse([ix - 15, iy - 15, ix + 15, iy + 15], outline=CRASH, width=1)
    star = []
    for k in range(16):
        r = 8 if k % 2 == 0 else 3
        a = math.pi * k / 8
        star.append((ix + r * math.cos(a), iy + r * math.sin(a)))
    d.polygon(star, fill=CRASH)
f_lab = F(SANS, 11)
d.text((LX + 238, MAP_Y + 108), "Nowy Lipowiec", font=f_lab, fill=INK)
d.text((LX + 352, MAP_Y + 170), "Rudnik n. Sanem", font=f_lab, fill=INK)
d.text((LX + 196, MAP_Y + 150), "Molodycz", font=f_lab, fill=INK)
d.text((LX + 10, MAP_Y + MAP_H - 18),
       "Three impacts in the south-east - no casualties",
       font=F(SANS, 12), fill=GRAY)

# stat callout + Rutte pull quote
SY = 504
d.text((LX, SY), "515", font=F(SANS_B, 56), fill=CRASH)
qx = LX + 128
d.text((qx, SY + 2), "\u201cA grave violation\u201d", font=F(SERIF, 20),
       fill=NATO)
d.text((qx, SY + 30), "of allied airspace", font=F(SERIF, 20), fill=NATO)
d.text((qx, SY + 56), "- Mark Rutte, NATO Secretary General,",
       font=F(SANS, 12), fill=GRAY)
d.text((qx, SY + 71), "flying into Warsaw on Saturday",
       font=F(SANS, 12), fill=GRAY)
f_body = F(SANS, 15)
block(LX, 592, "One night, 515 weapons - 27 ballistic, 84 cruise, "
      "404 drones. Kyiv bridge destroyed; eight killed, 28 wounded. "
      "Tusk: deliberate provocation. Poland seeks AWACS and F-35 jets.",
      f_body, LW, 17, max_lines=4)

# ---------------------------------------------------------------- lead two
y = kicker_bar(RX, TOP, LW, CRASH, "MARKETS CRASH - AI ROUT DEEPENS")
y = block(RX, y + 8, "AI ROUT ERASES 2026 STOCK GAINS", f_head, LW, 41)
y = block(RX, y + 3, "The Nasdaq's worst point plunge in years closes a "
          "brutal week for technology shares", f_deck, LW, 22,
          fill=(60, 60, 60))

CH_Y, CH_H = 306, 190
d.rectangle([RX, CH_Y, RX + LW, CH_Y + CH_H], fill=PANEL, outline=INK,
            width=1)
d.text((RX + 12, CH_Y + 8), "NASDAQ COMPOSITE - ONE DAY",
       font=F(SANS_B, 12), fill=GRAY)
curve = [(RX + 18, CH_Y + 52), (RX + 90, CH_Y + 44), (RX + 150, CH_Y + 66),
         (RX + 205, CH_Y + 58), (RX + 262, CH_Y + 96),
         (RX + 320, CH_Y + 88), (RX + 378, CH_Y + 132),
         (RX + 448, CH_Y + 168)]
d.polygon(curve + [(RX + 448, CH_Y + CH_H - 8), (RX + 18, CH_Y + CH_H - 8)],
          fill=CRASH_SOFT)
d.line(curve, fill=CRASH, width=4)
ex, ey = curve[-1]
d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=CRASH)
d.text((RX + 300, CH_Y + 150), "\u25bc 1,261 pts", font=F(SANS_B, 17),
       fill=CRASH)
d.text((RX + 12, CH_Y + CH_H - 20), "Second-biggest point drop on record",
       font=F(SANS, 12), fill=GRAY)

d.text((RX, SY), "-5.28%", font=F(SANS_B, 56), fill=CRASH)
qx = RX + 226
d.text((qx, SY + 2), "The Nasdaq's one-day fall.", font=F(SERIF, 16),
       fill=INK)
d.text((qx, SY + 26), "Nvidia -14%, Broadcom -12.2%,", font=F(SERIF, 16),
       fill=INK)
d.text((qx, SY + 50), "Micron -13.9%, AMD -13.2%", font=F(SERIF, 16),
       fill=INK)
block(RX, 592, "Nvidia hit a 52-week low as the SEC reviews its books; "
      "$2.7 trillion gone since the peak. Anthropic slid 8.5% a day "
      "after history's biggest IPO. S&P 500 in correction (-11.6%); "
      "VIX closed at 35.89.", f_body, LW, 17, max_lines=4)


# ---------------------------------------------------------------- grid
d.text((M, 666), "THE DAY IN EIGHT STORIES", font=F(SANS_B, 16), fill=NATO)
rule(686, GOLD, 2)

GRID = [
    ("WORLD", NATO, "TRUMP DELAYS IRAN STRIKE CALL TO 2027",
     "\u201cWe've got time.\u201d War cost $48.3B; four tankers hit in "
     "Hormuz in 96 hours."),
    ("WORLD", NATO, "ICJ MYANMAR RULING RIPPLES OUTWARD",
     "Britain expels a Myanmar diplomat; Gaza case vs Israel may gain "
     "weight."),
    ("EUROPE", TEAL, "UK AND EU SEAL LANDMARK RESET DEAL",
     "London and Brussels agree to rebuild ties a decade after Brexit."),
    ("WORLD", NATO, "US, CHINA, RUSSIA IN SHENZHEN PACT",
     "Xi and Putin's joint declaration takes aim at the ICC in The "
     "Hague."),
    ("WAR", CRASH, "EU ADDS \u20ac1BN FOR UKRAINE'S SKIES",
     "Extra drones and air defence pledged; Britain sends 1,000+ "
     "long-range drones."),
    ("WAR", CRASH, "UKRAINE HITS RUSSIAN LAUNCHERS",
     "Three missile launchers destroyed; HIMARS strike on 810th "
     "Brigade HQ, Sumy."),
    ("TECH", PURPLE, "TRUMP: NO AI DATA CENTRES ABROAD?",
     "Threat to bar US firms building AI sites overseas rattles the "
     "sector."),
    ("TECH", PURPLE, "ANTHROPIC 'SOLVES' MATH PROBLEM",
     "Lab claims the year's biggest open maths problem on its worst "
     "day."),
]

GY = 694
CELL_W, CELL_H, GAP = 234, 108, 10
f_tab = F(SANS_B, 10)
f_ghead = F(SANS_B, 16)
f_gsub = F(SANS, 12)
for i, (tab, color, head, sub) in enumerate(GRID):
    col, row = i % 4, i // 4
    x = M + col * (CELL_W + GAP)
    yy = GY + row * (CELL_H + 8)
    tabw = tw(tab, f_tab) + 14
    d.rectangle([x, yy, x + tabw, yy + 17], fill=color)
    d.text((x + 7, yy + 3), tab, font=f_tab, fill=(255, 255, 255))
    hy = block(x, yy + 23, head, f_ghead, CELL_W, 19, max_lines=2)
    block(x, hy + 3, sub, f_gsub, CELL_W, 14, fill=(60, 60, 60),
          max_lines=3)

# ---------------------------------------------------------------- in brief
BY = 926
d.text((M, BY), "IN BRIEF", font=F(SANS_B, 15), fill=NATO)
d.line([(M + 74, BY + 8), (RIGHT, BY + 8)], fill=FAINT, width=1)
BRIEFS = [
    "US releases Middle East UFO footage",
    "Denmark: Russia plotted rapper killing",
    "California eyes AI kill-switch powers",
    "Mamdani to close Rikers Island by 2032",
    "UN cuts food aid target for 2027",
    "Climate priorities set before COP31",
]
BW = 154
f_brief = F(SANS, 12)
for i, item in enumerate(BRIEFS):
    x = M + i * (BW + 8)
    if i % 2 == 0:
        d.rectangle([x - 4, BY + 24, x + BW, BY + 62], fill=(240, 234, 216))
    d.polygon([(x + 1, BY + 30), (x + 1, BY + 38), (x + 8, BY + 34)],
              fill=CRASH)
    block(x + 13, BY + 26, item, f_brief, BW - 14, 15, max_lines=2)

# ---------------------------------------------------------------- footer
rule(990, INK, 1)
d.text((M, 996), "LATE EDITION", font=F(SANS_B, 14), fill=CRASH)
foot = "ONE PAGE - EVERY STORY THAT MATTERED"
f_foot = F(SANS, 11)
d.text(((W - tw(foot, f_foot)) / 2, 998), foot, font=f_foot, fill=GRAY)
vol = "VOL CXII - NO 312"
d.text((RIGHT - tw(vol, f_foot), 998), vol, font=f_foot, fill=GRAY)


def main():
    out_path = os.path.join(HERE, "entry.png")
    img.save(out_path, format="PNG", optimize=True)
    data = open(out_path, "rb").read()
    print("wrote %s %d bytes sha256 %s" % (
        out_path, len(data), hashlib.sha256(data).hexdigest()))
    if len(data) > 1048576:
        print("ERROR: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
