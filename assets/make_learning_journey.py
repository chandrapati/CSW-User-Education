#!/usr/bin/env python3
"""Generate the CSW Learning Journey island map for the User Education README.

15 themed islands laid out in learning-path order (Overview -> Incident Response),
connected by a dotted "hop across the islands" trail from START to MASTERY.
Rendered at 2x and downsampled for crisp, anti-aliased output.
All original artwork; no Cisco copyrighted assets.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- canvas (layout space; drawing is supersampled by S) ----
S = 2
W, H = 1280, 860

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
INK       = (18, 38, 70)
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
    """Thin wrapper that scales all coordinates/sizes by S so layout math
    can be written in the readable 1280x860 space."""

    def __init__(self, draw):
        self.d = draw

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def line(self, pts, fill, width=1):
        self.d.line(self._p(pts), fill=fill, width=max(1, int(width * S)),
                    joint="curve")

    def ellipse(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = box
        self.d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill,
                       outline=outline, width=max(1, int(width * S)))

    def polygon(self, pts, fill=None, outline=None, width=1):
        self.d.polygon(self._p(pts), fill=fill, outline=outline,
                       width=max(1, int(width * S)))

    def rrect(self, box, radius, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = box
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S],
                                 radius=radius * S, fill=fill, outline=outline,
                                 width=max(1, int(width * S)))

    def arc(self, box, start, end, fill, width=1):
        x0, y0, x1, y1 = box
        self.d.arc([x0 * S, y0 * S, x1 * S, y1 * S], start, end, fill=fill,
                   width=max(1, int(width * S)))

    def text(self, xy, s, f, fill, anchor="mm"):
        self.d.text((xy[0] * S, xy[1] * S), s, font=f, fill=fill, anchor=anchor)


def blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


# ---------------------------------------------------------------- icons ----
def icon(c, kind, cx, cy):
    """Draw a ~44px-wide icon centered at (cx, cy) in Cisco blue."""
    col, dk = BLUE, BLUE_DK

    if kind == "overview":            # monitor + play
        c.rrect([cx - 17, cy - 15, cx + 17, cy + 8], 3, fill=col)
        c.rrect([cx - 13, cy - 11, cx + 13, cy + 4], 2, fill=WHITE)
        c.polygon([(cx - 4, cy - 7), (cx - 4, cy), (cx + 6, cy - 3.5)], fill=col)
        c.rrect([cx - 9, cy + 8, cx + 9, cy + 12], 2, fill=dk)
    elif kind == "compass":
        c.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=WHITE, outline=col, width=3)
        c.polygon([(cx, cy - 11), (cx + 5, cy + 2), (cx, cy - 1)], fill=col)
        c.polygon([(cx, cy + 11), (cx - 5, cy - 2), (cx, cy + 1)], fill=dk)
        c.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=dk)
    elif kind == "agent":             # robot head
        c.rrect([cx - 15, cy - 12, cx + 15, cy + 13], 6, fill=col)
        c.line([(cx, cy - 12), (cx, cy - 19)], fill=dk, width=3)
        c.ellipse([cx - 3, cy - 22, cx + 3, cy - 16], fill=dk)
        c.ellipse([cx - 10, cy - 5, cx - 3, cy + 2], fill=WHITE)
        c.ellipse([cx + 3, cy - 5, cx + 10, cy + 2], fill=WHITE)
        c.line([(cx - 8, cy + 8), (cx + 8, cy + 8)], fill=WHITE, width=3)
    elif kind == "search":            # magnifier
        c.ellipse([cx - 17, cy - 17, cx + 5, cy + 5], fill=WHITE, outline=col, width=4)
        c.line([(cx + 4, cy + 4), (cx + 15, cy + 15)], fill=col, width=6)
    elif kind == "telemetry":         # broadcast / signal
        c.ellipse([cx - 3, cy + 6, cx + 3, cy + 12], fill=col)
        for i, r in enumerate((9, 16, 23)):
            c.arc([cx - r, cy - r + 9, cx + r, cy + r + 9], 210, 330,
                  fill=blend(col, WHITE, i * 0.18), width=3)
    elif kind == "ai":                # spark / AI star
        c.polygon([(cx, cy - 18), (cx + 4, cy - 4), (cx + 18, cy),
                   (cx + 4, cy + 4), (cx, cy + 18), (cx - 4, cy + 4),
                   (cx - 18, cy), (cx - 4, cy - 4)], fill=col)
        c.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)
    elif kind == "lifecycle":         # circular arrows
        c.arc([cx - 15, cy - 15, cx + 15, cy + 15], 300, 210, fill=col, width=4)
        c.polygon([(cx + 6, cy - 15), (cx + 17, cy - 13), (cx + 11, cy - 4)], fill=col)
        c.arc([cx - 15, cy - 15, cx + 15, cy + 15], 120, 30, fill=col, width=4)
        c.polygon([(cx - 6, cy + 15), (cx - 17, cy + 13), (cx - 11, cy + 4)], fill=col)
    elif kind == "shield":            # shield + check
        pts = [(cx, cy - 17), (cx + 15, cy - 11), (cx + 15, cy + 2),
               (cx, cy + 17), (cx - 15, cy + 2), (cx - 15, cy - 11)]
        c.polygon(pts, fill=col)
        c.line([(cx - 7, cy), (cx - 2, cy + 6)], fill=WHITE, width=4)
        c.line([(cx - 2, cy + 6), (cx + 8, cy - 6)], fill=WHITE, width=4)
    elif kind == "puzzle":            # puzzle piece
        c.rrect([cx - 14, cy - 12, cx + 14, cy + 14], 4, fill=col)
        c.ellipse([cx - 5, cy - 20, cx + 5, cy - 10], fill=col)
        c.ellipse([cx + 10, cy - 4, cx + 20, cy + 6], fill=SAND)
    elif kind == "integrations":      # linked chain
        c.rrect([cx - 18, cy - 7, cx - 1, cy + 7], 7, outline=col, width=4)
        c.rrect([cx + 1, cy - 7, cx + 18, cy + 7], 7, outline=col, width=4)
        c.line([(cx - 5, cy), (cx + 5, cy)], fill=col, width=4)
    elif kind == "container":         # stacked container / cube
        c.polygon([(cx, cy - 16), (cx + 16, cy - 8), (cx, cy), (cx - 16, cy - 8)], fill=col)
        c.polygon([(cx - 16, cy - 8), (cx, cy), (cx, cy + 16), (cx - 16, cy + 8)], fill=dk)
        c.polygon([(cx + 16, cy - 8), (cx, cy), (cx, cy + 16), (cx + 16, cy + 8)],
                  fill=blend(col, WHITE, 0.15))
    elif kind == "play":              # play in circle
        c.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=col)
        c.polygon([(cx - 5, cy - 8), (cx - 5, cy + 8), (cx + 9, cy)], fill=WHITE)
    elif kind == "wrench":
        c.line([(cx - 10, cy + 10), (cx + 6, cy - 6)], fill=col, width=7)
        c.ellipse([cx + 2, cy - 16, cx + 16, cy - 2], fill=col)
        c.ellipse([cx + 6, cy - 12, cx + 13, cy - 5], fill=SAND)
        c.ellipse([cx - 15, cy + 6, cx - 5, cy + 16], fill=col)
    elif kind == "strategy":          # map + pin
        c.polygon([(cx - 16, cy - 12), (cx - 5, cy - 15), (cx + 5, cy - 12),
                   (cx + 16, cy - 15), (cx + 16, cy + 12), (cx + 5, cy + 15),
                   (cx - 5, cy + 12), (cx - 16, cy + 15)], fill=WHITE, outline=col, width=3)
        c.line([(cx - 5, cy - 15), (cx - 5, cy + 12)], fill=col, width=2)
        c.line([(cx + 5, cy - 12), (cx + 5, cy + 15)], fill=col, width=2)
        c.ellipse([cx + 3, cy - 8, cx + 15, cy + 4], fill=col)
        c.polygon([(cx + 5, cy + 2), (cx + 13, cy + 2), (cx + 9, cy + 11)], fill=col)
        c.ellipse([cx + 7, cy - 4, cx + 11, cy], fill=WHITE)
    elif kind == "siren":             # alert beacon
        c.rrect([cx - 13, cy + 8, cx + 13, cy + 14], 2, fill=dk)
        c.polygon([(cx - 11, cy + 8), (cx - 8, cy - 6), (cx + 8, cy - 6),
                   (cx + 11, cy + 8)], fill=col)
        c.ellipse([cx - 8, cy - 11, cx + 8, cy - 1], fill=col)
        for ang, dx, dy in ((0, -19, -8), (1, -16, -18), (2, 0, -22),
                            (3, 16, -18), (4, 19, -8)):
            c.line([(cx + dx * 0.7, cy - 8 + dy * 0.4),
                    (cx + dx, cy - 8 + dy)], fill=blend(col, WHITE, 0.1), width=3)


# ---------------------------------------------------------------- pieces ----
def palm(c, x, y, flip=False):
    """Small palm tree; base of trunk at (x, y)."""
    s = -1 if flip else 1
    # trunk (slightly curved)
    for i in range(6):
        t = i / 5
        c.line([(x + s * t * 6, y - t * 26), (x + s * (t + 0.2) * 6, y - (t + 0.2) * 26)],
               fill=blend(TRUNK, (110, 78, 44), t), width=6 - int(t * 2))
    tx, ty = x + s * 7, y - 30
    fronds = [(-34, -6), (-22, -20), (0, -26), (22, -20), (34, -6), (14, 4), (-14, 4)]
    for fx, fy in fronds:
        c.polygon([(tx, ty), (tx + s * fx * 0.5, ty + fy * 0.7),
                   (tx + s * fx, ty + fy)], fill=LEAF)
        c.line([(tx, ty), (tx + s * fx, ty + fy)], fill=LEAF_DK, width=2)
    c.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=(120, 90, 55))


def blob(cx, cy, rx, ry, seed, n=54):
    """Organic island outline: an ellipse with gentle multi-harmonic wobble."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = (0.085 * math.sin(3 * a + seed)
             + 0.05 * math.sin(5 * a + seed * 1.7)
             + 0.03 * math.sin(8 * a + seed * 0.6))
        pts.append((cx + math.cos(a) * rx * (1 + k),
                    cy + math.sin(a) * ry * (1 + k)))
    return pts


