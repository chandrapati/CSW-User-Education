#!/usr/bin/env python3
"""Generate the CSW Learning Journey island map for the User Education README.

15 themed stops laid out in learning-path order (Overview -> Incident Response),
connected by a dotted "hop across the islands" trail from START to MASTERY.
Small sand islands with large, prominent icons on top; no numbering.
Rendered at 2x and downsampled for crisp, anti-aliased output.
All original artwork; no Cisco copyrighted assets.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

# ---- canvas (layout space; drawing is supersampled by S) ----
S = 2
W, H = 1280, 820

# ---- palette ----
SKY_TOP   = (233, 245, 252)
SKY_BOT   = (205, 231, 246)
WAVE      = (196, 224, 242)
NAVY      = (12, 33, 78)
NAVY_2    = (20, 47, 100)
CYAN      = (33, 176, 235)
BLUE      = (0, 114, 206)      # Cisco blue
BLUE_DK   = (0, 78, 150)
WHITE     = (255, 255, 255)
SAND      = (247, 235, 205)
SAND_HI   = (252, 245, 224)
SAND_EDGE = (228, 208, 160)
SAND_SH   = (183, 205, 222)    # island shadow on water
TRUNK     = (150, 110, 66)
LEAF      = (52, 160, 92)
LEAF_DK   = (36, 132, 74)
GREEN     = (56, 168, 88)
GREEN_DK  = (38, 132, 66)
ROCK      = (128, 140, 150)
ROCK_DK   = (98, 110, 120)
LABEL     = (23, 46, 84)

FONT  = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
BOLDF = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Black.ttf"]


def _f(cands, size):
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def font(s): return _f(FONT, int(s * S))
def bold(s): return _f(BOLDF, int(s * S))


class Canvas:
    """Scales all coordinates/sizes by S so layout math stays in 1280x820 space."""

    def __init__(self, draw):
        self.d = draw

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def line(self, pts, fill, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, int(width * S)), joint="curve")

    def ellipse(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = box
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill,
                       outline=outline, width=max(1, int(width * S)))

    def polygon(self, pts, fill=None, outline=None, width=1):
        self.d.polygon(self._p(pts), fill=fill, outline=outline, width=max(1, int(width * S)))

    def rrect(self, box, radius, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = box
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=radius * S,
                                 fill=fill, outline=outline, width=max(1, int(width * S)))

    def arc(self, box, start, end, fill, width=1):
        x0, y0, x1, y1 = box
        self.d.arc([x0 * S, y0 * S, x1 * S, y1 * S], start, end, fill=fill,
                   width=max(1, int(width * S)))

    def text(self, xy, s, f, fill, anchor="mm"):
        self.d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


# ------------------------------------------------------------- big icons ----
def icon(c, kind, cx, cy):
    """Large (~60px), clean icon centered at (cx, cy)."""
    col, dk, wt = BLUE, BLUE_DK, WHITE

    if kind == "overview":                 # monitor + play
        c.rrect([cx - 30, cy - 24, cx + 30, cy + 12], 6, fill=col)
        c.rrect([cx - 25, cy - 19, cx + 25, cy + 6], 3, fill=wt)
        c.polygon([(cx - 6, cy - 11), (cx - 6, cy - 1), (cx + 9, cy - 6)], fill=col)
        c.rrect([cx - 7, cy + 12, cx + 7, cy + 18], 2, fill=dk)
        c.rrect([cx - 17, cy + 18, cx + 17, cy + 23], 3, fill=dk)
    elif kind == "compass":
        c.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=wt, outline=col, width=6)
        c.polygon([(cx, cy - 19), (cx + 8, cy + 3), (cx, cy - 2)], fill=col)
        c.polygon([(cx, cy + 19), (cx - 8, cy - 3), (cx, cy + 2)], fill=dk)
        c.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=dk)
    elif kind == "agent":                  # robot head + gear
        c.rrect([cx - 24, cy - 20, cx + 24, cy + 18], 10, fill=col)
        c.line([(cx, cy - 20), (cx, cy - 31)], fill=dk, width=4)
        c.ellipse([cx - 5, cy - 36, cx + 5, cy - 26], fill=dk)
        c.ellipse([cx - 16, cy - 9, cx - 3, cy + 4], fill=wt)
        c.ellipse([cx + 3, cy - 9, cx + 16, cy + 4], fill=wt)
        c.ellipse([cx - 12, cy - 6, cx - 6, cy], fill=dk)
        c.ellipse([cx + 6, cy - 6, cx + 12, cy], fill=dk)
        c.rrect([cx - 10, cy + 9, cx + 10, cy + 13], 2, fill=wt)
        gx, gy = cx + 20, cy + 19          # little gear
        for a in range(8):
            ang = a * math.pi / 4
            c.line([(gx + math.cos(ang) * 5, gy + math.sin(ang) * 5),
                    (gx + math.cos(ang) * 10, gy + math.sin(ang) * 10)], fill=dk, width=3)
        c.ellipse([gx - 7, gy - 7, gx + 7, gy + 7], fill=dk)
        c.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=SAND)
    elif kind == "search":                 # magnifier
        c.ellipse([cx - 26, cy - 26, cx + 6, cy + 6], fill=wt, outline=col, width=7)
        c.line([(cx + 6, cy + 6), (cx + 22, cy + 22)], fill=col, width=9)
    elif kind == "telemetry":              # broadcast waves
        c.ellipse([cx - 4, cy + 12, cx + 4, cy + 20], fill=col)
        for i, r in enumerate((11, 20, 29)):
            c.arc([cx - r, cy - r + 14, cx + r, cy + r + 14], 210, 330,
                  fill=blend(col, wt, i * 0.16), width=5)
    elif kind == "ai":                     # spark / AI star
        c.polygon([(cx, cy - 28), (cx + 6, cy - 6), (cx + 28, cy),
                   (cx + 6, cy + 6), (cx, cy + 28), (cx - 6, cy + 6),
                   (cx - 28, cy), (cx - 6, cy - 6)], fill=col)
        c.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=wt)
        c.polygon([(cx + 20, cy - 22), (cx + 23, cy - 15), (cx + 30, cy - 12),
                   (cx + 23, cy - 9), (cx + 20, cy - 2), (cx + 17, cy - 9),
                   (cx + 10, cy - 12), (cx + 17, cy - 15)], fill=blend(col, wt, 0.15))
    elif kind == "shield":                 # shield + check (Policy Lifecycle)
        pts = [(cx, cy - 28), (cx + 24, cy - 18), (cx + 24, cy + 4),
               (cx, cy + 28), (cx - 24, cy + 4), (cx - 24, cy - 18)]
        c.polygon(pts, fill=col)
        c.line([(cx - 11, cy), (cx - 3, cy + 10)], fill=wt, width=6)
        c.line([(cx - 3, cy + 10), (cx + 13, cy - 10)], fill=wt, width=6)
    elif kind == "lock":                   # padlock (Security)
        c.arc([cx - 15, cy - 26, cx + 15, cy + 4], 180, 360, fill=dk, width=7)
        c.rrect([cx - 22, cy - 8, cx + 22, cy + 24], 7, fill=col)
        c.ellipse([cx - 6, cy + 2, cx + 6, cy + 14], fill=wt)
        c.polygon([(cx - 4, cy + 9), (cx + 4, cy + 9), (cx + 6, cy + 20),
                   (cx - 6, cy + 20)], fill=wt)
    elif kind == "puzzle":                 # puzzle piece
        c.rrect([cx - 22, cy - 18, cx + 22, cy + 22], 6, fill=col)
        c.ellipse([cx - 8, cy - 30, cx + 8, cy - 14], fill=col)
        c.ellipse([cx + 16, cy - 6, cx + 32, cy + 10], fill=SAND)
    elif kind == "integrations":           # plug + outlet
        c.rrect([cx - 28, cy - 13, cx - 6, cy + 13], 6, fill=col)
        c.rrect([cx - 6, cy - 8, cx + 2, cy - 3], 2, fill=col)
        c.rrect([cx - 6, cy + 3, cx + 2, cy + 8], 2, fill=col)
        c.rrect([cx + 6, cy - 13, cx + 28, cy + 13], 6, fill=dk)
        c.rrect([cx + 12, cy - 8, cx + 17, cy - 3], 1, fill=SAND)
        c.rrect([cx + 12, cy + 3, cx + 17, cy + 8], 1, fill=SAND)
    elif kind == "container":              # isometric container / cube
        c.polygon([(cx, cy - 26), (cx + 26, cy - 13), (cx, cy), (cx - 26, cy - 13)], fill=col)
        c.polygon([(cx - 26, cy - 13), (cx, cy), (cx, cy + 26), (cx - 26, cy + 13)], fill=dk)
        c.polygon([(cx + 26, cy - 13), (cx, cy), (cx, cy + 26), (cx + 26, cy + 13)],
                  fill=blend(col, wt, 0.16))
        for k in (-13, 0, 13):             # ridges on the right face
            c.line([(cx + 8, cy + 4 + k * 0.5), (cx + 22, cy - 3 + k * 0.5)],
                   fill=blend(col, dk, 0.4), width=2)
    elif kind == "play":                   # play in circle
        c.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=col)
        c.polygon([(cx - 8, cy - 13), (cx - 8, cy + 13), (cx + 15, cy)], fill=wt)
    elif kind == "wrench":
        c.line([(cx - 18, cy + 18), (cx + 10, cy - 10)], fill=col, width=11)
        c.ellipse([cx + 2, cy - 26, cx + 24, cy - 4], fill=col)     # top head
        c.ellipse([cx + 8, cy - 20, cx + 20, cy - 8], fill=SAND)
        c.polygon([(cx + 8, cy - 26), (cx + 20, cy - 20), (cx + 10, cy - 8)], fill=SAND)
        c.ellipse([cx - 24, cy + 4, cx - 4, cy + 24], fill=col)     # bottom head
        c.ellipse([cx - 19, cy + 9, cx - 9, cy + 19], fill=SAND)
    elif kind == "strategy":               # folded map + pin
        c.polygon([(cx - 26, cy - 18), (cx - 8, cy - 22), (cx + 8, cy - 18),
                   (cx + 26, cy - 22), (cx + 26, cy + 18), (cx + 8, cy + 22),
                   (cx - 8, cy + 18), (cx - 26, cy + 22)], fill=wt, outline=col, width=4)
        c.line([(cx - 8, cy - 22), (cx - 8, cy + 18)], fill=col, width=2)
        c.line([(cx + 8, cy - 18), (cx + 8, cy + 22)], fill=col, width=2)
        c.ellipse([cx + 2, cy - 12, cx + 22, cy + 8], fill=col)     # pin
        c.polygon([(cx + 5, cy + 3), (cx + 19, cy + 3), (cx + 12, cy + 18)], fill=col)
        c.ellipse([cx + 8, cy - 6, cx + 16, cy + 2], fill=wt)
    elif kind == "siren":                  # alert beacon
        c.rrect([cx - 20, cy + 14, cx + 20, cy + 22], 3, fill=dk)
        c.polygon([(cx - 17, cy + 14), (cx - 12, cy - 8), (cx + 12, cy - 8),
                   (cx + 17, cy + 14)], fill=col)
        c.ellipse([cx - 12, cy - 15, cx + 12, cy - 1], fill=col)
        c.ellipse([cx - 5, cy - 13, cx + 5, cy - 5], fill=blend(col, wt, 0.5))
        for dx, dy in ((-30, -12), (-24, -28), (0, -34), (24, -28), (30, -12)):
            c.line([(cx + dx * 0.62, cy - 10 + dy * 0.42),
                    (cx + dx, cy - 10 + dy)], fill=blend(col, wt, 0.1), width=4)


# ---------------------------------------------------------------- pieces ----
def palm(c, x, y):
    """Small palm tree; base of trunk at (x, y)."""
    for i in range(6):
        t = i / 5
        c.line([(x + t * 5, y - t * 20), (x + (t + 0.2) * 5, y - (t + 0.2) * 20)],
               fill=blend(TRUNK, (110, 78, 44), t), width=5 - int(t))
    tx, ty = x + 6, y - 23
    for fx, fy in [(-24, -4), (-15, -15), (0, -19), (15, -15), (24, -4), (10, 3), (-10, 3)]:
        c.polygon([(tx, ty), (tx + fx * 0.5, ty + fy * 0.7), (tx + fx, ty + fy)], fill=LEAF)
        c.line([(tx, ty), (tx + fx, ty + fy)], fill=LEAF_DK, width=2)
    c.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(120, 90, 55))


def grass_tuft(c, x, y):
    for dx in (-5, -1, 3):
        c.line([(x + dx, y), (x + dx * 1.4, y - 8)], fill=LEAF_DK, width=2)
        c.line([(x + dx, y), (x + dx * 0.8, y - 10)], fill=LEAF, width=2)


def blob(cx, cy, rx, ry, seed, n=48):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = (0.08 * math.sin(3 * a + seed) + 0.05 * math.sin(5 * a + seed * 1.7)
             + 0.03 * math.sin(8 * a + seed * 0.6))
        pts.append((cx + math.cos(a) * rx * (1 + k), cy + math.sin(a) * ry * (1 + k)))
    return pts


def island(c, cx, cy, kind, label, seed):
    """Small sand island beneath a large icon; cy is the ICON center."""
    scy = cy + 30                          # sand mound center
    rx, ry = 58, 23
    c.ellipse([cx - rx + 4, scy + ry - 6, cx + rx + 8, scy + ry + 12], fill=SAND_SH)
    c.arc([cx - rx - 10, scy - ry, cx + rx + 10, scy + ry + 14], 20, 160, fill=WAVE, width=2)
    c.polygon(blob(cx, scy + 3, rx, ry, seed), fill=SAND_EDGE)
    c.polygon(blob(cx, scy, rx - 6, ry - 5, seed), fill=SAND)
    c.polygon(blob(cx, scy - 4, rx - 20, ry - 11, seed + 1.3), fill=SAND_HI)
    grass_tuft(c, cx - 34, scy + 2)
    palm(c, cx + 30, scy + 1)
    icon(c, kind, cx, cy + 2)
    c.text((cx, scy + ry + 17), label, bold(15), LABEL)


def dotted_path(c, pts, color=BLUE, r=4.2, gap=15):
    for a, b in zip(pts, pts[1:]):
        (x0, y0), (x1, y1) = a, b
        dist = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(dist / gap))
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            c.ellipse([x - r, y - r, x + r, y + r], fill=color)


def start_marker(c, x, y):
    c.ellipse([x - 26, y + 14, x + 26, y + 34], fill=ROCK_DK)
    c.ellipse([x - 24, y + 10, x + 22, y + 28], fill=ROCK)
    c.rrect([x - 34, y - 18, x + 34, y + 10], 6, fill=GREEN, outline=GREEN_DK, width=2)
    c.text((x, y - 5), "START", bold(15), WHITE)
    c.ellipse([x + 16, y - 34, x + 34, y - 16], fill=GREEN, outline=GREEN_DK, width=2)
    c.polygon([(x + 20, y - 20), (x + 30, y - 20), (x + 25, y - 8)], fill=GREEN)
    c.ellipse([x + 22, y - 30, x + 28, y - 24], fill=WHITE)


def mastery_marker(c, x, y):
    c.ellipse([x - 30, y + 14, x + 30, y + 36], fill=ROCK_DK)
    c.ellipse([x - 27, y + 9, x + 26, y + 29], fill=ROCK)
    c.line([(x - 14, y + 18), (x - 14, y - 40)], fill=(70, 70, 76), width=5)
    fx, fy, cs = x - 14, y - 40, 8
    for r_ in range(4):
        for col_ in range(6):
            fill = NAVY if (r_ + col_) % 2 == 0 else WHITE
            c.polygon([(fx + col_ * cs, fy + r_ * cs), (fx + (col_ + 1) * cs, fy + r_ * cs),
                       (fx + (col_ + 1) * cs, fy + (r_ + 1) * cs),
                       (fx + col_ * cs, fy + (r_ + 1) * cs)], fill=fill)
    c.rrect([x - 6, y - 2, x + 66, y + 24], 6, fill=NAVY)
    c.text((x + 30, y + 11), "MASTERY", bold(13), WHITE)


def cisco_logo(c, x, y):
    heights = [16, 26, 16, 26, 16, 26, 16, 26, 16]
    for i, h in enumerate(heights):
        bx = x + i * 8
        c.rrect([bx, y - h / 2, bx + 3.4, y + h / 2], 1.7, fill=WHITE)
    c.text((x + 34, y + 24), "CISCO", bold(15), WHITE, anchor="mm")


# ---- islands in learning-path order: (icon, label) ----
ISLANDS = [
    ("overview",     "Overview Demo"),
    ("compass",      "Foundations"),
    ("agent",        "Agents"),
    ("search",       "Visibility"),
    ("telemetry",    "Connectors & Telemetry"),
    ("ai",           "AI-Assisted Policy"),
    ("shield",       "Policy Lifecycle"),
    ("lock",         "Security & Forensics"),
    ("puzzle",       "Use Cases"),
    ("integrations", "Integrations"),
    ("container",    "Containers & K8s"),
    ("play",         "Official Demos"),
    ("wrench",       "Day-2 Ops"),
    ("strategy",     "Strategy"),
    ("siren",        "Incident Response"),
]


def build(path):
    big = Image.new("RGB", (W * S, H * S), SKY_TOP)
    d = ImageDraw.Draw(big)
    for yy in range(H):
        d.line([(0, yy * S), (W * S, yy * S)], fill=blend(SKY_TOP, SKY_BOT, yy / H), width=S)
    c = Canvas(d)

    for i in range(26):
        wy = 150 + i * 26 + (i % 3) * 6
        wx = 40 + (i * 53) % (W - 220)
        c.arc([wx, wy, wx + 84, wy + 30], 200, 340, fill=WAVE, width=2)

    # 5 columns x 3 rows, serpentine
    col_x = [225, 430, 635, 840, 1045]
    row_y = [230, 450, 670]                # icon-center rows

    pos = {}
    for i in range(5):
        pos[i + 1] = (col_x[i], row_y[0])
    for i in range(5):
        pos[6 + i] = (col_x[4 - i], row_y[1])
    for i in range(5):
        pos[11 + i] = (col_x[i], row_y[2])

    start_xy = (95, row_y[0] + 30)
    mastery_xy = (1150, row_y[2] + 30)

    E = 66                                  # island half-width at sand level
    def er(n): x, y = pos[n]; return (x + E, y + 30)
    def el(n): x, y = pos[n]; return (x - E, y + 30)

    trail = [(start_xy[0] + 34, start_xy[1] - 4), el(1)]
    for n in range(1, 5):
        trail += [er(n), el(n + 1)]
    x5, y5 = pos[5]; x6, y6 = pos[6]
    trail += [(x5 + E, y5 + 30), (x5 + 150, y5 + 90), (x6 + E, y6 - 30), er(6)]
    for n in range(6, 10):
        trail += [el(n), er(n + 1)]
    x10, y10 = pos[10]; x11, y11 = pos[11]
    trail += [(x10 - E, y10 + 30), (x10 - 150, y10 + 90), (x11 - E, y11 - 30), el(11)]
    for n in range(11, 15):
        trail += [er(n), el(n + 1)]
    trail += [er(15), (mastery_xy[0] - 34, mastery_xy[1] - 4)]

    dotted_path(c, trail)

    start_marker(c, *start_xy)
    for i, (kind, label) in enumerate(ISLANDS, 1):
        x, y = pos[i]
        island(c, x, y, kind, label, seed=i * 1.37)
    mastery_marker(c, *mastery_xy)

    # header banner
    c.rrect([70, 22, 812, 100], 14, fill=NAVY, outline=CYAN, width=3)
    c.rrect([76, 90, 806, 97], 4, fill=CYAN)
    cisco_logo(c, 100, 52)
    c.line([(216, 34), (216, 88)], fill=blend(NAVY, WHITE, 0.35), width=2)
    c.text((236, 60), "The CSW Learning Journey", bold(34), WHITE, anchor="lm")
    c.text((441, 128), "Hop across the islands in order  \u00b7  or dive into any stop",
           font(15.5), NAVY_2, anchor="mm")

    big.resize((W, H), Image.LANCZOS).save(path)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.normpath(os.path.join(here, "..", "docs", "user-education",
                                         "csw-learning-journey.png"))
    p = build(dest)
    print(os.path.relpath(p), f"{os.path.getsize(p)/1024:.0f} KB")
