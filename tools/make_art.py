#!/usr/bin/env python3
"""
Silver Star Plumbing — brand art generator.

Writes the site's SVG artwork from a small set of drawing primitives so the
whole set shares one palette, one line weight and one perspective. These are
generated illustrations, NOT photographs. Real job photos from the client
drop into img/photos/ and override these via js/config.js.

Run:  python3 tools/make_art.py
"""

import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")

# ---- palette (mirrors css/style.css) -------------------------------------
NAVY = "#0b1c2c"
NAVY2 = "#153352"
LINE = "#7fb6e8"
LINE_SOFT = "#3f6a95"
STEEL = "#c9d7e4"
ACCENT = "#2e9be0"
WATER = "#4fc3f7"
FLAME = "#ff9d4d"
ALERT = "#ff6b52"

W, H = 800, 600


def defs(extra=""):
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/>
  </linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8fa6bb"/><stop offset=".35" stop-color="{STEEL}"/>
    <stop offset=".62" stop-color="#7d94a9"/><stop offset="1" stop-color="#a9bccd"/>
  </linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{WATER}" stop-opacity=".15"/>
    <stop offset=".5" stop-color="{WATER}" stop-opacity=".45"/>
    <stop offset="1" stop-color="{WATER}" stop-opacity=".15"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="{ACCENT}" stop-opacity=".55"/>
    <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-opacity=".10" stroke-width="1"/>
  </pattern>
  {extra}
</defs>"""


def star(cx, cy, r, fill=STEEL, opacity=1.0):
    """Five-point star."""
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" opacity="{opacity}"/>'


def frame(body, watermark=False):
    wm = star(722, 92, 52, STEEL, 0.045) if watermark else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
{defs()}
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<ellipse cx="400" cy="330" rx="330" ry="250" fill="url(#glow)"/>
{wm}
{body}
<rect x="0" y="{H-4}" width="{W}" height="4" fill="{ACCENT}" opacity=".7"/>
</svg>"""


# ---- primitives ----------------------------------------------------------

def pipe(x1, y1, x2, y2, w=26):
    """Straight steel pipe segment."""
    if y1 == y2:
        return (f'<rect x="{min(x1,x2)}" y="{y1-w/2}" width="{abs(x2-x1)}" height="{w}" '
                f'rx="{w/2}" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="1.5"/>')
    return (f'<rect x="{x1-w/2}" y="{min(y1,y2)}" width="{w}" height="{abs(y2-y1)}" '
            f'rx="{w/2}" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="1.5"/>')


def coupling(cx, cy, w=34, h=18, vertical=False):
    if vertical:
        w, h = h, w
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="3" '
            f'fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="1.5"/>')


def droplet(cx, cy, s=1.0, fill=WATER, op=1.0):
    return (f'<path transform="translate({cx},{cy}) scale({s})" opacity="{op}" fill="{fill}" '
            f'd="M0,-30 C14,-10 22,2 22,12 A22,22 0 0 1 -22,12 C-22,2 -14,-10 0,-30 Z"/>')


def tank(cx, cy, w, h, label_lines=0):
    r = w / 2
    body = (f'<rect x="{cx-r}" y="{cy-h/2}" width="{w}" height="{h}" rx="{r*0.55}" '
            f'fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2"/>')
    ribs = "".join(
        f'<line x1="{cx-r+12}" y1="{cy-h/2+30+i*26}" x2="{cx+r-12}" y2="{cy-h/2+30+i*26}" '
        f'stroke="{LINE_SOFT}" stroke-opacity=".45" stroke-width="1.5"/>'
        for i in range(label_lines))
    return body + ribs


def gauge(cx, cy, r=26):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NAVY}" stroke="{STEEL}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{LINE}" '
            f'stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="3 5"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{cx+r*0.55}" y2="{cy-r*0.45}" stroke="{ACCENT}" '
            f'stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{STEEL}"/>')