def grass_tuft(c, x, y):
    for dx in (-6, -2, 2, 6):
        c.line([(x + dx, y), (x + dx * 1.4, y - 9)], fill=LEAF_DK, width=2)
        c.line([(x + dx, y), (x + dx * 0.8, y - 11)], fill=LEAF, width=2)


def island(c, cx, cy, kind, label, seed, has_palm=True):
    rx, ry = 88, 47
    # soft water shadow beneath the island
    c.ellipse([cx - rx + 6, cy + ry - 6, cx + rx + 10, cy + ry + 20], fill=SAND_SH)
    # surrounding water ripples
    c.arc([cx - rx - 14, cy - ry, cx + rx + 14, cy + ry + 22], 20, 160, fill=WAVE, width=2)
    c.arc([cx - rx - 24, cy - ry - 4, cx + rx + 24, cy + ry + 30], 25, 155, fill=blend(WAVE, SKY_BOT, 0.4), width=2)
    # wet-sand shoreline (darker, full size)
    c.polygon(blob(cx, cy + 4, rx, ry, seed), fill=SAND_EDGE)
    # dry sand body
    c.polygon(blob(cx, cy, rx - 7, ry - 6, seed), fill=SAND)
    # sunlit sand highlight (upper portion)
    c.polygon(blob(cx, cy - 9, rx - 26, ry - 16, seed + 1.3), fill=SAND_HI)
    if has_palm:
        grass_tuft(c, cx + 60, cy + 4)
        palm(c, cx + 44, cy + 4, flip=False)
    grass_tuft(c, cx - 52, cy + 8)
    icon(c, kind, cx - 8, cy - 4)
    # label
    c.text((cx, cy + ry + 26), label, bold(15.5), LABEL)


