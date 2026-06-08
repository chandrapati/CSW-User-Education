#!/usr/bin/env python3
"""Generate a polished phased-adoption roadmap banner for the CSW-User-Education
README. Dark theme, gantt-style colored phase pills, milestone gridlines, icons,
and short value tags. All original artwork; vendor-neutral.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1180, 560
BG     = (14, 23, 38)
PANEL  = (23, 37, 58)
PANEL2 = (30, 47, 72)
WHITE  = (236, 242, 248)
GREY   = (138, 159, 182)
GRID   = (44, 60, 84)
INK    = (10, 16, 26)

# per-phase accent colors (distinct, modern)
P_BLUE  = (38, 176, 235)
P_TEAL  = (38, 200, 162)
P_AMBER = (245, 176, 60)
P_ORANGE= (255, 120, 56)
P_VIOLET= (150, 122, 240)

FONT = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
BOLDF = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Black.ttf"]
def _f(c, s):
    for p in c:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, s)
            except Exception: pass
    return ImageFont.load_default()
def font(s): return _f(FONT, s)
def bold(s): return _f(BOLDF, s)

def _blend(a, b, t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

def ctext(d, xy, s, f, fill=WHITE, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

# ---- timeline scale ----
WX0, WX1 = 348, 1132          # pixel span of the week axis
WMIN, WMAX = 0, 13
def wx(week):
    return WX0 + (week - WMIN) / (WMAX - WMIN) * (WX1 - WX0)

ROW_Y0, ROW_DY = 156, 74
BAR_H = 32
GRID_TOP, GRID_BOT = 120, ROW_Y0 + 4*ROW_DY + 30

# phase: (num, name, value, color, start, end, continuous, icon)
PHASES = [
    (1, "Visibility",          "See every flow & dependency",   P_BLUE,   0, 2,  False, "eye"),
    (2, "Macro Segmentation",  "Biggest blast-radius cut",      P_TEAL,   2, 4,  False, "shield"),
    (3, "Micro-Segmentation",  "Per-app least privilege (ADM)", P_AMBER,  4, 12, False, "graph"),
    (4, "Risk Reduction",      "Shrink CVE exposure same-day",  P_ORANGE, 8, 13, True,  "bug"),
    (5, "Forensics & IR",      "Detection + evidence trail",    P_VIOLET, 8, 13, True,  "lens"),
]
MILES = [(0, "0"), (2, "2"), (4, "4"), (8, "8"), (12, "12+")]


def icon(d, kind, cx, cy, col):
    if kind == "eye":
        d.ellipse([cx-10, cy-6, cx+10, cy+6], outline=col, width=2)
        d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=col)
    elif kind == "shield":
        pts = [(cx, cy-9), (cx+8, cy-6), (cx+8, cy+1), (cx, cy+9), (cx-8, cy+1), (cx-8, cy-6)]
        d.polygon(pts, outline=col, width=2)
        d.line([cx-4, cy, cx-1, cy+4], fill=col, width=2)
        d.line([cx-1, cy+4, cx+5, cy-4], fill=col, width=2)
    elif kind == "graph":
        nodes = [(cx-8, cy+6), (cx+8, cy+6), (cx, cy-8)]
        for a in range(len(nodes)):
            d.line([nodes[a], nodes[(a+1) % 3]], fill=col, width=2)
        for nx, ny in nodes:
            d.ellipse([nx-3, ny-3, nx+3, ny+3], fill=col)
    elif kind == "bug":
        d.polygon([(cx, cy-9), (cx+9, cy+7), (cx-9, cy+7)], outline=col, width=2)
        d.line([cx, cy-2, cx, cy+3], fill=col, width=2)
        d.ellipse([cx-1, cy+5, cx+2, cy+8], fill=col)
    elif kind == "lens":
        d.ellipse([cx-9, cy-9, cx+3, cy+3], outline=col, width=2)
        d.line([cx+2, cy+2, cx+9, cy+9], fill=col, width=3)


def pill(d, x0, x1, cy, color, continuous=False):
    r = BAR_H // 2
    if continuous:
        x1 = x1  # extend; chevrons added after
    d.rounded_rectangle([x0, cy-r, x1, cy+r], radius=r, fill=color)
    # top sheen
    d.rounded_rectangle([x0+3, cy-r+3, x1-3, cy-2], radius=max(3, r-4),
                        fill=_blend(color, WHITE, .22))
    if continuous:
        for k in range(3):
            bxc = x1 + 8 + k*12
            d.polygon([(bxc, cy-7), (bxc, cy+7), (bxc+8, cy)],
                      fill=_blend(color, WHITE, .15 + k*0.0))


def build(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    ctext(d, (W//2, 34), "Phased Adoption Roadmap", bold(30), WHITE)
    ctext(d, (W//2, 64), "Each phase delivers value on its own  \u2014  value compounds left \u2192 right",
          font(15), GREY)

    # left panel divider
    d.line([336, GRID_TOP-6, 336, GRID_BOT], fill=GRID, width=2)

    # week gridlines + labels
    for wk, lab in MILES:
        x = int(wx(wk))
        d.line([x, GRID_TOP, x, GRID_BOT], fill=GRID, width=2)
        ctext(d, (x, GRID_TOP-14), f"Week {lab}", font(13), GREY)

    # continuous band marker (week 8 onward)
    d.text((wx(8)+6, GRID_BOT+8), "", font=font(12), fill=GREY)

    for i, (num, name, val, col, s, e, cont, ic) in enumerate(PHASES):
        cy = ROW_Y0 + i*ROW_DY
        # number badge
        d.ellipse([28, cy-18, 64, cy+18], fill=col)
        ctext(d, (46, cy), str(num), bold(20), INK)
        # icon
        icon(d, ic, 92, cy, col)
        # name + value (left panel)
        d.text((118, cy-13), name, font=bold(17), fill=col, anchor="lm")
        d.text((118, cy+12), val, font=font(12), fill=GREY, anchor="lm")
        # bar
        x0, x1 = int(wx(s)), int(wx(e))
        pill(d, x0, x1, cy, col, continuous=cont)
        # window / status label on the bar
        if cont:
            ctext(d, ((x0+x1)//2, cy), f"Week {s} \u2192 ongoing", bold(13), INK)
        else:
            ctext(d, ((x0+x1)//2, cy), f"Weeks {s}\u2013{e}", bold(13), INK)

    # footer note
    d.rounded_rectangle([28, GRID_BOT+18, W-28, H-20], radius=10, fill=PANEL)
    ctext(d, (W//2, (GRID_BOT+18 + H-20)//2),
          "Stop after Phase 2 and you've already cut ransomware fan-out and isolated prod from non-prod  \u00b7  "
          "Phases 4\u20135 run continuously",
          font(14), _blend(WHITE, GREY, .3))

    img.save(path)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    p = build(os.path.join(here, "csw-roadmap.png"))
    print(os.path.basename(p), f"{os.path.getsize(p)/1024:.0f} KB")