def valve_wheel(cx, cy, r=30):
    spokes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r*0.9*c:.1f}" y2="{cy + r*0.9*s:.1f}" '
        f'stroke="{ALERT}" stroke-width="5" stroke-linecap="round"/>'
        for c, s in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ALERT}" stroke-width="7"/>'
            + spokes + f'<circle cx="{cx}" cy="{cy}" r="7" fill="{STEEL}"/>')


def arcs(cx, cy, count=3, r0=42, step=26, color=ACCENT, start=-140, sweep=100):
    import math
    out = []
    for i in range(count):
        r = r0 + i * step
        a1 = math.radians(start)
        a2 = math.radians(start + sweep)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        out.append(f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" '
                   f'stroke="{color}" stroke-width="4" stroke-linecap="round" '
                   f'opacity="{0.85 - i*0.22:.2f}"/>')
    return "".join(out)


# ---- scenes --------------------------------------------------------------

def scene_water_heater():
    b = tank(360, 320, 210, 300, label_lines=5)
    b += pipe(300, 150, 300, 175, 22) + pipe(300, 150, 420, 150, 22)
    b += pipe(420, 100, 420, 152, 22) + coupling(300, 178, vertical=True)
    b += f'<rect x="300" y="405" width="120" height="34" rx="8" fill="{NAVY}" opacity=".55"/>'
    b += gauge(548, 250)
    b += droplet(560, 400, 1.1, WATER, .9)
    b += f'<circle cx="360" cy="470" r="26" fill="{NAVY}" stroke="{STEEL}" stroke-width="3"/>'
    b += f'<path d="M348,470 q12,-16 24,0 q-12,16 -24,0" fill="{FLAME}" opacity=".9"/>'
    return frame(b)


def scene_repipe():
    b = ""
    for i, y in enumerate((180, 290, 400)):
        b += pipe(120, y, 640, y, 24)
        b += coupling(300 + i * 60, y)
    b += pipe(640, 180, 640, 400, 24)
    b += coupling(640, 180, vertical=True) + coupling(640, 400, vertical=True)
    b += gauge(180, 480, 30)
    b += droplet(520, 490, 1.0, WATER, .8)
    return frame(b)


def scene_shower_valve():
    b = f'<rect x="250" y="120" width="300" height="360" rx="18" fill="{NAVY}" opacity=".5" stroke="{LINE_SOFT}" stroke-width="2"/>'
    for gx in range(4):
        for gy in range(5):
            b += (f'<rect x="{262+gx*72}" y="{132+gy*68}" width="66" height="62" rx="4" '
                  f'fill="none" stroke="{LINE}" stroke-opacity=".18" stroke-width="1.5"/>')
    b += f'<circle cx="400" cy="330" r="72" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2"/>'
    b += f'<circle cx="400" cy="330" r="46" fill="{NAVY}" opacity=".75"/>'
    b += f'<rect x="392" y="262" width="16" height="60" rx="8" fill="{ACCENT}"/>'
    b += f'<circle cx="400" cy="330" r="14" fill="{STEEL}"/>'
    b += pipe(400, 150, 400, 200, 20)
    b += (f'<path d="M330,190 h140 l-16,26 h-108 Z" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="1.5"/>')
    for i in range(7):
        x = 342 + i * 20
        b += f'<line x1="{x}" y1="220" x2="{x-6}" y2="252" stroke="{WATER}" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
    return frame(b)


