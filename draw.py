# draw.py — draws the news-image-20261125 front page (819x1024 PNG, v3).
#
# v3 rebuilds the layout on the feed's top entry (@hwang-steven, 99.2%):
# portrait 819x1024, navy top bar, giant Playfair masthead, red italic
# subhead, coloured region tabs, IN NUMBERS strip, 3 large heroes with
# flat illustrations + WHY IT MATTERS, 10 scenes in 2 rows of 5, map +
# ALSO ON list, red-bordered DATE CHECK, sources footer.
#
# Facts are the v2 re-research (news-image-20261125-research-v2.md) as
# corrected by the v2 audit (news-image-20261125-audit-v2.md): 35 stories,
# 7 regions, 12 fields. Heroes are ROTATED vs v2 — Tariffs (#5), Kospi
# (#7) and Shenzhou (#4) are the heroes because they carry the strongest
# flat illustrations (cargo ship, falling chip chart, space station) and
# the subhead can name all three; Dow (#1), Hormuz (#2) and UCL (#3)
# move to scenes 4-6. No story is dropped: heroes 1-3 + scenes 4-13 +
# ALSO 14-35 = all 35. Numbers on the page are OUR counts only
# (35 stories, 7 regions, 12 fields) — never the reference's 50/10/21.
# Deterministic: no network, no clock, no randomness.
# Run: python3 draw.py  ->  writes entry.png next to this file.
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 819, 1024
PAPER = (247, 241, 224)
INK = (24, 22, 18)
RED = (178, 34, 28)
DARK = (18, 28, 48)
NAVY = (16, 24, 44)
BLUE = (38, 84, 134)
GREEN = (24, 110, 58)
TAN = (222, 200, 150)
SAND = (238, 222, 182)
GREY = (110, 104, 90)
LIGHT = (255, 253, 246)
GOLD = (255, 215, 90)

FONT_DIR = os.path.join(HERE, "fonts")
PF = os.path.join(FONT_DIR, "PlayfairDisplay.ttf")
PFI = os.path.join(FONT_DIR, "PlayfairDisplay-Italic.ttf")
INTER = os.path.join(FONT_DIR, "Inter.ttf")


def _vfont(path, size, axes):
    # NOTE: RAQM/kerning was tried and measured: basic vs RAQM renders
    # are byte-identical in this Pillow build, so this build does not
    # kern. The uneven gaps in 8pt bold caps ("REPOR TED") are the Inter
    # bearings at tiny size, not a kerning bug — unchanged, see README.
    f = ImageFont.truetype(path, size)
    f.set_variation_by_axes(axes)
    return f


def pf(size, wght=900):
    """Playfair Display — high-contrast Didone display serif."""
    return _vfont(PF, size, [wght])


def pfi(size, wght=700):
    """Playfair Display Italic — subhead voice."""
    return _vfont(PFI, size, [wght])


def inter(size, wght=400):
    """Inter — clean grotesque sans for labels / body / sources."""
    return _vfont(INTER, size, [14, wght])


F_MAST = inter(11, 700)
F_SUB = None  # fitted per width below
F_SEC = inter(12, 700)
F_NUM = pf(24, 800)
F_NUMCAP = inter(8, 400)
F_HERO_H = None  # fitted
F_HERO_D = None  # fitted
F_WHY = inter(9, 700)
F_WHY_T = inter(10, 400)
F_CARD_H = None  # fitted
F_CARD_D = None  # fitted
F_SRC = inter(8, 700)
F_PLACE = inter(10, 700)
F_PILL = inter(8, 700)
F_ALSO = inter(7, 400)
F_ALSO_B = inter(7, 700)
F_DC = inter(8, 400)
F_FOOT = inter(8, 400)
F_MAP_LBL = inter(8, 700)
F_TAB = inter(10, 700)
F_LEGEND = inter(7, 400)
F_SCORE = inter(8, 700)
F_MINI = inter(8, 700)
F_MINI_S = inter(7, 400)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def line_step(fnt, extra=2):
    """True line step for a font: ascent+descent+extra.

    PIL draws text from the top of the ascender box; stepping by
    fnt.size + 2 (the v3 bug) is 4-5px short of the real glyph box for
    Playfair, so every descender (g, y, p, j) struck the line below.
    """
    a, dd = fnt.getmetrics()
    return a + dd + extra


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=2):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_step(fnt, leading)
    return y


