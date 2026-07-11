#!/usr/bin/env python3
"""Generate the CSW Learning Journey island map for the User Education README.

15 themed stops in learning-path order (Overview -> Incident Response), connected
by a dotted trail from START to MASTERY, laid out as an island-hopping map.

Design goals (v2 — "more attractive"):
  * richer sky->ocean gradient with soft clouds, water sparkles, and wave rings
  * real soft drop-shadows (Gaussian-blurred layers) under islands + header for depth
  * three colour-coded learning PHASES (Foundations / Operate & Integrate /
    Advanced & Day-2) applied to the icons, path segments, and numbered badges
  * numbered stop badges, a phase legend card, and a decorative compass rose
Rendered at 2x and downsampled (LANCZOS) for crisp, anti-aliased output.
All original artwork; no Cisco copyrighted assets.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- canvas (layout space; drawing is supersampled by S) ----
S = 2
W, H = 1280, 820

# ---- palette ----
SKY_TOP   = (240, 248, 254)
SKY_MID   = (214, 236, 248)
SKY_BOT   = (188, 223, 242)
WAVE      = (205, 230, 246)
WAVE_LT   = (226, 241, 251)
CLOUD     = (255, 255, 255)
SUN       = (255, 241, 199)
NAVY      = (16, 28, 67)
NAVY_2    = (28, 52, 120)         # header gradient end
NAVY_BDR  = (120, 170, 226)
WHITE     = (255, 255, 255)
CUT       = (250, 251, 253)
SAND_HI   = (253, 253, 249)
SAND_MID  = (243, 238, 221)
SAND_EDGE = (219, 210, 188)
SAND_SH   = (196, 214, 228)
BUSH      = (107, 151, 78)
BUSH_DK   = (80, 118, 58)
TRUNK     = (150, 110, 66)
GREEN     = (56, 168, 88)
GREEN_DK  = (38, 132, 66)
ROCK      = (128, 140, 150)
ROCK_DK   = (98, 110, 120)
LABEL     = (20, 26, 72)
SHADOW    = (24, 46, 86)          # base colour for soft shadows

# phase colours: (light, dark)  ->  Foundations / Operate & Integrate / Advanced
PHASES = [
    ((61, 110, 194), (36, 70, 150),  "Foundations"),          # blue
    ((22, 160, 150), (14, 116, 108), "Operate & Integrate"),  # teal
    ((116, 88, 204), (80, 58, 150),  "Advanced & Day-2"),     # indigo
]

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


def new_layer():
    """Transparent supersampled RGBA layer + its Canvas (for blurred shadows/glows)."""
    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    return img, Canvas(ImageDraw.Draw(img))


def blur_paste(base, layer, radius):
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius * S)))


# ------------------------------------------------------------- big icons ----
def icon(c, kind, cx, cy, col, dk):
    """Large (~60px), clean phase-coloured icon centered at (cx, cy)."""
    if kind == "overview":                 # monitor + play
        c.rrect([cx - 30, cy - 24, cx + 30, cy + 12], 6, fill=col)
        c.rrect([cx - 25, cy - 19, cx + 25, cy + 6], 3, fill=WHITE)
        c.polygon([(cx - 6, cy - 11), (cx - 6, cy - 1), (cx + 9, cy - 6)], fill=col)
        c.rrect([cx - 7, cy + 12, cx + 7, cy + 18], 2, fill=dk)
        c.rrect([cx - 17, cy + 18, cx + 17, cy + 23], 3, fill=dk)
    elif kind == "compass":
        c.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=WHITE, outline=col, width=6)
        c.polygon([(cx, cy - 19), (cx + 8, cy + 3), (cx, cy - 2)], fill=col)
        c.polygon([(cx, cy + 19), (cx - 8, cy - 3), (cx, cy + 2)], fill=dk)
        c.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=dk)
    elif kind == "agent":                  # robot head + gear
        c.rrect([cx - 24, cy - 20, cx + 24, cy + 18], 10, fill=col)
        c.line([(cx, cy - 20), (cx, cy - 31)], fill=dk, width=4)
        c.ellipse([cx - 5, cy - 36, cx + 5, cy - 26], fill=dk)
        c.ellipse([cx - 16, cy - 9, cx - 3, cy + 4], fill=WHITE)
        c.ellipse([cx + 3, cy - 9, cx + 16, cy + 4], fill=WHITE)
        c.ellipse([cx - 12, cy - 6, cx - 6, cy], fill=dk)
        c.ellipse([cx + 6, cy - 6, cx + 12, cy], fill=dk)
        c.rrect([cx - 10, cy + 9, cx + 10, cy + 13], 2, fill=WHITE)
        gx, gy = cx + 20, cy + 19
        for a in range(8):
            ang = a * math.pi / 4
            c.line([(gx + math.cos(ang) * 5, gy + math.sin(ang) * 5),
                    (gx + math.cos(ang) * 10, gy + math.sin(ang) * 10)], fill=dk, width=3)
        c.ellipse([gx - 7, gy - 7, gx + 7, gy + 7], fill=dk)
        c.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=CUT)
    elif kind == "search":                 # magnifier
        c.ellipse([cx - 26, cy - 26, cx + 6, cy + 6], fill=WHITE, outline=col, width=7)
        c.line([(cx + 6, cy + 6), (cx + 22, cy + 22)], fill=col, width=9)
    elif kind == "telemetry":              # broadcast waves
        c.ellipse([cx - 4, cy + 12, cx + 4, cy + 20], fill=col)
        for i, r in enumerate((11, 20, 29)):
            c.arc([cx - r, cy - r + 14, cx + r, cy + r + 14], 210, 330,
                  fill=blend(col, WHITE, i * 0.16), width=5)
    elif kind == "ai":                     # spark / AI star
        c.polygon([(cx, cy - 28), (cx + 6, cy - 6), (cx + 28, cy),
                   (cx + 6, cy + 6), (cx, cy + 28), (cx - 6, cy + 6),
                   (cx - 28, cy), (cx - 6, cy - 6)], fill=col)
        c.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)
        c.polygon([(cx + 20, cy - 22), (cx + 23, cy - 15), (cx + 30, cy - 12),
                   (cx + 23, cy - 9), (cx + 20, cy - 2), (cx + 17, cy - 9),
                   (cx + 10, cy - 12), (cx + 17, cy - 15)], fill=blend(col, WHITE, 0.15))
    elif kind == "shield":                 # shield + check (Policy Lifecycle)
        pts = [(cx, cy - 28), (cx + 24, cy - 18), (cx + 24, cy + 4),
               (cx, cy + 28), (cx - 24, cy + 4), (cx - 24, cy - 18)]
        c.polygon(pts, fill=col)
        c.line([(cx - 11, cy), (cx - 3, cy + 10)], fill=WHITE, width=6)
        c.line([(cx - 3, cy + 10), (cx + 13, cy - 10)], fill=WHITE, width=6)
    elif kind == "lock":                   # padlock (Security)
        c.arc([cx - 15, cy - 26, cx + 15, cy + 4], 180, 360, fill=dk, width=7)
        c.rrect([cx - 22, cy - 8, cx + 22, cy + 24], 7, fill=col)
        c.ellipse([cx - 6, cy + 2, cx + 6, cy + 14], fill=WHITE)
        c.polygon([(cx - 4, cy + 9), (cx + 4, cy + 9), (cx + 6, cy + 20),
                   (cx - 6, cy + 20)], fill=WHITE)
    elif kind == "puzzle":                 # puzzle piece
        c.rrect([cx - 22, cy - 18, cx + 22, cy + 22], 6, fill=col)
        c.ellipse([cx - 8, cy - 30, cx + 8, cy - 14], fill=col)
        c.ellipse([cx + 16, cy - 6, cx + 32, cy + 10], fill=CUT)
    elif kind == "integrations":           # plug + outlet
        c.rrect([cx - 28, cy - 13, cx - 6, cy + 13], 6, fill=col)
        c.rrect([cx - 6, cy - 8, cx + 2, cy - 3], 2, fill=col)
        c.rrect([cx - 6, cy + 3, cx + 2, cy + 8], 2, fill=col)
        c.rrect([cx + 6, cy - 13, cx + 28, cy + 13], 6, fill=dk)
        c.rrect([cx + 12, cy - 8, cx + 17, cy - 3], 1, fill=CUT)
        c.rrect([cx + 12, cy + 3, cx + 17, cy + 8], 1, fill=CUT)
    elif kind == "container":              # isometric container / cube
        c.polygon([(cx, cy - 26), (cx + 26, cy - 13), (cx, cy), (cx - 26, cy - 13)], fill=col)
        c.polygon([(cx - 26, cy - 13), (cx, cy), (cx, cy + 26), (cx - 26, cy + 13)], fill=dk)
        c.polygon([(cx + 26, cy - 13), (cx, cy), (cx, cy + 26), (cx + 26, cy + 13)],
                  fill=blend(col, WHITE, 0.16))
        for k in (-13, 0, 13):
            c.line([(cx + 8, cy + 4 + k * 0.5), (cx + 22, cy - 3 + k * 0.5)],
                   fill=blend(col, dk, 0.4), width=2)
    elif kind == "play":                   # play in circle
        c.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=col)
        c.polygon([(cx - 8, cy - 13), (cx - 8, cy + 13), (cx + 15, cy)], fill=WHITE)
    elif kind == "wrench":
        c.line([(cx - 18, cy + 18), (cx + 10, cy - 10)], fill=col, width=11)
        c.ellipse([cx + 2, cy - 26, cx + 24, cy - 4], fill=col)
        c.ellipse([cx + 8, cy - 20, cx + 20, cy - 8], fill=CUT)
        c.polygon([(cx + 8, cy - 26), (cx + 20, cy - 20), (cx + 10, cy - 8)], fill=CUT)
        c.ellipse([cx - 24, cy + 4, cx - 4, cy + 24], fill=col)
        c.ellipse([cx - 19, cy + 9, cx - 9, cy + 19], fill=CUT)
    elif kind == "strategy":               # folded map + pin
        c.polygon([(cx - 26, cy - 18), (cx - 8, cy - 22), (cx + 8, cy - 18),
                   (cx + 26, cy - 22), (cx + 26, cy + 18), (cx + 8, cy + 22),
                   (cx - 8, cy + 18), (cx - 26, cy + 22)], fill=WHITE, outline=col, width=4)
        c.line([(cx - 8, cy - 22), (cx - 8, cy + 18)], fill=col, width=2)
        c.line([(cx + 8, cy - 18), (cx + 8, cy + 22)], fill=col, width=2)
        c.ellipse([cx + 2, cy - 12, cx + 22, cy + 8], fill=col)
        c.polygon([(cx + 5, cy + 3), (cx + 19, cy + 3), (cx + 12, cy + 18)], fill=col)
        c.ellipse([cx + 8, cy - 6, cx + 16, cy + 2], fill=WHITE)
    elif kind == "siren":                  # alert beacon
        c.rrect([cx - 20, cy + 14, cx + 20, cy + 22], 3, fill=dk)
        c.polygon([(cx - 17, cy + 14), (cx - 12, cy - 8), (cx + 12, cy - 8),
                   (cx + 17, cy + 14)], fill=col)
        c.ellipse([cx - 12, cy - 15, cx + 12, cy - 1], fill=col)
        c.ellipse([cx - 5, cy - 13, cx + 5, cy - 5], fill=blend(col, WHITE, 0.5))
        for dx, dy in ((-30, -12), (-24, -28), (0, -34), (24, -28), (30, -12)):
            c.line([(cx + dx * 0.62, cy - 10 + dy * 0.42),
                    (cx + dx, cy - 10 + dy)], fill=blend(col, WHITE, 0.1), width=4)


# ---------------------------------------------------------------- pieces ----
def palm(c, x, y):
    for i in range(6):
        t = i / 5
        c.line([(x + t * 6, y - t * 26), (x + (t + 0.2) * 6, y - (t + 0.2) * 26)],
               fill=blend(TRUNK, (110, 78, 44), t), width=6 - int(t * 2))
    tx, ty = x + 8, y - 30
    for fx, fy in [(-30, -5), (-19, -19), (0, -24), (19, -19), (30, -5), (13, 4), (-13, 4)]:
        c.polygon([(tx, ty), (tx + fx * 0.5, ty + fy * 0.7), (tx + fx, ty + fy)], fill=BUSH)
        c.line([(tx, ty), (tx + fx, ty + fy)], fill=BUSH_DK, width=2)
    c.ellipse([tx - 3, ty - 3, tx + 3, ty + 3], fill=(120, 90, 55))


def bush(c, x, y, s=1.0):
    for dx, dy, r in [(-6, 1, 7), (1, -3, 8), (8, 1, 6)]:
        c.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s],
                  fill=BUSH_DK)
    for dx, dy, r in [(-5, -1, 6), (1, -4, 7), (7, 0, 5)]:
        c.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s],
                  fill=BUSH)


def island(c, cx, cy, kind, label, num, col, dk):
    """Cream-sand dome island beneath a large icon, with a numbered phase badge."""
    scy = cy + 26
    rx, ry = 52, 18
    c.ellipse([cx - rx, scy - ry, cx + rx, scy + ry], fill=SAND_EDGE)             # tan rim
    c.ellipse([cx - rx + 2, scy - ry, cx + rx - 2, scy + ry - 5], fill=SAND_MID)  # sand body
    c.ellipse([cx - rx + 4, scy - ry, cx + rx - 4, scy + ry - 9], fill=SAND_HI)   # cream top
    bush(c, cx - 30, scy + 3)
    bush(c, cx - 13, scy + 6, s=0.8)
    palm(c, cx + 26, scy - 1)
    icon(c, kind, cx, cy, col, dk)
    # numbered phase badge (pin) top-left of the icon
    bx, by = cx - 40, cy - 22
    c.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=dk, outline=WHITE, width=3)
    c.text((bx, by - 0.5), str(num), bold(13), WHITE)
    c.text((cx, scy + ry + 16), label, bold(15), LABEL)


def dotted_path(c, pts, color, r=4.2, gap=15):
    for a, b in zip(pts, pts[1:]):
        (x0, y0), (x1, y1) = a, b
        dist = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(dist / gap))
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            c.ellipse([x - r, y - r, x + r, y + r], fill=color)


def chevron(c, p0, p1, color, at=0.5, size=6.5):
    """Small direction arrowhead placed at fraction `at` along segment p0->p1."""
    (x0, y0), (x1, y1) = p0, p1
    ang = math.atan2(y1 - y0, x1 - x0)
    cx = x0 + (x1 - x0) * at
    cy = y0 + (y1 - y0) * at
    tip = (cx + math.cos(ang) * size, cy + math.sin(ang) * size)
    l = (cx + math.cos(ang + 2.5) * size, cy + math.sin(ang + 2.5) * size)
    r = (cx + math.cos(ang - 2.5) * size, cy + math.sin(ang - 2.5) * size)
    c.polygon([tip, l, r], fill=color)


def start_marker(c, x, y):
    c.ellipse([x - 24, y + 10, x + 22, y + 28], fill=ROCK)
    c.rrect([x - 34, y - 18, x + 34, y + 10], 6, fill=GREEN, outline=GREEN_DK, width=2)
    c.text((x, y - 5), "START", bold(15), WHITE)
    c.ellipse([x + 16, y - 34, x + 34, y - 16], fill=GREEN, outline=GREEN_DK, width=2)
    c.polygon([(x + 20, y - 20), (x + 30, y - 20), (x + 25, y - 8)], fill=GREEN)
    c.ellipse([x + 22, y - 30, x + 28, y - 24], fill=WHITE)


def mastery_marker(c, x, y):
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


def cloud(c, x, y, s):
    for dx, dy, r in [(-26, 4, 18), (-6, -6, 24), (18, 2, 20), (0, 8, 26), (34, 8, 15)]:
        c.ellipse([x + (dx - r) * s, y + (dy - r) * s,
                   x + (dx + r) * s, y + (dy + r) * s], fill=CLOUD)


def sparkle(c, x, y, s, color=WHITE):
    c.polygon([(x, y - 6 * s), (x + 1.4 * s, y - 1.4 * s), (x + 6 * s, y),
               (x + 1.4 * s, y + 1.4 * s), (x, y + 6 * s), (x - 1.4 * s, y + 1.4 * s),
               (x - 6 * s, y), (x - 1.4 * s, y - 1.4 * s)], fill=color)


def compass_rose(c, x, y, R=30):
    c.ellipse([x - R, y - R, x + R, y + R], fill=(255, 255, 255), outline=NAVY_BDR, width=2)
    c.ellipse([x - R + 6, y - R + 6, x + R - 6, y + R - 6], outline=blend(NAVY_BDR, WHITE, 0.4), width=1)
    # 4-point star
    c.polygon([(x, y - R + 4), (x + 5, y - 5), (x, y), (x - 5, y - 5)], fill=(214, 78, 74))     # N red
    c.polygon([(x, y + R - 4), (x + 5, y + 5), (x, y), (x - 5, y + 5)], fill=NAVY)              # S
    c.polygon([(x + R - 4, y), (x + 5, y - 5), (x, y), (x + 5, y + 5)], fill=blend(NAVY, WHITE, 0.35))
    c.polygon([(x - R + 4, y), (x - 5, y - 5), (x, y), (x - 5, y + 5)], fill=blend(NAVY, WHITE, 0.35))
    c.text((x, y - R - 8), "N", bold(11), NAVY)


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


def phase_of(n):
    """1-based stop number -> phase index 0/1/2."""
    return min(2, (n - 1) // 5)


def legend_card(base):
    """Translucent phase legend, composited top-right."""
    lay, c = new_layer()
    x0, y0, x1, y1 = 986, 26, 1258, 150
    c.rrect([x0, y0, x1, y1], 12, fill=(255, 255, 255, 232), outline=(*NAVY_BDR, 255), width=2)
    c.text((x0 + 18, y0 + 20), "LEARNING PHASES", bold(13), (*NAVY, 255), anchor="lm")
    for i, (col, dk, name) in enumerate(PHASES):
        yy = y0 + 46 + i * 26
        c.ellipse([x0 + 16, yy - 7, x0 + 30, yy + 7], fill=(*col, 255))
        rng = ["1\u20135", "6\u201310", "11\u201315"][i]
        c.text((x0 + 40, yy), f"{rng}   {name}", font(13.5), (*LABEL, 255), anchor="lm")
    base.alpha_composite(lay)


def build(path):
    # ---- ocean gradient base (RGBA) ----
    big = Image.new("RGBA", (W * S, H * S), (*SKY_TOP, 255))
    d = ImageDraw.Draw(big)
    for yy in range(H):
        t = yy / H
        col = blend(SKY_TOP, SKY_MID, t * 2) if t < 0.5 else blend(SKY_MID, SKY_BOT, (t - 0.5) * 2)
        d.line([(0, yy * S), (W * S, yy * S)], fill=(*col, 255), width=S)
    c = Canvas(d)

    # ---- soft sun glow (top-right, behind legend) ----
    sun, sc = new_layer()
    sc.ellipse([1120, -70, 1300, 90], fill=(*SUN, 150))
    blur_paste(big, sun, 34)

    # ---- soft clouds ----
    clouds, cc = new_layer()
    for cx_, cy_, s_ in [(250, 150, 1.0), (620, 110, 0.75), (900, 175, 0.9), (720, 470, 0.7)]:
        cloud(cc, cx_, cy_, s_)
    blur_paste(big, clouds, 6)

    # ---- wave rings + sparkles on the water ----
    for i in range(30):
        wy = 150 + i * 22 + (i % 3) * 7
        wx = 40 + (i * 71) % (W - 200)
        c.arc([wx, wy, wx + 74, wy + 26], 200, 340, fill=WAVE, width=2)
        c.arc([wx + 8, wy + 5, wx + 60, wy + 24], 205, 335, fill=WAVE_LT, width=1)
    for sx, sy, ss in [(160, 320, 1.0), (560, 300, 0.7), (980, 470, 0.9), (330, 560, 0.8),
                       (860, 610, 0.7), (1170, 250, 0.8), (470, 165, 0.6)]:
        sparkle(c, sx, sy, ss, blend(WAVE_LT, WHITE, 0.6))

    # ---- layout (serpentine) ----
    col_x = [225, 430, 635, 840, 1045]
    row_y = [230, 450, 670]
    pos = {}
    for i in range(5):
        pos[i + 1] = (col_x[i], row_y[0])
    for i in range(5):
        pos[6 + i] = (col_x[4 - i], row_y[1])
    for i in range(5):
        pos[11 + i] = (col_x[i], row_y[2])

    start_xy = (95, row_y[0] + 26)
    mastery_xy = (1150, row_y[2] + 26)

    E = 56
    def er(n): x, y = pos[n]; return (x + E, y + 26)
    def el(n): x, y = pos[n]; return (x - E, y + 26)

    # build trail as list of (segment, phase) for colour-coded dots + chevrons
    seg = []  # (p0, p1, phase)
    seg.append(((start_xy[0] + 34, start_xy[1] - 4), el(1), 0))
    for n in range(1, 5):
        seg.append((er(n), el(n + 1), phase_of(n)))
    x5, y5 = pos[5]; x6, y6 = pos[6]
    seg.append(((x5 + E, y5 + 26), (x5 + 150, y5 + 90), 0))
    seg.append(((x5 + 150, y5 + 90), (x6 + E, y6 - 30), 1))
    seg.append(((x6 + E, y6 - 30), er(6), 1))
    for n in range(6, 10):
        seg.append((el(n), er(n + 1), phase_of(n)))
    x10, y10 = pos[10]; x11, y11 = pos[11]
    seg.append(((x10 - E, y10 + 26), (x10 - 150, y10 + 90), 1))
    seg.append(((x10 - 150, y10 + 90), (x11 - E, y11 - 30), 2))
    seg.append(((x11 - E, y11 - 30), el(11), 2))
    for n in range(11, 15):
        seg.append((er(n), el(n + 1), phase_of(n)))
    seg.append((er(15), (mastery_xy[0] - 34, mastery_xy[1] - 4), 2))

    # ---- soft shadows under islands + markers (blurred layer) ----
    sh, shc = new_layer()
    for n in range(1, 16):
        x, y = pos[n]
        shc.ellipse([x - 52, y + 40, x + 56, y + 66], fill=(*SHADOW, 90))
    shc.ellipse([start_xy[0] - 26, start_xy[1] + 30, start_xy[0] + 28, start_xy[1] + 50], fill=(*SHADOW, 80))
    shc.ellipse([mastery_xy[0] - 30, mastery_xy[1] + 26, mastery_xy[0] + 32, mastery_xy[1] + 48], fill=(*SHADOW, 80))
    blur_paste(big, sh, 5)

    # ---- path glow (blurred, phase-coloured) ----
    glow, gc = new_layer()
    for p0, p1, ph in seg:
        gc.line([p0, p1], fill=(*PHASES[ph][0], 70), width=9)
    blur_paste(big, glow, 4)

    # ---- crisp dotted path + chevrons ----
    for p0, p1, ph in seg:
        dotted_path(c, [p0, p1], PHASES[ph][0])
    # chevrons only on the straight inter-island segments (skip the vertical curves)
    straight = [s for s in seg if abs(s[0][1] - s[1][1]) < 20]
    for p0, p1, ph in straight:
        chevron(c, p0, p1, PHASES[ph][1], at=0.5)

    # ---- islands + markers ----
    start_marker(c, *start_xy)
    for i, (kind, label) in enumerate(ISLANDS, 1):
        x, y = pos[i]
        ph = phase_of(i)
        col, dk, _ = PHASES[ph]
        island(c, x, y, kind, label, i, col, dk)
    mastery_marker(c, *mastery_xy)

    # ---- compass rose (right-middle empty water) ----
    compass_rose(c, 1185, 505, R=30)

    # ---- header drop shadow + banner ----
    hsh, hc = new_layer()
    hc.rrect([74, 28, 816, 106], 14, fill=(*SHADOW, 120))
    blur_paste(big, hsh, 5)

    # header banner with horizontal navy gradient
    hd = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    hdd = ImageDraw.Draw(hd)
    for xx in range(70, 812):
        col = blend(NAVY, NAVY_2, (xx - 70) / 742)
        hdd.line([(xx * S, 22 * S), (xx * S, 100 * S)], fill=(*col, 255), width=S)
    mask = Image.new("L", (W * S, H * S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([70 * S, 22 * S, 812 * S, 100 * S], radius=14 * S, fill=255)
    big.paste(hd, (0, 0), mask)
    c.rrect([70, 22, 812, 100], 14, outline=NAVY_BDR, width=3)
    cisco_logo(c, 100, 52)
    c.line([(216, 34), (216, 88)], fill=blend(NAVY, WHITE, 0.35), width=2)
    c.text((236, 60), "The CSW Learning Journey", bold(34), WHITE, anchor="lm")

    # tagline pill
    c.rrect([300, 116, 700, 142], 13, fill=(*blend(WHITE, SKY_MID, 0.3), 255), outline=NAVY_BDR, width=1)
    c.text((500, 129), "Hop across the islands in order  \u00b7  or dive into any stop",
           font(14.5), NAVY, anchor="mm")

    # ---- phase legend ----
    legend_card(big)

    big.convert("RGB").resize((W, H), Image.LANCZOS).save(path)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.normpath(os.path.join(here, "..", "docs", "user-education",
                                         "csw-learning-journey.png"))
    p = build(dest)
    print(os.path.relpath(p), f"{os.path.getsize(p)/1024:.0f} KB")