def scene_softener():
    """Water softener: resin tank with a control valve head, plus the brine
    tank and the line between them."""
    b = (f'<rect x="228" y="206" width="150" height="266" rx="70" '
         f'fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2.5"/>')
    b += (f'<rect x="210" y="136" width="186" height="78" rx="16" '            # valve head
          f'fill="{NAVY2}" stroke="{STEEL}" stroke-width="2.5"/>')
    b += f'<rect x="230" y="158" width="62" height="28" rx="6" fill="{WATER}" opacity=".5"/>'
    b += f'<circle cx="352" cy="172" r="15" fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    b += pipe(110, 175, 212, 175, 22) + pipe(394, 175, 452, 175, 22)
    b += coupling(158, 175)
    b += (f'<rect x="470" y="252" width="162" height="220" rx="14" '           # brine tank
          f'fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2.5"/>')
    b += (f'<rect x="458" y="228" width="186" height="30" rx="10" '            # lid
          f'fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="2"/>')
    b += f'<rect x="496" y="298" width="110" height="152" rx="8" fill="{NAVY}" opacity=".4"/>'
    for i in range(18):                                                        # salt
        cx, cy = 508 + (i % 6) * 18, 424 - (i // 6) * 26
        b += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{STEEL}" opacity=".7"/>'
    b += (f'<path d="M396,172 C444,172 452,204 452,240" fill="none" '          # brine line
          f'stroke="{ACCENT}" stroke-width="7" stroke-linecap="round" opacity=".85"/>')
    return frame(b)

def scene_ro():
    """Under-sink reverse osmosis: three filter stages, the bladder storage
    tank, and the dedicated faucet coming up through the counter."""
    b = f'<rect x="50" y="150" width="700" height="22" rx="6" fill="{STEEL}" opacity=".85"/>'
    b += (f'<path d="M186,150 v-58 q0,-34 34,-34 q34,0 34,34 v20" fill="none" '  # RO faucet
          f'stroke="url(#steel)" stroke-width="16" stroke-linecap="round"/>')
    b += f'<rect x="245" y="108" width="18" height="18" rx="4" fill="{STEEL}"/>'
    b += droplet(254, 140, .3, WATER, .9)
    b += f'<rect x="150" y="248" width="330" height="18" rx="6" fill="{NAVY2}" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    for i, x in enumerate((200, 305, 410)):
        b += f'<rect x="{x-43}" y="234" width="86" height="34" rx="8" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
        b += f'<rect x="{x-36}" y="268" width="72" height="152" rx="14" fill="url(#glass)" stroke="{STEEL}" stroke-width="2"/>'
        b += f'<rect x="{x-22}" y="298" width="44" height="108" rx="10" fill="{WATER}" opacity="{.18+i*.14:.2f}"/>'
    b += f'<ellipse cx="606" cy="362" rx="88" ry="102" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2.5"/>'
    b += f'<ellipse cx="606" cy="362" rx="54" ry="68" fill="{WATER}" opacity=".2"/>'
    b += f'<rect x="592" y="246" width="28" height="26" rx="6" fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    b += (f'<path d="M453,256 C520,256 566,252 606,250" fill="none" stroke="{ACCENT}" '
          f'stroke-width="7" stroke-linecap="round" opacity=".8"/>')
    b += (f'<path d="M200,234 C200,198 212,178 250,172" fill="none" stroke="{ACCENT}" '
          f'stroke-width="7" stroke-linecap="round" opacity=".8"/>')
    return frame(b)

