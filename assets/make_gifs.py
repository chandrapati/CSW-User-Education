#!/usr/bin/env python3
"""Generate two animated GIFs for the CSW-User-Education README:
  1) csw-containment.gif  -- ransomware blast radius WITHOUT vs WITH CSW
  2) csw-architecture.gif -- how CSW works (visibility -> context -> ADM -> analysis -> enforce)
All original artwork; vendor-neutral; no Cisco copyrighted assets.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1000, 560
BG     = (14, 23, 38)
PANEL  = (23, 37, 58)
PANEL2 = (30, 47, 72)
GREEN  = (46, 204, 113)
GREEN_D= (28, 130, 78)
RED    = (255, 77, 79)
RED_D  = (150, 35, 37)
BLUE   = (0, 188, 235)
BLUE_D = (10, 110, 140)
AMBER  = (245, 166, 35)
WHITE  = (236, 242, 248)
GREY   = (124, 146, 168)
LINE   = (58, 78, 104)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
]
BOLD_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
def _font(cands, size):
    for p in cands:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()
def font(size):  return _font(FONT_CANDIDATES, size)
def bold(size):  return _font(BOLD_CANDIDATES, size)

def base():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def ctext(d, xy, s, f, fill=WHITE, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def _blend(a, b, t):
    return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

SHADOW = (6, 11, 20)

def _shadow(d, x0, y0, x1, y1, r=12):
    d.rounded_rectangle([x0+5, y0+6, x1+5, y1+6], radius=r, fill=SHADOW)

def draw_server(d, cx, cy, w, h, body, edge, accent):
    x0, y0, x1, y1 = cx-w//2, cy-h//2, cx+w//2, cy+h//2
    _shadow(d, x0, y0, x1, y1)
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=body, outline=edge, width=3)
    d.rounded_rectangle([x0+3, y0+3, x1-3, y0+h//2-2], radius=9, fill=_blend(body, WHITE, .07))
    # power icon (top-left)
    d.ellipse([x0+12, y0+8, x0+24, y0+20], outline=accent, width=2)
    d.line([x0+18, y0+6, x0+18, y0+13], fill=accent, width=2)
    # status LEDs (top-right)
    for k in range(3):
        lx = x1-15-k*12
        d.ellipse([lx-3, y0+10, lx+3, y0+16], fill=accent if k == 0 else _blend(body, accent, .45))
    # drive bays
    for k in range(2):
        by = y0+32+k*18
        d.rounded_rectangle([x0+12, by, x1-12, by+11], radius=4, fill=_blend(body, WHITE, .10), outline=_blend(body, WHITE, .20))
        d.rounded_rectangle([x0+16, by+3, x0+32, by+8], radius=2, fill=_blend(body, WHITE, .26))
        d.ellipse([x1-21, by+3, x1-15, by+9], fill=accent)

def draw_database(d, cx, cy, w, h, body, edge, accent):
    cw = w-42
    x0, x1 = cx-cw//2, cx+cw//2
    ty, by = cy-h//2+12, cy+h//2-12
    eh = 16
    _shadow(d, x0, ty-eh//2, x1, by+eh//2, r=eh//2)
    d.rectangle([x0, ty, x1, by], fill=body)
    d.line([x0, ty, x0, by], fill=edge, width=3)
    d.line([x1, ty, x1, by], fill=edge, width=3)
    d.ellipse([x0, by-eh//2, x1, by+eh//2], fill=body, outline=edge, width=3)
    for f in (1, 2):
        ry = ty + (by-ty)*f//3
        d.arc([x0, ry-eh//2, x1, ry+eh//2], 0, 180, fill=edge, width=2)
    d.ellipse([x0, ty-eh//2, x1, ty+eh//2], fill=_blend(body, WHITE, .12), outline=edge, width=3)
    d.ellipse([cx-3, ty-3, cx+3, ty+3], fill=accent)

def draw_container(d, cx, cy, w, h, body, edge, accent):
    x0, y0, x1, y1 = cx-w//2, cy-h//2, cx+w//2, cy+h//2
    _shadow(d, x0, y0, x1, y1)
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=body, outline=edge, width=3)
    # microservice tiles (2 rows x 3 cols)
    for r in range(2):
        for c in range(3):
            sx = cx-31+c*31
            sy = cy-15+r*27
            d.rounded_rectangle([sx-11, sy-10, sx+11, sy+10], radius=3,
                                fill=_blend(body, accent, .32), outline=accent, width=2)
    # corner brackets
    L = 11
    for (bx, by, dx, dy) in [(x0+6, y0+6, 1, 1), (x1-6, y0+6, -1, 1), (x0+6, y1-6, 1, -1), (x1-6, y1-6, -1, -1)]:
        d.line([bx, by, bx+dx*L, by], fill=accent, width=3)
        d.line([bx, by, bx, by+dy*L], fill=accent, width=3)

# workload type per grid cell (S=server, D=database, C=container)
TYPES = ['S','D','C','S','D','C','S','D','C','S','D','C','S','D','C']

def draw_workload(d, idx, cx, cy, w, h, infected):
    body  = RED_D if infected else PANEL2
    edge  = RED if infected else GREEN
    accent= AMBER if infected else GREEN
    t = TYPES[idx % len(TYPES)]
    if t == 'D':
        draw_database(d, cx, cy, w, h, body, edge, accent)
    elif t == 'C':
        draw_container(d, cx, cy, w, h, body, edge, accent)
    else:
        draw_server(d, cx, cy, w, h, body, edge, accent)
    if infected:
        d.ellipse([cx-16, cy-16, cx+16, cy+16], fill=RED, outline=WHITE, width=2)
        draw_lock(d, cx, cy+1, 13, WHITE, RED)

def badge(d, cx, cy, txt, fill, fg=WHITE, pad=7, f=None):
    f = f or bold(15)
    bb = d.textbbox((0,0), txt, font=f)
    w = bb[2]-bb[0]; h = bb[3]-bb[1]
    d.rounded_rectangle([cx-w//2-pad, cy-h//2-pad, cx+w//2+pad, cy+h//2+pad], radius=9, fill=fill)
    ctext(d, (cx, cy-1), txt, f, fg)

def shield(d, cx, cy, r, fill, outline=WHITE):
    pts = [(cx, cy-r), (cx+r, cy-r+4), (cx+r, cy+2), (cx, cy+r), (cx-r, cy+2), (cx-r, cy-r+4)]
    d.polygon(pts, fill=fill, outline=outline)

def draw_lock(d, cx, cy, s, color, body):
    d.arc([cx-int(s*0.5), cy-int(s*0.95), cx+int(s*0.5), cy-int(s*0.1)], start=180, end=360,
          fill=color, width=max(2, int(s*0.22)))
    d.rounded_rectangle([cx-int(s*0.62), cy-int(s*0.2), cx+int(s*0.62), cy+int(s*0.8)],
                        radius=int(s*0.2), fill=body, outline=color, width=2)
    d.ellipse([cx-3, cy+int(s*0.12), cx+3, cy+int(s*0.12)+6], fill=color)

def draw_x(d, cx, cy, r, color, w=3):
    d.line([cx-r, cy-r, cx+r, cy+r], fill=color, width=w)
    d.line([cx-r, cy+r, cx+r, cy-r], fill=color, width=w)

def draw_warning(d, cx, cy, r, fill, fg):
    d.polygon([(cx, cy-r), (cx+r, cy+int(r*0.8)), (cx-r, cy+int(r*0.8))], fill=fill, outline=fg)
    d.line([cx, cy-int(r*0.25), cx, cy+int(r*0.3)], fill=fg, width=max(2, int(r*0.22)))
    d.ellipse([cx-2, cy+int(r*0.45), cx+3, cy+int(r*0.45)+5], fill=fg)

def draw_check(d, cx, cy, r, color, w=4):
    d.line([cx-r, cy, cx-int(r*0.2), cy+int(r*0.7)], fill=color, width=w)
    d.line([cx-int(r*0.2), cy+int(r*0.7), cx+r, cy-int(r*0.7)], fill=color, width=w)

def header_bar(d, title, sub, accent):
    d.rectangle([0, 0, W, 64], fill=PANEL)
    d.rectangle([0, 64, W, 68], fill=accent)
    ctext(d, (W//2, 26), title, bold(26), WHITE)
    ctext(d, (W//2, 50), sub, font(15), GREY)

def caption(d, txt, accent, big=None, big_icon=None):
    d.rectangle([0, H-66, W, H], fill=PANEL)
    d.rectangle([0, H-66, 6, H], fill=accent)
    if big:
        f = bold(22)
        bb = d.textbbox((0,0), big, font=f); tw = bb[2]-bb[0]
        tx = W//2 + (14 if big_icon else 0)
        ctext(d, (tx, H-43), big, f, accent)
        if big_icon == 'warn':
            draw_warning(d, tx - tw//2 - 18, H-43, 12, accent, (10,16,26))
        elif big_icon == 'check':
            draw_check(d, tx - tw//2 - 18, H-45, 11, accent, 4)
        ctext(d, (W//2, H-19), txt, font(15), GREY)
    else:
        ctext(d, (W//2, H-33), txt, font(18), WHITE)

# ----- grid layout for containment -----
COLS, ROWS = 5, 3
HW, HH = 132, 78
GX0, GY0 = 130, 120
GDX = (W - 2*GX0) // (COLS-1)
GDY = 130
def hpos(i):
    r, c = divmod(i, COLS)
    return GX0 + c*GDX, GY0 + r*GDY
def neighbors(i):
    r, c = divmod(i, COLS); out=[]
    if c>0: out.append(i-1)
    if c<COLS-1: out.append(i+1)
    if r>0: out.append(i-COLS)
    if r<ROWS-1: out.append(i+COLS)
    return out
N = COLS*ROWS

def bfs_waves(start):
    from collections import deque
    seen={start:0}; q=deque([start]); waves={0:[start]}
    while q:
        u=q.popleft()
        for v in neighbors(u):
            if v not in seen:
                seen[v]=seen[u]+1
                waves.setdefault(seen[v],[]).append(v)
                q.append(v)
    return seen, waves
DIST, WAVES = bfs_waves(0)
MAXW = max(WAVES)

def draw_links(d, infected, color, width=5):
    drawn=set()
    for i in infected:
        for j in neighbors(i):
            if j in infected and (j,i) not in drawn:
                x1,y1=hpos(i); x2,y2=hpos(j)
                d.line([x1,y1,x2,y2], fill=color, width=width)
                drawn.add((i,j))

def draw_all_shields(d):
    drawn=set()
    for i in range(N):
        for j in neighbors(i):
            if (j,i) in drawn: continue
            x1,y1=hpos(i); x2,y2=hpos(j)
            shield(d, (x1+x2)//2, (y1+y2)//2, 11, BLUE, WHITE)
            drawn.add((i,j))

def attacker(d, i):
    x,y=hpos(i)
    badge(d, x, y-HH//2-16, "ATTACKER", RED, WHITE, f=bold(13))

CAPS_A = {
 0:"Initial access \u2014 attacker lands on ONE workload",
 1:"Recon & enumeration \u2014 scanning the flat internal network",
 2:"Credential theft \u2014 Mimikatz, LSASS, Kerberoasting",
 3:"Lateral movement \u2014 SMB / RDP / WinRM / PsExec / SSH",
 4:"Privilege escalation \u2014 reaching DCs, backups, hypervisors",
}
def frame_A(infected_upto):
    img,d=base()
    header_bar(d, "WITHOUT Micro-Segmentation", "Flat network \u2014 nothing stops workload-to-workload traffic", RED)
    infected=set()
    for w in range(infected_upto+1):
        infected.update(WAVES.get(w,[]))
    draw_links(d, infected, RED_D, 5)
    for i in range(N):
        x,y=hpos(i)
        draw_workload(d, i, x, y, HW, HH, i in infected)
    if infected_upto==0: attacker(d,0)
    if infected_upto>=MAXW:
        caption(d, "One breach \u2192 the entire estate is encrypted", RED, big="RANSOMWARE FANS OUT", big_icon='warn')
    else:
        caption(d, CAPS_A.get(infected_upto, "Payload & impact \u2014 ransomware spreading"), RED)
    return img

def frame_B(stage):
    img,d=base()
    header_bar(d, "WITH Cisco Secure Workload", "Least-privilege policy on every workload \u2014 only required traffic allowed", BLUE)
    infected={0} if stage>=1 else set()
    for i in range(N):
        x,y=hpos(i)
        draw_workload(d, i, x, y, HW, HH, i in infected)
    draw_all_shields(d)
    if stage in (2,3):
        for j in neighbors(0):
            x1,y1=hpos(0); x2,y2=hpos(j)
            mx,my=(x1+x2)//2,(y1+y2)//2
            d.line([x1,y1,mx,my], fill=AMBER, width=5)
            shield(d, mx, my, 16, AMBER, WHITE)
            draw_x(d, mx, my+1, 6, RED_D, 3)
        badge(d, hpos(0)[0], hpos(0)[1]+HH//2+18, "BLOCKED", AMBER, (40,30,0), f=bold(14))
    if stage==0:
        caption(d, "Same attack, same flat-looking network \u2014 but every link now has a policy gate", BLUE)
    elif stage==1:
        caption(d, "Attacker still lands on host 1 \u2026", BLUE)
    elif stage in (2,3):
        caption(d, "\u2026 every lateral hop is DENIED by least-privilege policy", AMBER)
    else:
        caption(d, "Blast radius contained to 1 workload \u2014 ransomware cannot spread", GREEN, big="BREACH CONTAINED", big_icon='check')
    return img

def build_containment(path, sample_dir=None):
    frames=[]; durs=[]
    def add(img, ms): frames.append(img); durs.append(ms)
    add(frame_A(0), 1100)
    for w in range(1, MAXW+1): add(frame_A(w), 750)
    add(frame_A(MAXW), 1700)
    add(frame_B(0), 1300)
    add(frame_B(1), 1100)
    add(frame_B(2), 900)
    add(frame_B(3), 900)
    add(frame_B(4), 2200)
    if sample_dir:
        frame_A(0).save(os.path.join(sample_dir,"A_land.png"))
        frame_A(MAXW).save(os.path.join(sample_dir,"A_full.png"))
        frame_B(2).save(os.path.join(sample_dir,"B_blocked.png"))
        frame_B(4).save(os.path.join(sample_dir,"B_contained.png"))
    pal=[f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=durs, loop=0, disposal=2, optimize=True)
    return path

# ============ Architecture GIF ============
STAGES = [
    ("1  VISIBILITY",  "See every flow & process across every workload", BLUE),
    ("2  CONTEXT",     "Enrich with labels from CMDB, cloud, ISE, DNS",  BLUE),
    ("3  DISCOVERY",   "ADM + ML auto-discover application dependencies", AMBER),
    ("4  ANALYSIS",    "Simulate & validate policy \u2014 no app impact",     AMBER),
    ("5  ENFORCEMENT", "Least-privilege policy pushed everywhere",        GREEN),
]
SOURCES = ["VM","Bare-metal","Container","Cloud","Kubernetes"]
ENFORCE = ["Host firewall (agent)","Secure Firewall (agentless)","Cloud security groups"]

def arch_frame(active, pulse):
    img,d=base()
    d.rectangle([0,0,W,58], fill=PANEL); d.rectangle([0,58,W,62], fill=BLUE)
    ctext(d,(W//2,22),"How Cisco Secure Workload Works",bold(25),WHITE)
    ctext(d,(W//2,44),"One policy brain \u00b7 distributed enforcement \u00b7 agent + agentless",font(14),GREY)
    sw=150; sy=104; m=22
    first=m+sw//2; last=W-m-sw//2; step=(last-first)/(len(SOURCES)-1)
    for k,s in enumerate(SOURCES):
        x=int(first+step*k)
        d.rounded_rectangle([x-sw//2,sy-20,x+sw//2,sy+20],radius=9,fill=PANEL2,outline=BLUE_D,width=2)
        ctext(d,(x,sy),s,bold(15),WHITE)
        d.line([x,sy+20,x,158],fill=LINE,width=2)
    bx0,by0,bx1,by1=60,168,W-60,300
    d.rounded_rectangle([bx0,by0,bx1,by1],radius=16,fill=PANEL,outline=BLUE,width=3)
    ctext(d,((bx0+bx1)//2,by0+20),"CISCO SECURE WORKLOAD  \u2014  POLICY BRAIN",bold(17),BLUE)
    n=len(STAGES); pad=30
    seg=(bx1-bx0-2*pad)//n
    cy=by0+78
    for k,(t,sub,acc) in enumerate(STAGES):
        x=bx0+pad+seg*k+seg//2
        on = (k==active)
        fill = acc if on else PANEL2
        edge = WHITE if on else LINE
        d.rounded_rectangle([x-seg//2+8,cy-26,x+seg//2-8,cy+26],radius=10,fill=fill,outline=edge,width=3 if on else 2)
        ctext(d,(x,cy-7),t,bold(14), (10,16,26) if on else WHITE)
        if k<n-1:
            ax=x+seg//2-6
            d.line([ax,cy,ax+12,cy],fill=GREY,width=3)
            d.polygon([(ax+12,cy-5),(ax+12,cy+5),(ax+19,cy)],fill=GREY)
    px = bx0+pad + (seg*active+seg//2)
    d.ellipse([px-6+pulse, cy+30, px+6+pulse, cy+42], fill=STAGES[active][2])
    ey=360; ew=300
    centers=[ew//2+16, W//2, W-ew//2-16]
    for k,s in enumerate(ENFORCE):
        x=centers[k]
        on = active==4
        d.line([x,310,x,ey-22],fill=GREEN if on else LINE,width=3 if on else 2)
        d.rounded_rectangle([x-ew//2,ey-22,x+ew//2,ey+22],radius=9,
                            fill=_blend(PANEL2,GREEN_D,.5) if on else PANEL2,
                            outline=GREEN if on else LINE,width=3 if on else 2)
        ctext(d,(x,ey),s,bold(13),WHITE)
    t,sub,acc=STAGES[active]
    caption(d, sub, acc, big=t.strip())
    return img

def build_architecture(path, sample_dir=None):
    frames=[];durs=[]
    for k in range(len(STAGES)):
        for p in range(3):
            frames.append(arch_frame(k, p*5)); durs.append(260 if p<2 else 700)
    frames.append(arch_frame(4,10)); durs.append(1600)
    if sample_dir:
        arch_frame(0,0).save(os.path.join(sample_dir,"ARCH_s1.png"))
        arch_frame(2,5).save(os.path.join(sample_dir,"ARCH_s3.png"))
        arch_frame(4,10).save(os.path.join(sample_dir,"ARCH_s5.png"))
    pal=[f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=durs, loop=0, disposal=2, optimize=True)
    return path

if __name__=="__main__":
    here=os.path.dirname(os.path.abspath(__file__))
    samp=os.path.join(here,"_samples"); os.makedirs(samp,exist_ok=True)
    c=build_containment(os.path.join(here,"csw-containment.gif"), samp)
    a=build_architecture(os.path.join(here,"csw-architecture.gif"), samp)
    for f in (c,a):
        print(os.path.basename(f), f"{os.path.getsize(f)/1024:.0f} KB")