def rule(draw, x0, y, x1, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def tracked_width(draw, text, fnt, track=1):
    w = sum(draw.textlength(ch, font=fnt) for ch in text)
    return w + track * max(0, len(text) - 1)


def draw_tracked(draw, text, fnt, x, y, fill=INK, track=1):
    """Draw ALL-CAPS kickers with letter-spacing (grotesque label voice)."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + track
    return cx


def centered_tracked(draw, text, fnt, y, fill=INK, track=2):
    w = tracked_width(draw, text, fnt, track)
    draw_tracked(draw, text, fnt, (W - w) / 2, y, fill=fill, track=track)
    return y + fnt.size


def centered(draw, text, fnt, y, fill=INK):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def fit_font(draw, text, make_font, width, max_lines, sizes):
    """Pick the largest size (from sizes, descending) whose wrap fits.

    Deterministic: pure function of the text and the font metrics.
    Returns (font, lines)."""
    for size in sizes:
        fnt = make_font(size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = make_font(sizes[-1])
    return fnt, wrap(draw, text, fnt, width)


def fit_single(draw, text, make_font, width, sizes):
    """Largest size whose text fits on ONE line. Returns (font, width)."""
    for size in sizes:
        fnt = make_font(size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
    return make_font(sizes[-1])


def draw_lines(draw, lines, fnt, x, y, fill=INK, leading=2):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_step(fnt, leading)
    return y


def section(draw, label, x, y):
    draw_tracked(draw, label, F_SEC, x, y, fill=RED, track=1)
    return y + 17


def draw_kicker(draw, num, place, x, y, w):
    """Kicker with tracked caps, shrunk (tracking, then size) until it
    fits its column. (v4: '12 · NIGERIA · NIGER STATE' at 10pt/track-1
    measured 159px in a 153px column, so it ran into the next kicker
    with only a 2px gap between them.)"""
    text = "%d · %s" % (num, place)
    for size, track in [(10, 1), (10, 0), (9, 0), (8, 0)]:
        fnt = inter(size, 700)
        if tracked_width(draw, text, fnt, track) <= w:
            draw_tracked(draw, text, fnt, x, y, fill=RED, track=track)
            return
    draw_tracked(draw, text, inter(8, 700), x, y, fill=RED, track=0)


def draw_pill(draw, text, x_right, y):
    """Small outlined verification pill, right-aligned to x_right."""
    fnt = F_PILL
    tw = draw.textlength(text, font=fnt)
    bw, bh = tw + 10, 13
    x0 = x_right - bw
    draw.rectangle([x0, y, x_right, y + bh], fill=(255, 255, 255),
                   outline=RED, width=1)
    draw.text((x0 + 5, y + 2), text, font=fnt, fill=RED)
    return x0


# ---------------------------------------------------------------- stories
# Heroes 1-3 (ROTATED vs v2): (number, place, pill, headline, dek, why,
# source, scene key). Numbers are the NEW display numbers, not the v2
# research numbers — the v2 research numbers are in the comments.
HEROES = [
    (1, "WASHINGTON · TRADE", "CONFIRMED",
     "Trump proposes new tariffs on 14 trading partners",
     "USTR proposes 20% tariff on China, 15% caps for EU, Japan, Korea, "
     "Taiwan; Malaysia 18%.",
     "Tariffs follow a Jan 25 hearing; China faces the top rate.",
     "CONFIRMED · REUTERS", "ship"),  # v2 #5
    (2, "SEOUL · MARKETS", "CONFIRMED",
     "AI doubts sink Asian chip stocks: Kospi closes \u22126.2%",
     "Kospi ends at 4,697.51; SK Hynix \u221211.1%, Samsung \u22129.9%; "
     "Nikkei \u22122.8%, Shanghai \u22122.0%.",
     "The rout wipes out Tuesday's entire 6.32% gain.",
     "CONFIRMED · YONHAP, WSJ, THE HINDU", "kospi"),  # v2 #7
    (3, "JIUQUAN, CHINA · SPACE", "CONFIRMED",
     "Pakistan's first astronaut docks at China's station",
     "Muhammad Zeeshan Ali, 40, first Pakistani in orbit; liftoff "
     "00:18:52 UTC, docking 03:56 UTC.",
     "China's station takes its first foreign astronaut.",
     "CONFIRMED · XINHUA, NATURE", "station"),  # v2 #4
]

# Scenes 4-13: (number, place, pill, headline, dek, source, scene key)
SCENES = [
    (4, "MARKETS · NEW YORK", "CONFIRMED",
     "Dow erases 1,100-point plunge",
     "Dow -1,104 to 48,913.74, then +164.25 to close +0.33% at 50,182.95.",
     "CONFIRMED · WSJ, AP, INVESTOPEDIA", "stocks"),  # v2 #1
    (5, "STRAIT OF HORMUZ", "CLAIMED",
     "Tankers hit mines in Hormuz",
     "IRGC claims 2 tankers hit mines, then an LNG carrier burns.",
     "CLAIMED · REUTERS, IRGC", "hormuz"),  # v2 #2
    (6, "CHAMPIONS LEAGUE", "CONFIRMED",
     "Lille stun Bayern, Roma end PSG's record",
     "Nine games: Lille 2-1 Bayern; PSG 2-2 Roma; Liverpool 3-0 "
     "Club Brugge.",
     "CONFIRMED · UEFA", "ucl"),  # v2 #3
    (7, "USA · WASHINGTON", "CONFIRMED",
     "US economy booms 4.3% as inflation runs hot",
     "Q3 GDP revised to 4.3%; Oct core PCE +3.3%; jobless claims 189,000.",
     "CONFIRMED · BEA, DEPT. OF LABOR, WSJ", "economy"),  # v2 #6
    (8, "YEMEN · HODEIDAH", "CONFIRMED",
     "Saudi coalition bombs Hodeidah",
     "Coalition hits Hodeidah Port, Saada and Amran after evacuation "
     "warning.",
     "CONFIRMED · SPA, ARAB NEWS, ISW", "hodeidah"),  # v2 #8
    (9, "UKRAINE · SAMARA", "OFFICIAL",
     "Ukraine drones torch two Samara oil refineries",
     "Strikes on Syzran and Kuibyshev refineries; fires at both, "
     "1 killed.",
     "OFFICIAL · UKRAINIAN GENERAL STAFF", "refinery"),  # v2 #9
    (10, "GAZA", "CONFIRMED",
     "Israeli strikes kill 5 in Gaza",
     "North Gaza security chief Abu al-Ouf, 47, wife and 2 daughters "
     "killed; 1 more in Karama.",
     "CONFIRMED · REUTERS, XINHUA", "gaza"),  # v2 #10
    (11, "MARKETS · NEW YORK", "CONFIRMED",
     "Nvidia -3.9% as Anthropic touches record low",
     "Nvidia -3.91% to $149.30; Anthropic low $73.85, 11% below its "
     "$83 IPO price.",
     "CONFIRMED · WSJ, REUTERS, FINNHUB, CNN", "nvda"),  # v2 #11
    (12, "NIGERIA · NIGER STATE", "REPORTED",
     "Militants kill at least 30 in Nigeria's Niger State",
     "Gunmen kill at least 30 and burn homes — seen as retaliation for "
     "Fulani herders killed days earlier.",
     "REPORTED · REUTERS", "nigeria"),  # v2 #12
    (13, "AUSTRALIA · CANBERRA", "CONFIRMED",
     "Australia and Solomons sign security pact",
     "Australia becomes Solomons' primary security partner; A$740m over "
     "10 years.",
     "CONFIRMED · AFP, REUTERS", "solomon"),  # v2 #13
]

# Also On Wednesday 25 November, 14-35 — numbers UNCHANGED from v2.
ALSO = [
    (14, "IRAQ", "Top court backs Baghdad deploying troops to Kurdistan borders"),
    (15, "SYRIA", "2.3 million Captagon pills seized as US praises smuggling crackdown"),
    (16, "ISRAEL", "Judges recommend dropping Netanyahu's bribery case (Case 4000)"),
    (17, "UKRAINE", "Russian ballistic missiles hit Kyiv shopping centre, 3 hurt"),
    (18, "UKRAINE", "Russian strikes halt DTEK power plant, set Naftogaz gas site ablaze"),
    (19, "COLOMBIA", "Police free 76 hostages after 17-hour supermarket siege"),
    (20, "EGYPT", "At least 31 killed, 21 injured as fuel vehicle overturns and burns"),
    (21, "INDONESIA", "Three bodies found in search for 26 believed trapped in flooded mine"),
    (22, "DAVIS CUP", "Italy edge South Korea 2-1 into semi-finals"),
    (23, "CRICKET", "Mulder's 7/31 seals South Africa's 2-0 Test sweep of Bangladesh"),
    (24, "NBA CUP", "Tatum scores 41 as Celtics beat Wizards 131-116"),
    (25, "AUSTRALIA", "Parliament passes Digital Duty of Care 97-43"),
    (26, "SOUTH AFRICA", "Court quashes Phala Phala report, halting Ramaphosa impeachment"),
    (27, "UNITED NATIONS", "Rights chief warns of atrocity-crimes risk against Palestinians"),
    (28, "CONGO", "UN peacekeepers evacuate 10 Ebola health workers trapped in fighting"),
    (29, "INDIA", "Government approves $1.2bn incentive package for construction equipment"),
    (30, "KENYA", "Cult leader Paul Mackenzie convicted on new child-cruelty charges"),
    (31, "SENEGAL", "Parliament adopts 128-9 resolution condemning Faye's budget decree"),
    (32, "UNITED STATES", "Army detonates 5 tons of lead azide in Iowa, 'a success'"),
    (33, "PUERTO RICO", "Supreme Court voids LUMA power-grid contract extension 5-4"),
    (34, "EUROPE", "STOXX 600 -1.1%, DAX -1.26% to 24,702.13, FTSE -0.38%"),
    (35, "UNITED STATES", "HP shares jump 11.4% to $31.12 after Q4 earnings beat"),
]

# Region tabs: (label, count, muted fill). Counts from research v2.
REGIONS = [
    ("N. AMERICA 8", (165, 40, 35)),
    ("AFRICA 7", (40, 90, 110)),
    ("MIDDLE EAST 7", (185, 110, 30)),
    ("EUROPE 6", (45, 70, 140)),
    ("ASIA 4", (25, 110, 85)),
    ("OCEANIA 2", (110, 80, 140)),
    ("S. AMERICA 1", (150, 120, 40)),
]

NUMBERS = [
    ("20%", "top proposed US tariff", INK),
    ("\u22126.16%", "Kospi close, worst in AI rout", RED),
    ("1,100-pt", "Dow erases 1,100-pt plunge", INK),
    ("30", "killed in Nigeria", INK),
    ("31", "killed in Egypt", INK),
]

DATE_CHECK = (
    "LEFT OUT — first reported on other days: Ghalibaf 7 conditions "
    "(24 Nov); RSF defector claims (23 Nov); Andy Taylor died (23 Nov); "
    "Russia ~490k troops toll (first 24 Nov); US consumer confidence "
    "103.3 (24 Nov); Nvidia \u22125.86%, KOSPI +6.32%, Nikkei +3.91%, US "
    "close Dow 50,018.70 (24 Nov); Houthi Riyadh tower, 11 hurt (24 Nov); "
    "IRGC tanker no. 4 claim (24 Nov); Hamas chief Naeem Abu Nahel killed "
    "(24 Nov).  NOT YET: Thanksgiving (27 Nov); F1 Qatar (29 Nov); Fed "
    "decision (8\u20139 Dec); tariffs effective Jan 2027; Davis Cup semi "
    "(28 Nov).")

FOOTER = ("Every story happened or was first reported on Wed 25 Nov 2026.  "
          "CONFIRMED = 2+ outlets · OFFICIAL = on the record · REPORTED = "
          "one outlet · CLAIMED = unverified claim.")
SOURCES = ("Sources: AP · Reuters · AFP · BBC · CNN · FT · Xinhua · UEFA · "
           "BEA · DOL · Yonhap · SPA · ISW · OHCHR · Finnhub · Investopedia.")

HOW_SURE = ("HOW SURE — CONFIRMED: 2+ outlets · OFFICIAL: on the record · "
            "REPORTED: one outlet · CLAIMED: unverified claim.")

# ---------------------------------------------------------------- hero scenes
# Large flat illustrations, one per hero (w ~260, h ~104). All drawn
# shapes + text only; no photos, no gradients, muted palette.

def draw_ship(d, x, y, w, h):
    """Container ship, tariffs hero (ref #1)."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(38, 84, 134))
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.66], fill=(255, 255, 255))
    # Containers: two rows of flat coloured boxes on the deck.
    cols = [(178, 34, 28), (38, 84, 134), (220, 170, 40), (25, 110, 85),
            (230, 120, 40), (110, 80, 140)]
    cw, ch = w / 9.0, h * 0.16
    for r in range(2):
        for c in range(8):
            cx = x + 8 + c * cw
            cy = y + h * 0.62 - ch * (2 - r) - 2
            d.rectangle([cx, cy, cx + cw - 2, cy + ch - 2],
                        fill=cols[(r * 3 + c) % len(cols)])
    # Hull.
    d.polygon([(x + 4, y + h * 0.62), (x + w - 4, y + h * 0.62),
               (x + w - 26, y + h - 6), (x + 26, y + h - 6)],
              fill=(24, 22, 18))
    d.text((x + 10, y + h - 20), "EU", font=inter(10, 700),
           fill=(255, 255, 255))
    d.text((x + w - 62, y + h - 20), "CHINA", font=inter(10, 700),
           fill=(255, 255, 255))
    # Red circle badge, top right: UP TO 20%. Small (r=20, cy=y+22) so
    # its bottom (y+42) stays clear of the CHINA label (y+44..y+57).
    # (v4b shrank the illustration 80 -> 64px but kept r=28 at cy=y+32,
    # so the badge painted over CHINA and only the 'C' peeked out.)
    cx, cy, r = x + w - 24, y + 22, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
              outline=(255, 255, 255), width=2)
    t1 = "UP TO"
    d.text((cx - d.textlength(t1, font=inter(8, 700)) / 2, cy - 13), t1,
           font=inter(8, 700), fill=(255, 255, 255))
    t2 = "20%"
    d.text((cx - d.textlength(t2, font=inter(14, 700)) / 2, cy - 3), t2,
           font=inter(14, 700), fill=(255, 255, 255))