def scene_gas():
    """Gas line: black iron with a tee down to a capped drip leg, a lever gas
    cock, yellow flex connector to the appliance, and a test gauge."""
    IRON, IRON_D, IRON_L = "#55626e", "#2f3a44", "#6d7b86"

    def ipipe(x1, y1, x2, y2, w=28):
        if y1 == y2:
            return (f'<rect x="{min(x1,x2)}" y="{y1-w/2}" width="{abs(x2-x1)}" height="{w}" '
                    f'rx="4" fill="{IRON}" stroke="{IRON_D}" stroke-width="2"/>')
        return (f'<rect x="{x1-w/2}" y="{min(y1,y2)}" width="{w}" height="{abs(y2-y1)}" '
                f'rx="4" fill="{IRON}" stroke="{IRON_D}" stroke-width="2"/>')

    def fitting(cx, cy, w=44, h=38):
        return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="5" '
                f'fill="{IRON_L}" stroke="{IRON_D}" stroke-width="2"/>')

    b = ipipe(60, 300, 470, 300)
    b += fitting(292, 300)
    b += ipipe(292, 300, 292, 424)
    b += fitting(292, 434, 46, 26)
    b += f'<rect x="392" y="276" width="68" height="48" rx="9" fill="{IRON_L}" stroke="{IRON_D}" stroke-width="2"/>'
    b += f'<rect x="417" y="230" width="18" height="52" rx="9" fill="{FLAME}"/>'
    b += f'<rect x="396" y="216" width="60" height="20" rx="10" fill="{FLAME}"/>'
    b += ipipe(460, 300, 536, 300)
    b += (f'<path d="M536,300 C600,300 600,238 656,238" fill="none" '
          f'stroke="#e8c25a" stroke-width="24" stroke-linecap="round"/>')
    b += (f'<path d="M536,300 C600,300 600,238 656,238" fill="none" '
          f'stroke="#a8862f" stroke-width="24" stroke-linecap="round" '
          f'stroke-dasharray="3 13" opacity=".7"/>')
    b += f'<rect x="650" y="212" width="36" height="52" rx="8" fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="2"/>'
    b += gauge(150, 190, 34)
    b += ipipe(150, 222, 150, 288, 16)
    return frame(b)

def scene_shutoff():
    """Automatic water shut-off valve: motorised body inline on the main,
    status ring, and the phone alert that comes with it."""
    b = pipe(50, 340, 750, 340, 30)
    for x in (286, 514):                                   # union nuts
        b += (f'<rect x="{x-15}" y="308" width="30" height="64" rx="5" '
              f'fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="1.5"/>')
    for x in (120, 186):                                   # flow arrows
        b += (f'<path d="M{x},340 h26 m-10,-10 l10,10 l-10,10" fill="none" '
              f'stroke="{WATER}" stroke-width="4.5" stroke-linecap="round" '
              f'stroke-linejoin="round" opacity=".8"/>')
    b += (f'<rect x="330" y="250" width="140" height="180" rx="28" '
          f'fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2.5"/>')
    b += (f'<rect x="352" y="192" width="96" height="66" rx="18" '           # actuator
          f'fill="{NAVY2}" stroke="{STEEL}" stroke-width="2.5"/>')
    b += f'<rect x="370" y="210" width="60" height="9" rx="4.5" fill="{ACCENT}" opacity=".85"/>'
    b += f'<circle cx="400" cy="336" r="42" fill="{NAVY}" opacity=".6"/>'
    b += (f'<circle cx="400" cy="336" r="42" fill="none" stroke="{ACCENT}" '   # status ring
          f'stroke-width="9" stroke-linecap="round" stroke-dasharray="198 66" '
          f'transform="rotate(-90 400 336)"/>')
    b += f'<circle cx="400" cy="336" r="21" fill="{NAVY}" stroke="{STEEL}" stroke-width="2"/>'
    b += (f'<path d="M390,330 h20 M390,340 h13" stroke="{WATER}" stroke-width="3.5" '
          f'stroke-linecap="round"/>')
    b += f'<rect x="596" y="148" width="122" height="204" rx="20" fill="{NAVY}" stroke="{STEEL}" stroke-width="3"/>'
    b += f'<rect x="609" y="171" width="96" height="158" rx="8" fill="{NAVY2}"/>'
    b += f'<circle cx="657" cy="207" r="19" fill="{ALERT}"/>'
    b += f'<path d="M657,197 v13" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
    b += f'<circle cx="657" cy="217" r="2.6" fill="#fff"/>'
    for i, w in enumerate((66, 52, 38)):
        b += f'<rect x="{657-w/2}" y="{242+i*22}" width="{w}" height="8" rx="4" fill="{STEEL}" opacity=".45"/>'
    return frame(b)