def dotted_path(c, pts, color=BLUE, r=4.2, gap=15):
    """Dotted trail through a list of waypoints (straight segments)."""
    for a, b in zip(pts, pts[1:]):
        (x0, y0), (x1, y1) = a, b
        dist = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(dist / gap))
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            c.ellipse([x - r, y - r, x + r, y + r], fill=color)


def start_marker(c, x, y):
    # rock base
    c.ellipse([x - 26, y + 14, x + 26, y + 34], fill=ROCK_DK)
    c.ellipse([x - 24, y + 10, x + 22, y + 28], fill=ROCK)
    # green road sign
    c.rrect([x - 34, y - 18, x + 34, y + 10], 6, fill=GREEN, outline=GREEN_DK, width=2)
    c.text((x, y - 5), "START", bold(15), WHITE)
    # location pin
    c.ellipse([x + 16, y - 34, x + 34, y - 16], fill=GREEN, outline=GREEN_DK, width=2)
    c.polygon([(x + 20, y - 20), (x + 30, y - 20), (x + 25, y - 8)], fill=GREEN)
    c.ellipse([x + 22, y - 30, x + 28, y - 24], fill=WHITE)


def mastery_marker(c, x, y):
    # rock base
    c.ellipse([x - 30, y + 14, x + 30, y + 36], fill=ROCK_DK)
    c.ellipse([x - 27, y + 9, x + 26, y + 29], fill=ROCK)
    # pole
    c.line([(x - 14, y + 18), (x - 14, y - 40)], fill=(70, 70, 76), width=5)
    # checkered flag
    fx, fy, cols, rows, cs = x - 14, y - 40, 6, 4, 8
    for r_ in range(rows):
        for col_ in range(cols):
            fill = NAVY if (r_ + col_) % 2 == 0 else WHITE
            c.polygon([(fx + col_ * cs, fy + r_ * cs),
                       (fx + (col_ + 1) * cs, fy + r_ * cs),
                       (fx + (col_ + 1) * cs, fy + (r_ + 1) * cs),
                       (fx + col_ * cs, fy + (r_ + 1) * cs)], fill=fill)
    # label pill
    c.rrect([x - 6, y - 2, x + 66, y + 24], 6, fill=NAVY)
    c.text((x + 30, y + 11), "MASTERY", bold(13), WHITE)