def draw_kospi_hero(d, x, y, w, h):
    """Dark falling chip chart, Kospi hero (ref #2)."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 20))
    for i in (1, 2, 3):
        gy = y + h * i // 4
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=(50, 55, 70), width=1)
    # Line starts right of the "AI" chip so it never strikes through it.
    pts = [(x + 40, y + 16), (x + w * 0.30, y + 20), (x + w * 0.45, y + 16),
           (x + w * 0.58, y + 52), (x + w * 0.74, y + 62),
           (x + w - 12, y + h - 16)]
    d.line(pts, fill=(230, 60, 50), width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 110))
    # "AI" chip, top left.
    d.rectangle([x + 8, y + 8, x + 30, y + 24], outline=(255, 255, 255),
                width=1)
    d.text((x + 13, y + 11), "AI", font=inter(10, 700),
           fill=(255, 255, 255))
    # Label block: paint the dark background OVER the chart line first,
    # so the red line / dots can never strike through the labels.
    # (v3 drew the labels straight on the chart; the falling line
    # crossed "SAMSUNG -9.9%".)
    d.rectangle([x + w - 124, y + 6, x + w - 4, y + 58], fill=(12, 14, 20))
    d.text((x + w - 118, y + 10), "KOSPI  \u22126.2%", font=inter(11, 700),
           fill=(230, 60, 50))
    d.text((x + w - 118, y + 28), "SK HYNIX  \u221211.1%",
           font=inter(9, 400), fill=(255, 255, 255))
    d.text((x + w - 118, y + 42), "SAMSUNG  \u22129.9%",
           font=inter(9, 400), fill=(255, 255, 255))


def draw_station(d, x, y, w, h):
    """Tiangong station over Earth, Shenzhou hero (ref #3).

    Every shape is clipped to the (x, y, w, h) box: the Earth ellipse's
    bounding box ends at y + h*0.99, never below it. (First pass let the
    ellipse run to y + h*1.55, so the blue blob painted over the
    headline below the illustration.)
    """
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 36))
    for sx, sy in [(14, 10), (60, 6), (120, 14), (180, 8), (230, 16),
                   (40, 30), (200, 34), (90, 44), (150, 26)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    # Earth horizon — top arc of an ellipse exactly as wide as the
    # column, so it cannot bleed into the neighbouring hero or past the
    # page edge. (First pass used x-w*0.25 .. x+w*1.25, and the blue
    # spilled left into the Kospi hero and right off the page.)
    d.ellipse([x, y + h * 0.60, x + w, y + h * 0.99],
              fill=(38, 84, 150))
    d.ellipse([x + w * 0.15, y + h * 0.78, x + w * 0.55, y + h * 0.99],
              fill=(60, 140, 90))
    # Station: bright solar panels + white core module with a dark
    # outline, centred. (First pass used dark blue panels that vanished
    # against the dark space.)
    my = y + h * 0.36
    d.rectangle([x + w * 0.05, my - 5, x + w * 0.28, my + 5],
                fill=(70, 140, 210))
    d.rectangle([x + w * 0.64, my - 5, x + w * 0.87, my + 5],
                fill=(70, 140, 210))
    d.rectangle([x + w * 0.30, my - 7, x + w * 0.62, my + 7],
                fill=(230, 230, 225), outline=(90, 90, 90), width=1)
    d.rectangle([x + w * 0.42, my + 7, x + w * 0.50, my + 17],
                fill=(230, 230, 225), outline=(90, 90, 90), width=1)
    # Flags: Pakistan (green + white stripe) and China (red).
    d.rectangle([x + 10, y + h - 40, x + 34, y + h - 24], fill=(20, 110, 70))
    d.rectangle([x + 10, y + h - 40, x + 15, y + h - 24],
                fill=(255, 255, 255))
    d.rectangle([x + 38, y + h - 40, x + 62, y + h - 24], fill=(200, 30, 30))
    d.text((x + 10, y + h - 20), "SHENZHOU-24", font=inter(9, 700),
           fill=(255, 255, 255))
    t = "TIANGONG"
    d.text((x + w - 8 - d.textlength(t, font=inter(9, 700)), y + h - 20), t,
           font=inter(9, 700), fill=(255, 255, 255))


# ---------------------------------------------------------------- scene minis
# Compact data scenes for scenes 4-13 (w ~153, h ~40). Positions are
# relative to w so nothing spills past the card edge.

def draw_mini(d, key, x, y, w, h):
    if key == "stocks":
        d.rectangle([x, y, x + w, y + h], fill=DARK)
        for i in (1, 2):
            gy = y + h * i // 3
            d.line([(x + 4, gy), (x + w - 4, gy)], fill=(60, 72, 96), width=1)
        pts = [(x + 8, y + 5), (x + w * 0.22, y + 7),
               (x + w * 0.40, y + 6), (x + w * 0.55, y + h * 0.58),
               (x + w * 0.72, y + h * 0.52), (x + w - 8, y + 10)]
        d.line(pts, fill=(230, 60, 50), width=2, joint="curve")
        d.text((x + 6, y + h - 11), "DOW +0.33%  ·  S&P -0.25%  ·  NSDQ -0.62%",
               font=inter(6, 700), fill=(120, 220, 140))
    elif key == "hormuz":
        d.rectangle([x, y, x + w, y + h], fill=SAND)
        d.polygon([(x, y + h * 0.45), (x + w, y + h * 0.32),
                   (x + w, y + h * 0.72), (x, y + h * 0.85)],
                  fill=(120, 170, 205))
        d.text((x + 6, y + 3), "3\u20134 CLAIMED", font=inter(8, 700), fill=RED)
        for i, tx in enumerate([0.22, 0.50, 0.78]):
            cx, cy = x + w * tx, y + h * (0.52 + 0.05 * (i % 2))
            d.rectangle([cx - 10, cy - 3, cx + 10, cy + 3], fill=(30, 30, 30))
            d.polygon([(cx - 4, cy - 8), (cx, cy - 15), (cx + 4, cy - 8)],
                      fill=(230, 110, 30))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=RED)
        d.text((x + 5, y + h - 11), "3-4 SHIPS CLAIMED · NO VERIFICATION",
               font=inter(7, 700), fill=(255, 255, 255))
    elif key == "ucl":
        d.rectangle([x, y, x + w, y + h], fill=(14, 60, 38))
        d.text((x + 6, y + 1), "MATCHDAY 5 · 9 RESULTS", font=inter(7, 700),
               fill=(255, 215, 90))
        f_row = inter(6, 400)
        cols = [
            ["LIL 2-1 BAY", "PSG 2-2 ROM", "LIV 3-0 BRU"],
            ["BAR 4-1 SAB", "SPO 2-2 MUN", "INT 2-0 STU"],
            ["ATL 2-0 VIK", "SHA 0-1 FEN", "SLA 0-1 VIL"],
        ]
        for ci, col in enumerate(cols):
            cx = x + 6 + ci * (w // 3)
            ry = y + 12
            for row in col:
                d.text((cx, ry), row, font=f_row, fill=(255, 255, 255))
                ry += 7
    elif key == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
        for sx, sy in [(10, 5), (34, 3), (70, 6), (110, 4), (140, 8)]:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.polygon([(x + 18, y + 3), (x + 13, y + 13), (x + 23, y + 13)],
                  fill=(220, 220, 220))
        d.rectangle([x + 13, y + 13, x + 23, y + 24], fill=(240, 240, 240))
        d.polygon([(x + 16, y + 24), (x + 18, y + 28), (x + 20, y + 24)],
                  fill=(255, 140, 40))
        d.text((x + 32, y + 5), "TIANGONG", font=inter(8, 700),
               fill=(255, 215, 90))
        d.text((x + 32, y + 18), "1ST PAKISTANI ABOARD", font=inter(7, 700),
               fill=(255, 255, 255))
    elif key == "tariff":
        d.rectangle([x, y, x + w, y + h], fill=(150, 20, 20))
        d.rectangle([x + 4, y + 3, x + int(w * 0.60), y + h - 3],
                    fill=(245, 245, 240))
        d.text((x + 8, y + 5), "20% CHINA", font=inter(9, 700), fill=RED)
        d.text((x + 8, y + 19), "15% EU · JP · KR · TW", font=inter(7, 700),
               fill=INK)
        d.text((x + int(w * 0.60) + 6, y + 5), "14", font=inter(14, 700),
               fill=(255, 255, 255))
        d.text((x + int(w * 0.60) + 6, y + 22), "PARTNERS", font=inter(7, 700),
               fill=(255, 220, 220))
    elif key == "economy":
        d.rectangle([x, y, x + w, y + h], fill=DARK)
        d.text((x + 8, y + 2), "Q2 3.4%", font=inter(7, 700),
               fill=(255, 255, 255))
        d.text((x + 44, y + 2), "Q3 4.3%", font=inter(7, 700),
               fill=(120, 220, 140))
        d.rectangle([x + 10, y + h - 11, x + 34, y + h - 4],
                    fill=(120, 170, 205))
        d.rectangle([x + 44, y + h - 15, x + 68, y + h - 4],
                    fill=(120, 220, 140))
        d.text((x + 92, y + 2), "GDP 4.3%", font=inter(9, 700),
               fill=(120, 220, 140))
        d.text((x + 92, y + 16), "CORE PCE 3.3%", font=inter(7, 700),
               fill=(255, 255, 255))
    elif key == "kospi":
        d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
        pts = [(x + 5, y + 7), (x + 45, y + 9), (x + 85, y + 7),
               (x + 120, y + 24), (x + w - 5, y + 27)]
        d.line(pts, fill=RED, width=2, joint="curve")
        d.text((x + 5, y + h - 12), "KOSPI -6.16%", font=inter(8, 700),
               fill=RED)
        t = "SAMSUNG -9.87%"
        d.text((x + w - 4 - d.textlength(t, font=inter(7, 700)), y + h - 11),
               t, font=inter(7, 700), fill=INK)
    elif key == "hodeidah":
        d.rectangle([x, y, x + w, y + h], fill=SAND)
        d.rectangle([x + 5, y + 16, x + 58, y + h - 2], fill=(90, 86, 78))
        d.rectangle([x + 62, y + 20, x + 92, y + h - 2], fill=(120, 116, 108))
        d.polygon([(x + 108, y + 2), (x + 114, y + 12), (x + 120, y + 2)],
                  fill=(230, 110, 30))
        d.polygon([(x + 126, y + 7), (x + 132, y + 17), (x + 138, y + 7)],
                  fill=(230, 110, 30))
        d.text((x + 6, y + 3), "HODEIDAH PORT", font=inter(8, 700), fill=RED)
    elif key == "refinery":
        d.rectangle([x, y, x + w, y + h], fill=(40, 40, 44))
        for i, tx in enumerate([0.15, 0.45, 0.75]):
            cx = x + w * tx
            d.rectangle([cx - 13, y + 12, cx + 13, y + h - 4],
                        fill=(90, 90, 96))
            d.polygon([(cx - 3, y + 10), (cx, y + 2), (cx + 3, y + 10)],
                      fill=(230, 110, 30))
        d.text((x + 5, y + h - 11), "2 REFINERIES HIT", font=inter(7, 700),
               fill=(255, 255, 255))
    elif key == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=SAND)
        d.polygon([(x, y + h), (x + w * 0.25, y), (x + w * 0.38, y),
                   (x + w * 0.16, y + h)], fill=(120, 170, 205))
        d.ellipse([x + w // 2 - 3, y + 6, x + w // 2 + 3, y + 12], fill=RED)
        d.ellipse([x + w // 2 + 9, y + 15, x + w // 2 + 14, y + 20], fill=RED)
        d.text((x + w - 58, y + 3), "5 KILLED", font=inter(8, 700), fill=RED)
        d.text((x + w - 58, y + 16), "GAZA", font=inter(8, 700), fill=INK)
    elif key == "nvda":
        d.rectangle([x, y, x + w, y + h], fill=DARK)
        pts = [(x + 5, y + 2), (x + 50, y + 4), (x + 90, y + 3),
               (x + 120, y + 7), (x + w - 5, y + 9)]
        d.line(pts, fill=(230, 60, 50), width=2, joint="curve")
        d.text((x + 5, y + 12), "NVIDIA -3.91% TO $149.30", font=inter(8, 700),
               fill=(255, 120, 110))
        d.text((x + 5, y + 23), "ANTHROPIC LOW $73.85", font=inter(8, 700),
               fill=(255, 255, 255))
    elif key == "nigeria":
        d.rectangle([x, y, x + w, y + h], fill=(200, 190, 170))
        d.rectangle([x + 5, y + 14, x + 44, y + h - 2], fill=(70, 66, 60))
        d.rectangle([x + 47, y + 18, x + 76, y + h - 2], fill=(90, 86, 78))
        d.ellipse([x + 11, y + 3, x + 23, y + 12], fill=(150, 145, 135))
        d.text((x + 86, y + 2), "30 KILLED", font=inter(8, 700), fill=RED)
        d.text((x + 86, y + 15), "NIGER STATE", font=inter(7, 700), fill=INK)
    elif key == "solomon":
        d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
        d.rectangle([x, y, x + w // 2, y + h], fill=(30, 80, 160))
        d.rectangle([x + w // 2, y, x + w, y + h], fill=(0, 120, 80))
        d.text((x + 8, y + 2), "A$740m", font=inter(9, 700),
               fill=(255, 255, 255))
        d.text((x + 8, y + 16), "AUSTRALIA", font=inter(7, 700),
               fill=(255, 255, 255))
        d.text((x + w // 2 + 8, y + 2), "SOLOMONS", font=inter(9, 700),
               fill=(255, 255, 255))
        d.text((x + w // 2 + 8, y + 16), "CANBERRA", font=inter(7, 700),
               fill=(255, 255, 255))


# ---------------------------------------------------------------- world map
NA = [(-168, 66), (-150, 70), (-140, 70), (-125, 71), (-115, 73), (-105, 73),
      (-95, 80), (-85, 73), (-80, 73), (-75, 72), (-68, 62), (-60, 55),
      (-55, 47), (-60, 44), (-65, 44), (-70, 42), (-74, 39), (-76, 35),
      (-80, 32), (-81, 26), (-84, 24), (-87, 21), (-90, 21), (-92, 15),
      (-95, 16), (-97, 16), (-100, 20), (-105, 20), (-110, 24), (-114, 29),
      (-120, 34), (-124, 40), (-125, 48), (-130, 55), (-140, 60), (-150, 59),
      (-158, 58), (-165, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-55, 70), (-45, 70), (-35, 68), (-25, 70), (-22, 74),
             (-30, 76), (-45, 77), (-58, 76), (-60, 70)]
SA = [(-79, 9), (-77, 7), (-75, 10), (-72, 12), (-64, 10), (-60, 8),
      (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22),
      (-48, -27), (-52, -32), (-58, -38), (-65, -41), (-68, -50), (-70, -54),
      (-73, -50), (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-79, -8),
      (-81, -4), (-80, 2), (-79, 9)]
AFRICA = [(-17, 15), (-16, 20), (-12, 28), (-10, 31), (-6, 34), (-1, 35),
          (3, 37), (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31),
          (34, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 11), (51, 2),
          (48, -2), (44, -8), (40, -12), (36, -18), (33, -25), (28, -33),
          (20, -35), (17, -32), (15, -27), (13, -20), (12, -15), (13, -8),
          (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-4, 48), (-1, 46), (-2, 49),
          (0, 51), (3, 52), (5, 53), (7, 55), (8, 57), (10, 59), (13, 56),
          (18, 56), (21, 55), (24, 58), (26, 60), (23, 65), (18, 66),
          (14, 67), (10, 64), (5, 60), (5, 58), (0, 55), (-3, 54), (-5, 50),
          (-5, 48), (-8, 43), (-10, 39), (-10, 36)]
ASIA = [(28, 62), (32, 66), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73),
        (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
        (150, 70), (160, 69), (170, 67), (178, 66), (178, 62), (170, 60),
        (162, 56), (158, 52), (156, 50), (150, 45), (142, 45), (141, 40),
        (140, 35), (135, 33), (130, 32), (127, 30), (122, 28), (120, 23),
        (118, 22), (112, 21), (108, 18), (105, 10), (103, 8), (100, 7),
        (98, 10), (95, 15), (92, 21), (89, 22), (86, 20), (83, 17), (80, 13),
        (77, 8), (75, 10), (73, 16), (72, 20), (70, 23), (67, 25), (62, 25),
        (58, 26), (56, 27), (52, 28), (50, 29), (48, 30), (46, 30), (44, 29),
        (42, 31), (40, 36), (38, 36), (36, 36), (34, 36), (32, 38), (30, 41),
        (28, 45), (28, 52), (28, 58), (28, 62)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (148, -39), (150, -37), (153, -32), (153, -27),
             (150, -23), (146, -19), (143, -15), (142, -11), (140, -13),
             (136, -12), (132, -12), (130, -13), (126, -14), (122, -17),
             (118, -20), (114, -21), (113, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51),
      (-5, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (140, 36), (141, 38),
         (142, 42), (140, 44), (138, 40), (136, 37), (133, 35), (130, 33)]
ISLANDS = [(95, 5), (100, 0), (105, -2), (110, -5), (115, 0), (120, -3),
           (125, 0), (130, -2), (135, -4), (140, -5)]

# (number, lon, lat, dx, dy) — NEW v3 numbering: 1 tariffs (Washington),
# 2 Kospi (Seoul), 3 Shenzhou (Jiuquan), 4 Dow (New York), 5 Hormuz,
# 6 UCL (Lille), 7 GDP (Washington), 8 Hodeidah, 9 Samara, 10 Gaza,
# 11 Nvidia (New York), 12 Nigeria, 13 Solomon (Canberra).
# dx/dy nudge the pin circle off the true point where two stories share
# one city (1/7 Washington, 4/11 New York).
PINS = [
    (1, -77, 39, 0, 0), (2, 127, 37.5, 0, 0), (3, 100.3, 39.8, 0, 0),
    (4, -74, 40.7, 0, 0), (5, 56.5, 26.5, 0, 0), (6, 3.1, 50.6, 0, 0),
    (7, -77, 39, 16, -13), (8, 42.9, 14.8, 0, 0), (9, 50.1, 53.2, 0, 0),
    (10, 34.5, 31.5, 0, 0), (11, -74, 40.7, -18, 11),
    (12, 6, 10, 0, 0), (13, 149.1, -35.3, -10, -8),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in (NA, GREENLAND, SA, AFRICA, EUROPE, ASIA, AUSTRALIA, UK, JAPAN):
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN,
                  outline=(150, 130, 95))
    for lon, lat in ISLANDS:
        cx, cy = proj(lon, lat)
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=TAN)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (cx, cy)], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        tw = d.textlength(label, font=F_MAP_LBL)
        d.text((cx - tw / 2, cy - 5), label, font=F_MAP_LBL,
               fill=(255, 255, 255))

# ---------------------------------------------------------------- layout
MX = 10            # side margin
IW = W - 2 * MX    # 799 inner width
RX = W - MX        # 809 right edge


def draw_hero_card(d, num, place, pill, headline, dek, why, source, scene,
                   x, y, w):
    draw_kicker(d, num, place, x, y, w)
    draw_pill(d, pill, x + w, y - 1)
    sy = y + 14
    if scene == "ship":
        draw_ship(d, x, sy, w, 64)
    elif scene == "kospi":
        draw_kospi_hero(d, x, sy, w, 64)
    else:
        draw_station(d, x, sy, w, 64)
    hy = sy + 64 + 4
    fnt, lines = fit_font(d, headline, lambda s: pf(s, 800), w, 2,
                          [18, 17, 16])
    hy = draw_lines(d, lines, fnt, x, hy, leading=2)
    dy = hy + 4
    fnt_d, lines_d = fit_font(d, dek, lambda s: inter(s, 400), w, 2, [10, 9])
    dy = draw_lines(d, lines_d, fnt_d, x, dy, leading=2)
    # WHY IT MATTERS — red label + sentence, max 2 lines.
    wy = dy + 4
    label = "WHY IT MATTERS"
    lw = sum(d.textlength(ch, font=F_WHY) for ch in label) + 1 * (
        len(label) - 1)
    draw_tracked(d, label, F_WHY, x, wy, fill=RED, track=1)
    first_w = w - lw - 8
    words = why.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=F_WHY_T) <= first_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            first_w = w
    if cur:
        lines.append(cur)
    d.text((x + lw + 8, wy), lines[0], font=F_WHY_T, fill=INK)
    wy2 = wy + line_step(F_WHY_T, 2)
    for line in lines[1:2]:
        d.text((x, wy2), line, font=F_WHY_T, fill=INK)
        wy2 += line_step(F_WHY_T, 2)
    # Source line.
    sy2 = wy2 + 4
    d.text((x, sy2), source, font=F_SRC, fill=RED)
    return sy2 + line_step(F_SRC, 2)


def draw_scene_card(d, num, place, pill, headline, dek, source, scene,
                    x, y, w):
    draw_kicker(d, num, place, x, y, w)
    sy = y + 13
    draw_mini(d, scene, x, sy, w, 34)
    hy = sy + 34 + 3
    fnt, lines = fit_font(d, headline, lambda s: pf(s, 800), w, 2, [13, 12])
    hy = draw_lines(d, lines, fnt, x, hy, leading=2)
    dy = hy + 2
    fnt_d, lines_d = fit_font(d, dek, lambda s: inter(s, 400), w, 2, [9, 8])
    dy = draw_lines(d, lines_d, fnt_d, x, dy, leading=2)
    src = source
    f_src = F_SRC
    while d.textlength(src, font=f_src) > w and f_src.size > 6:
        f_src = inter(f_src.size - 1, 700)
    d.text((x, dy + 4), src, font=f_src, fill=RED)
    return dy + 4 + line_step(f_src, 2)


# ALSO headlines, shortened to fit one 7pt line per item in a 240px
# column (the full facts stay in the research file; this is an index).
ALSO_SHORT = [
    (14, "IRAQ", "Top court backs Baghdad troops on Kurdistan borders"),
    (15, "SYRIA", "2.3m Captagon pills seized as US praises crackdown"),
    (16, "ISRAEL", "Judges: drop Netanyahu bribery case (Case 4000)"),
    (17, "UKRAINE", "Russian missiles hit Kyiv mall, 3 hurt"),
    (18, "UKRAINE", "Russian strikes halt DTEK plant, hit Naftogaz site"),
    (19, "COLOMBIA", "Police free 76 hostages after 17-hour siege"),
    (20, "EGYPT", "31 killed, 21 hurt as fuel vehicle overturns and burns"),
    (21, "INDONESIA", "26 believed trapped; 3 bodies found in mine"),
    (22, "DAVIS CUP", "Italy edge South Korea 2-1 into semi-finals"),
    (23, "CRICKET", "Mulder 7/31 seals SA's 2-0 Test sweep of Bangladesh"),
    (24, "NBA CUP", "Tatum scores 41 as Celtics beat Wizards 131-116"),
    (25, "AUSTRALIA", "Parliament passes Digital Duty of Care 97-43"),
    (26, "SOUTH AFRICA", "Court quashes Phala Phala report"),
    (27, "UNITED NATIONS", "UN rights chief warns of atrocity risk"),
    (28, "CONGO", "UN evacuates 10 Ebola workers trapped in fighting"),
    (29, "INDIA", "India approves $1.2bn incentive package"),
    (30, "KENYA", "Mackenzie convicted on child-cruelty charges"),
    (31, "SENEGAL", "128-9 vote condemns Faye's budget decree"),
    (32, "UNITED STATES", "Army detonates 5 tons of lead azide"),
    (33, "PUERTO RICO", "Court voids LUMA power-grid contract 5-4"),
    (34, "EUROPE", "STOXX -1.1%, DAX -1.26%, FTSE -0.38%"),
    (35, "UNITED STATES", "HP shares jump 11.4% to $31.12"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)

    # --- Top bar (navy), like the reference.
    d.rectangle([MX, MX, RX, 34], fill=NAVY)
    draw_tracked(d, "THE WORLD IN ONE DAY", F_MAST, 16, 17, fill=GOLD,
                 track=2)
    top_right = ("35 STORIES · 7 REGIONS · 12 FIELDS · ALL FIRST REPORTED "
                 "ON WEDNESDAY 25 NOVEMBER 2026")
    f_tr = inter(8, 700)
    d.text((RX - 6 - d.textlength(top_right, font=f_tr), 18), top_right,
           font=f_tr, fill=(255, 255, 255))

    # --- Masthead — the date IS the masthead. Its line box is
    # ascent+descent tall; the subhead starts below that box + 4px, so
    # descenders (the 'y' in Wednesday) can never touch it. (v3 put the
    # subhead at a fixed y=106 while the 54pt date box ended at y~113.)
    date_y = 36
    f_date = fit_single(d, "Wednesday 25 November 2026",
                        lambda s: pf(s, 900), IW, [50, 48, 46, 44])
    centered(d, "Wednesday 25 November 2026", f_date, date_y)
    sub_y = date_y + line_step(f_date, 0) + 4
    sub = ("US proposes tariffs on 14 economies · AI doubts sink Asian "
           "chip stocks · Pakistan's first astronaut docks at Tiangong")
    f_sub = fit_single(d, sub, lambda s: pfi(s, 700), IW, [13, 12, 11, 10])
    centered(d, sub, f_sub, sub_y, fill=RED)
    rule_y = sub_y + line_step(f_sub, 0) + 6
    rule(d, 12, rule_y, W - 12, width=2)
    rule(d, 12, rule_y + 4, W - 12, width=1)

    # --- Region tabs, equal widths, muted fills.
    y = rule_y + 8
    widths = [114, 114, 114, 114, 114, 114, 115]
    tx = MX
    for (label, color), tw in zip(REGIONS, widths):
        d.rectangle([tx, y, tx + tw, y + 18], fill=color)
        lw = d.textlength(label, font=F_TAB)
        d.text((tx + (tw - lw) / 2, y + 4), label, font=F_TAB,
               fill=(255, 255, 255))
        tx += tw

    # --- THE DAY IN NUMBERS — Playfair numerals, 5 columns. Captions
    # are ONE line each now (v3 wrapped to 2 lines and the 2nd line
    # touched the rule below the strip).
    y = y + 18 + 4
    section(d, "THE DAY IN NUMBERS", MX, y)
    ncol_w = IW // 5
    for i, (num, cap, color) in enumerate(NUMBERS):
        cx = MX + i * ncol_w
        d.text((cx, y + 16), num, font=F_NUM, fill=color)
        d.text((cx, y + 50), cap, font=F_NUMCAP, fill=INK)
        if i:
            d.line([(cx - 4, y + 16), (cx - 4, y + 60)],
                   fill=(200, 192, 172))
    rule(d, 12, y + 62, W - 12)

    # --- Heroes 1-3. Height is MEASURED, not assumed: the rule below
    # sits under the TALLEST hero card, so no hero text can cross it.
    hy = y + 68
    hero_w = (IW - 20) // 3
    hero_bottoms = []
    for i, (num, place, pill, headline, dek, why, source, scene) in \
            enumerate(HEROES):
        hero_bottoms.append(draw_hero_card(
            d, num, place, pill, headline, dek, why, source, scene,
            MX + i * (hero_w + 10), hy, hero_w))
    hy_end = max(hero_bottoms)
    rule(d, 12, hy_end + 6, W - 12)

    # --- Scenes 4-13, two rows of five. Row 2 starts 10px below the
    # TALLEST row-1 card, so a row-1 source line can never strike the
    # row-2 kicker. (v3 used a fixed 130px row: row-1 sources spilled
    # 2-10px past it and printed over the row-2 kickers.)
    ry = hy_end + 14
    scene_w = (IW - 4 * 8) // 5
    row1_bottoms = []
    for col in range(5):
        num, place, pill, headline, dek, source, scene = SCENES[col]
        row1_bottoms.append(draw_scene_card(
            d, num, place, pill, headline, dek, source, scene,
            MX + col * (scene_w + 8), ry, scene_w))
    ry2 = max(row1_bottoms) + 8
    row2_bottoms = []
    for col in range(5):
        num, place, pill, headline, dek, source, scene = SCENES[5 + col]
        row2_bottoms.append(draw_scene_card(
            d, num, place, pill, headline, dek, source, scene,
            MX + col * (scene_w + 8), ry2, scene_w))
    scenes_end = max(row2_bottoms)
    rule(d, 12, scenes_end + 6, W - 12)

    # --- Bottom: map (left) + ALSO ON (right).
    y = scenes_end + 12
    section(d, "WHERE IT HAPPENED", MX, y)
    section(d, "ALSO ON WEDNESDAY 25 NOVEMBER", 322, y)
    by = y + 18
    draw_map(d, MX, by, 300, 88)
    # Map legend: coloured dots + region names, two rows.
    ly = by + 92
    leg = [("N. America", REGIONS[0][1]), ("Africa", REGIONS[1][1]),
           ("Middle East", REGIONS[2][1]), ("Europe", REGIONS[3][1]),
           ("Asia", REGIONS[4][1]), ("Oceania", REGIONS[5][1]),
           ("S. America", REGIONS[6][1])]
    for j, (name, color) in enumerate(leg):
        row2 = j // 4
        col2 = j % 4
        ex = MX + col2 * 78
        ey = ly + row2 * 11
        d.ellipse([ex, ey + 1, ex + 6, ey + 7], fill=color)
        d.text((ex + 9, ey), name, font=F_LEGEND, fill=INK)
    # HOW SURE box under the map.
    hy2 = ly + 22
    d.rectangle([MX, hy2, 310, hy2 + 32], outline=INK, width=1)
    hs_end = draw_wrapped(d, HOW_SURE, inter(7, 400), MX + 5, hy2 + 4, 290,
                          leading=3)
    assert hs_end <= hy2 + 32, "HOW SURE box overflow"
    # ALSO ON list, two columns of 11 one-line items. 10px step for
    # 7pt Inter (line box 9px) so lines can never touch. (v3 used 8.5.)
    cols = [ALSO_SHORT[0:11], ALSO_SHORT[11:22]]
    for ci, col in enumerate(cols):
        cy = by
        for num, place, headline in col:
            pre = "%d. %s \u2014 " % (num, place)
            fb, fh = F_ALSO_B, F_ALSO
            if (d.textlength(pre, font=fb)
                    + d.textlength(headline, font=fh) > 244):
                fb, fh = inter(6, 700), inter(6, 400)
            d.text((322 + ci * 244, cy), pre, font=fb, fill=INK)
            d.text((322 + ci * 244 + d.textlength(pre, font=fb), cy),
                   headline, font=fh, fill=INK)
            cy += 10
    bottom_y = max(hy2 + 32, by + 11 * 10)

    # --- DATE CHECK, red-bordered box, full width. Height fits its
    # lines at 12px step (7pt line box 9px + 3px clearance).
    y = bottom_y + 8
    f_dc = inter(7, 400)
    dc_lines = wrap(d, DATE_CHECK, f_dc, IW - 90)
    dc_h = 6 + len(dc_lines) * line_step(f_dc, 2) + 6
    d.rectangle([MX, y, RX, y + dc_h], outline=RED, width=1)
    d.text((MX + 6, y + 6), "DATE CHECK", font=inter(8, 700), fill=RED)
    dy = y + 6
    for line in dc_lines:
        d.text((MX + 78, dy), line, font=f_dc, fill=INK)
        dy += line_step(f_dc, 2)
    dc_end = y + dc_h

    # --- Footer, 11px step for 7pt lines (line box 9px).
    f_foot = inter(7, 400)
    fy = dc_end + 2
    centered(d, FOOTER, f_foot, fy)
    centered(d, SOURCES, f_foot, fy + line_step(f_foot, 2))
    final_y = fy + line_step(f_foot, 2) + line_step(f_foot, 0)
    print("final y:", final_y, "of", H)
    print("hero bottoms:", hero_bottoms, "row1:", row1_bottoms,
          "row2:", row2_bottoms, "bottom_y:", bottom_y,
          "dc lines:", len(dc_lines))
    assert final_y <= H - 10, "page overflow: final y %d" % final_y

    img.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