def scene_leak_detect():
    """Leak detection: a pressurised line leaking under the slab, located with
    a ground microphone and a receiver rather than by demolition."""
    b = f'<rect x="30" y="326" width="740" height="26" rx="6" fill="{STEEL}" opacity=".32"/>'
    b += f'<rect x="30" y="352" width="740" height="128" fill="{NAVY}" opacity=".5"/>'
    b += pipe(30, 442, 770, 442, 26)
    b += f'<circle cx="430" cy="442" r="10" fill="{ALERT}"/>'
    for dx, dy in ((-34, -46), (-8, -56), (20, -44)):
        b += (f'<path d="M430,432 q{dx*0.5},{dy*0.5} {dx},{dy}" fill="none" stroke="{WATER}" '
              f'stroke-width="5" stroke-linecap="round" opacity=".75"/>')
    b += arcs(430, 442, 4, 50, 30, ACCENT, -170, 160)
    b += f'<ellipse cx="430" cy="322" rx="54" ry="17" fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="2"/>'
    b += f'<rect x="409" y="278" width="42" height="46" rx="11" fill="{NAVY2}" stroke="{STEEL}" stroke-width="2"/>'
    b += (f'<path d="M430,278 C430,232 536,246 560,214" fill="none" stroke="{ACCENT}" '
          f'stroke-width="6" stroke-linecap="round"/>')
    b += f'<rect x="540" y="116" width="184" height="124" rx="16" fill="{NAVY}" stroke="{STEEL}" stroke-width="3"/>'
    b += f'<rect x="558" y="134" width="148" height="70" rx="8" fill="{NAVY2}"/>'
    for i, h in enumerate((16, 28, 44, 32, 20)):
        b += f'<rect x="{574+i*27}" y="{196-h}" width="15" height="{h}" rx="3" fill="{WATER}" opacity=".85"/>'
    b += f'<circle cx="632" cy="222" r="7" fill="{ACCENT}"/>'
    return frame(b)

def scene_drain():
    b = f'<rect x="300" y="110" width="200" height="26" rx="8" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    b += pipe(400, 136, 400, 300, 30)
    b += (f'<path d="M400,300 v40 a56,56 0 0 0 112,0 v-40" fill="none" stroke="url(#steel)" '
          f'stroke-width="30" stroke-linecap="round"/>')
    b += pipe(512, 300, 512, 190, 30)
    b += coupling(400, 240, vertical=True) + coupling(512, 240, vertical=True)
    b += f'<circle cx="456" cy="356" r="17" fill="{WATER}" opacity=".55"/>'
    b += droplet(400, 190, .55, WATER, .8)
    b += arcs(456, 356, 2, 84, 26, ACCENT, -30, 90)
    return frame(b)


def scene_fixtures():
    b = f'<rect x="230" y="380" width="340" height="24" rx="8" fill="{NAVY}" opacity=".6" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    b += (f'<path d="M300,380 v-120 a80,80 0 0 1 160,0 v30" fill="none" stroke="url(#steel)" '
          f'stroke-width="24" stroke-linecap="round"/>')
    b += f'<rect x="444" y="286" width="32" height="26" rx="6" fill="{STEEL}" stroke="{LINE_SOFT}" stroke-width="1.5"/>'
    for i, dy in enumerate((330, 360, 388)):
        b += droplet(460, dy, .34 - i * .06, WATER, .85 - i * .2)
    b += f'<rect x="262" y="404" width="76" height="16" rx="6" fill="url(#steel)"/>'
    b += f'<circle cx="300" cy="404" r="20" fill="none" stroke="{ACCENT}" stroke-width="5"/>'
    b += gauge(600, 210, 28)
    return frame(b)