def cisco_logo(c, x, y):
    """Classic Cisco 'signal bars' bridge logo + wordmark."""
    heights = [16, 26, 16, 26, 16, 26, 16, 26, 16]
    for i, h in enumerate(heights):
        bx = x + i * 8
        c.rrect([bx, y - h / 2, bx + 3.4, y + h / 2], 1.7, fill=WHITE)
    c.text((x + 34, y + 24), "CISCO", bold(15), WHITE, anchor="mm")


# ---- island definitions: (number, icon, label) in learning-path order ----
ISLANDS = [
    (1,  "overview",     "Overview Demo"),
    (2,  "compass",      "Foundations"),
    (3,  "agent",        "Agents"),
    (4,  "search",       "Visibility"),
    (5,  "telemetry",    "Connectors & Telemetry"),
    (6,  "ai",           "AI-Assisted Policy"),
    (7,  "lifecycle",    "Policy Lifecycle"),
    (8,  "shield",       "Security & Forensics"),
    (9,  "puzzle",       "Use Cases"),
    (10, "integrations", "Integrations"),
    (11, "container",    "Containers & K8s"),
    (12, "play",         "Official Demos"),
    (13, "wrench",       "Day-2 Ops"),
    (14, "strategy",     "Strategy"),
    (15, "siren",        "Incident Response"),
]