def scene_emergency():
    """Emergency: a ruptured line spraying, and the main ball valve being shut."""
    import math
    b = pipe(30, 300, 770, 300, 34)
    b += (f'<path d="M348,300 q28,-9 56,0" fill="none" stroke="{NAVY}" '
          f'stroke-width="11" stroke-linecap="round"/>')
    b += (f'<path d="M352,286 l15,-13 l11,15 l17,-11 l9,17" fill="none" stroke="{NAVY}" '
          f'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    for a in (-64, -44, -24, -4, 16):
        r = math.radians(a - 90)
        b += (f'<path d="M376,282 L{376+128*math.cos(r):.0f},{282+128*math.sin(r):.0f}" '
              f'stroke="{WATER}" stroke-width="6" stroke-linecap="round" opacity=".65"/>')
    for dx, dy, s in ((-92, -128, .34), (10, -158, .28), (86, -120, .32)):
        b += droplet(376 + dx, 282 + dy, s, WATER, .55)
    b += f'<rect x="558" y="266" width="100" height="68" rx="11" fill="url(#steel)" stroke="{LINE_SOFT}" stroke-width="2.5"/>'
    b += f'<rect x="600" y="192" width="17" height="80" rx="8" fill="{ALERT}"/>'
    b += f'<rect x="572" y="176" width="90" height="23" rx="11" fill="{ALERT}"/>'
    b += f'<circle cx="608" cy="300" r="13" fill="{NAVY}" stroke="{STEEL}" stroke-width="2"/>'
    b += (f'<path d="M162,198 l60,104 h-120 Z" fill="{ALERT}" opacity=".93" '
          f'stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    b += f'<path d="M162,232 v36" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
    b += f'<circle cx="162" cy="284" r="4.6" fill="#fff"/>'
    return frame(b)

def scene_hero():
    """Wide hero band, 1600x900."""
    global W, H
    W, H = 1600, 900
    b = ""
    for i, y in enumerate((250, 400, 550)):
        b += pipe(-40, y, 700 + i * 120, y, 30)
        b += coupling(320 + i * 90, y, 40, 22)
    b += pipe(700, 250, 700, 550, 30)
    b += pipe(820, 400, 1660, 400, 30)
    b += coupling(700, 250, 24, 44, vertical=True)
    b += tank(1080, 470, 190, 300, label_lines=4)
    b += gauge(1330, 300, 34)
    b += droplet(900, 620, 1.4, WATER, .55)
    b += star(1400, 640, 90, STEEL, .10)
    out = frame(b, watermark=False)
    W, H = 800, 600
    return out


def scene_logo():
    """Wordmark-free star mark for header/favicon, 128x128."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img">
<defs>
 <linearGradient id="s" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="{STEEL}"/>
  <stop offset="1" stop-color="#7d94a9"/>
 </linearGradient>
</defs>
<circle cx="64" cy="64" r="60" fill="{NAVY}" stroke="{ACCENT}" stroke-width="4"/>
{star(64, 58, 34, 'url(#s)')}
<path d="M64 84 c9 13 14 20 14 26 a14 14 0 0 1 -28 0 c0-6 5-13 14-26 Z" fill="{WATER}" opacity=".95"/>
</svg>"""


SCENES = {
    "hero.svg": scene_hero,
    "logo.svg": scene_logo,
    "svc-water-heaters.svg": scene_water_heater,
    "svc-repipe.svg": scene_repipe,
    "svc-shower-valves.svg": scene_shower_valve,
    "svc-water-softeners.svg": scene_softener,
    "svc-reverse-osmosis.svg": scene_ro,
    "svc-gas-lines.svg": scene_gas,
    "svc-shutoff-valves.svg": scene_shutoff,
    "svc-leak-detection.svg": scene_leak_detect,
    "svc-drains.svg": scene_drain,
    "svc-fixtures.svg": scene_fixtures,
    "svc-emergency.svg": scene_emergency,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SCENES.items():
        path = os.path.join(OUT, name)
        with open(path, "w") as f:
            f.write(fn())
        print(f"wrote {path} ({os.path.getsize(path)} bytes)")
    print(f"\n{len(SCENES)} files written to {OUT}")


if __name__ == "__main__":
    main()