def build(path):
    big = Image.new("RGB", (W * S, H * S), SKY_TOP)
    d = ImageDraw.Draw(big)

    # vertical sky gradient
    for yy in range(H):
        t = yy / H
        d.line([(0, yy * S), (W * S, yy * S)], fill=blend(SKY_TOP, SKY_BOT, t),
               width=S)
    c = Canvas(d)

    # gentle wave strokes in the water
    for i in range(26):
        wy = 150 + i * 28 + (i % 3) * 6
        wx = 40 + (i * 53) % (W - 220)
        c.arc([wx, wy, wx + 90, wy + 34], 200, 340, fill=WAVE, width=2)

    # ---- layout: 5 columns x 3 rows, serpentine ----
    col_x = [225, 430, 635, 840, 1045]
    row_y = [270, 495, 720]

    pos = {}
    # row 0: 1..5 left->right
    for i in range(5):
        pos[i + 1] = (col_x[i], row_y[0])
    # row 1: 6..10 right->left
    for i in range(5):
        pos[6 + i] = (col_x[4 - i], row_y[1])
    # row 2: 11..15 left->right
    for i in range(5):
        pos[11 + i] = (col_x[i], row_y[2])

    start_xy = (95, row_y[0])
    mastery_xy = (1150, row_y[2])

    # ---- dotted trail (behind islands) ----
    def edge_r(n):   # right edge point of island n
        x, y = pos[n]; return (x + 90, y + 2)

    def edge_l(n):
        x, y = pos[n]; return (x - 90, y + 2)

    trail = [(start_xy[0] + 34, start_xy[1] - 4)]
    trail.append(edge_l(1))
    # row 1 across
    for n in range(1, 5):
        trail.append(edge_r(n)); trail.append(edge_l(n + 1))
    # curve 5 -> 6 down the right side
    x5, y5 = pos[5]; x6, y6 = pos[6]
    trail += [(x5 + 90, y5), (x5 + 150, y5 + 60), (x6 + 90, y6 - 60), edge_r(6)]
    # row 2 across (right->left)
    for n in range(6, 10):
        trail.append(edge_l(n)); trail.append(edge_r(n + 1))
    # curve 10 -> 11 down the left side
    x10, y10 = pos[10]; x11, y11 = pos[11]
    trail += [(x10 - 90, y10), (x10 - 150, y10 + 60), (x11 - 90, y11 - 60), edge_l(11)]
    # row 3 across
    for n in range(11, 15):
        trail.append(edge_r(n)); trail.append(edge_l(n + 1))
    trail += [edge_r(15), (mastery_xy[0] - 34, mastery_xy[1] - 4)]

    dotted_path(c, trail)

    # ---- markers + islands ----
    start_marker(c, *start_xy)
    for num, kind, label in ISLANDS:
        x, y = pos[num]
        island(c, x, y, kind, label, seed=num * 1.37)
    mastery_marker(c, *mastery_xy)

    # ---- header banner ----
    c.rrect([70, 22, 812, 100], 14, fill=NAVY, outline=CYAN, width=3)
    c.rrect([76, 90, 806, 97], 4, fill=CYAN)          # cyan underline
    cisco_logo(c, 100, 52)
    c.line([(216, 34), (216, 88)], fill=blend(NAVY, WHITE, 0.35), width=2)
    c.text((236, 60), "The CSW Learning Journey", bold(34), WHITE, anchor="lm")

    # subtitle
    c.text((441, 128), "Hop across the islands in order  \u00b7  or dive into any stop",
           font(15.5), NAVY_2, anchor="mm")

    out = big.resize((W, H), Image.LANCZOS)
    out.save(path)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.normpath(os.path.join(here, "..", "docs", "user-education",
                                         "csw-learning-journey.png"))
    p = build(dest)
    print(os.path.relpath(p), f"{os.path.getsize(p)/1024:.0f} KB")
