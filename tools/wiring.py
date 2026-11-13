"""Generate breadboard-style wiring diagrams as SVG (pin-to-pin, coloured wires).

Fritzing is GUI-only and this host has no Qt/X, so the layout is built as data
here and emitted as SVG. The MCU is drawn as a board (green PCB, metal shield,
antenna keepout, camera FPC, USB-C) with colour-coded header pins.

Self-checks: label collisions, canvas overflow, wire endpoints must sit on a
pin/bus/rail, no wire may run through a board, XML parses.
"""

import os

W_WHITE = "#e6edf3"
BG = "#0d1117"
BOARD = "#161b22"
STROKE = "#30363d"
PIN = "#0b0f14"
PIN_STROKE = "#4b5563"
MUTED = "#8b949e"
DIM = "#6e7681"
RED = "#f85149"
GREY = "#8b949e"
ORANGE = "#d29922"
BLUE = "#58a6ff"
GREEN = "#3fb950"
PURPLE = "#bc8cff"
TEAL = "#2dd4bf"

# board look
PCB_GREEN = "#1b4d2e"
PCB_DARK = "#133622"
PCB_STROKE = "#2e7d43"
SILK = "#cfe8d8"
SHIELD = "#c9d1d9"
SHIELD_STROKE = "#6e7681"
GOLD = "#d4a72c"
SILVER = "#aeb6c0"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', sans-serif"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.parts, self.labels = [], []
        self.pin_pts, self.boxes, self.wires, self.bus_ys = [], [], [], []
        self.rails, self.nodes, self.hbus = [], [], []

    def node(self, x, y):
        """Electrical terminal / junction that is not a pin (resistor end, cap plate)."""
        self.nodes.append((x, y))

    def busline(self, y, x0, x1, color=GREY, width=3.0):
        self.hbus.append((x0, x1, y))
        self.path(f"M {x0},{y} L {x1},{y}", color, width)

    # ------------------------------------------------------------------ text
    def esc(self, s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=12, fill=W_WHITE, anchor="start", weight="400", mono=True):
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{self.esc(s)}</text>'
        )

    def label(self, x, y, s, size=10, fill=MUTED, anchor="middle", plate=False):
        tw = len(s) * size * 0.60
        x0 = x - tw / 2 if anchor == "middle" else (x - tw if anchor == "end" else x)
        if plate:
            self.parts.append(
                f'<rect x="{x0-4:.1f}" y="{y-size-2:.1f}" width="{tw+8:.1f}" '
                f'height="{size+7}" rx="3" fill="{BG}" fill-opacity="0.95"/>'
            )
        self.labels.append((x0, y - size, x0 + tw, y + 4, s))
        self.text(x, y, s, size=size, fill=fill, anchor=anchor)

    # ---------------------------------------------------------------- shapes
    def rect(self, x, y, w, h, fill, stroke=None, rx=8, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        st = f' stroke="{stroke}"' if stroke else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}"{st} stroke-width="{sw}"{d}/>'
        )

    def box(self, x, y, w, h, title, sub=None, fill=BOARD, stroke=STROKE):
        self.boxes.append((x, y, x + w, y + h, title))
        self.rect(x, y, w, h, fill, stroke, rx=10)
        self.text(x + 12, y + 22, title, size=12.5, fill=W_WHITE, weight="600", mono=False)
        if sub:
            self.text(x + 12, y + 38, sub, size=9.5, fill=MUTED, mono=False)

    def path(self, d, color, width=3.0, dash=None, opacity=1.0):
        dsh = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"{dsh}/>'
        )

    def wire(self, pts, color, width=3.0, r=12, dots=True):
        self.wires.append((list(pts), color))
        d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
        for i in range(1, len(pts) - 1):
            x1, y1 = pts[i]
            ax, ay = pts[i - 1]
            bx, by = pts[i + 1]

            def shrink(p, q):
                dx, dy = q[0] - p[0], q[1] - p[1]
                ln = (dx * dx + dy * dy) ** 0.5 or 1.0
                k = min(r, ln / 2.0)
                return (p[0] + dx / ln * k, p[1] + dy / ln * k)

            a, b = shrink((x1, y1), (ax, ay)), shrink((x1, y1), (bx, by))
            d += f" L {a[0]:.1f},{a[1]:.1f} Q {x1:.1f},{y1:.1f} {b[0]:.1f},{b[1]:.1f}"
        d += f" L {pts[-1][0]:.1f},{pts[-1][1]:.1f}"
        self.path(d, color, width)
        if dots:
            for p in (pts[0], pts[-1]):
                self.parts.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="3.4" fill="{color}"/>')

    def resistor(self, x, y, length=46, vertical=False, color=PURPLE):
        n = 6
        pts = [(x, y)]
        for i in range(1, n + 1):
            off = 5 if i % 2 else -5
            pts.append((x + (off if vertical else i * length / n),
                        y + (i * length / n if vertical else off)))
        pts.append((x, y + length) if vertical else (x + length, y))
        self.path("M " + " L ".join(f"{a:.1f},{b:.1f}" for a, b in pts), color, 2.4)
        return pts[-1]

    def rail(self, x, y0, y1, color, name):
        self.rails.append((x, y0, y1))
        self.path(f"M {x},{y0} L {x},{y1}", color, 5)
        if name:
            self.text(x + 10, y0 - 8, name, size=10.5, fill=color)

    # ------------------------------------------------------------------ pins
    def pins(self, x, y, w, names, side="right", step=26, top=52):
        out = {}
        for i, n in enumerate(names):
            py = y + top + i * step
            px = x + w if side == "right" else x
            self.rect(px - 7, py - 7, 14, 14, PIN, PIN_STROKE, rx=2, sw=1)
            if side == "right":
                self.text(px - 13, py + 4, n, size=9.5, fill=MUTED, anchor="end")
            else:
                self.text(px + 13, py + 4, n, size=9.5, fill=MUTED)
            out[n] = (px, py)
            self.pin_pts.append((px, py, n))
        return out

    def pins_bottom(self, x, y, names, start=30, step=44):
        out = {}
        for i, n in enumerate(names):
            px = x + start + i * step
            self.rect(px - 7, y - 7, 14, 14, PIN, PIN_STROKE, rx=2, sw=1)
            self.text(px, y + 21, n, size=9, fill=MUTED, anchor="middle")
            out[n] = (px, y)
            self.pin_pts.append((px, y, n))
        return out

    # ------------------------------------------------------- coloured pins
    def cpin(self, px, py, name, color, side="right"):
        """Colour-coded header pin (colour = function). Label sits inside the board."""
        self.rect(px - 6, py - 6, 12, 12, color, "#0d1117", rx=2.5, sw=1)
        if side == "right":
            self.text(px - 14, py + 3.5, name, size=9, fill=color, anchor="end")
        else:
            self.text(px + 14, py + 3.5, name, size=9, fill=color, anchor="start")
        self.pin_pts.append((px, py, name))
        return (px, py)

    def cpin_bottom(self, px, py, name, color):
        self.rect(px - 6, py - 6, 12, 12, color, "#0d1117", rx=2.5, sw=1)
        self.text(px, py + 18, name, size=8.5, fill=color, anchor="middle")
        self.pin_pts.append((px, py, name))
        return (px, py)

    # -------------------------------------------------------------- the board
    def pcb(self, x, y, w, h, title, sub, cam=False, chip="WROOM-1 N16R8"):
        self.boxes.append((x, y, x + w, y + h, title))
        self.rect(x, y, w, h, PCB_GREEN, PCB_STROKE, rx=9, sw=2.4)
        for hx, hy in ((x + 9, y + 9), (x + w - 9, y + 9), (x + 9, y + h - 9), (x + w - 9, y + h - 9)):
            self.parts.append(f'<circle cx="{hx}" cy="{hy}" r="3.1" fill="{BG}" stroke="{SILK}" stroke-width="1"/>')
        self.text(x + 12, y + 24, title, size=13, fill=SILK, weight="700", mono=False)
        self.text(x + 12, y + 40, sub, size=9.5, fill=SILK, mono=False)
        # antenna keepout (right, at shield height)
        self.rect(x + w - 26, y + 52, 16, 56, PCB_DARK, None, rx=3)
        # metal module shield
        shw = w - 74
        self.rect(x + 16, y + 52, shw, 56, SHIELD, SHIELD_STROKE, rx=5, sw=1.4)
        self.text(x + 16 + shw / 2, y + 76, "ESP32-S3", size=10.5, fill="#1f2328", anchor="middle", weight="700", mono=False)
        self.text(x + 16 + shw / 2, y + 92, chip, size=8, fill="#57606a", anchor="middle", mono=False)
        if cam:
            self.rect(x + 16, y + 120, 44, 13, GOLD, None, rx=3)
            self.text(x + 16, y + 148, "OV2640 · GPIO 4-18", size=8.5, fill=SILK)
        # USB-C, power LED
        self.rect(x + w / 2 - 11, y + h - 8, 22, 8, SILVER, None, rx=2)
        self.parts.append(f'<circle cx="{x + 12}" cy="{y + h - 12}" r="3" fill="{GREEN}"/>')

    # ---------------------------------------------------------------- output
    def render(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{self.esc(self.title)}">\n'
            f'<rect width="{self.w}" height="{self.h}" fill="{BG}"/>\n'
            + "\n".join(self.parts) + "\n</svg>\n"
        )

    # ---------------------------------------------------------------- checks
    def check_labels(self):
        bad = []
        for x0, y0, x1, y1, s in self.labels:
            if x0 < 4 or y0 < 4 or x1 > self.w - 4 or y1 > self.h - 4:
                bad.append(f"Label ausserhalb: {s!r}")
        for i in range(len(self.labels)):
            for j in range(i + 1, len(self.labels)):
                a, b = self.labels[i], self.labels[j]
                if a[0] < b[2] - 2 and b[0] < a[2] - 2 and a[1] < b[3] - 1 and b[1] < a[3] - 1:
                    bad.append(f"Label-Ueberlappung: {a[4]!r} / {b[4]!r}")
        return bad

    def check_wiring(self):
        bad = []
        pins = [(x, y) for x, y, _ in self.pin_pts]

        def ok_end(p):
            if any(abs(p[0] - q[0]) <= 9 and abs(p[1] - q[1]) <= 9 for q in pins):
                return True
            if any(abs(p[1] - y) <= 3 for y in self.bus_ys):
                return True
            for x, y0, y1 in self.rails:
                if abs(p[0] - x) <= 4 and y0 - 4 <= p[1] <= y1 + 4:
                    return True
            if any(abs(p[0] - nx) <= 6 and abs(p[1] - ny) <= 6 for nx, ny in self.nodes):
                return True
            if any(x0 - 4 <= p[0] <= x1 + 4 and abs(p[1] - y) <= 4 for x0, x1, y in self.hbus):
                return True
            for bx0, by0, bx1, by1, _ in self.boxes:
                if (abs(p[0] - bx0) <= 5 or abs(p[0] - bx1) <= 5) and by0 - 5 <= p[1] <= by1 + 5:
                    return True
            return False

        for pts, color in self.wires:
            for end in (pts[0], pts[-1]):
                if not ok_end(end):
                    bad.append(f"Kabelende ohne Pin/Schiene: ({end[0]:.0f},{end[1]:.0f}) {color}")
            for i in range(len(pts) - 1):
                (x1, y1), (x2, y2) = pts[i], pts[i + 1]
                steps = int(max(abs(x2 - x1), abs(y2 - y1)) / 3) + 1
                for k in range(steps + 1):
                    x = x1 + (x2 - x1) * k / steps
                    y = y1 + (y2 - y1) * k / steps
                    if any(abs(x - p[0]) < 14 and abs(y - p[1]) < 14 for p in (pts[0], pts[-1])):
                        continue
                    for bx0, by0, bx1, by1, name in self.boxes:
                        if bx0 + 5 < x < bx1 - 5 and by0 + 5 < y < by1 - 5:
                            bad.append(f"Kabel laeuft durch {name!r} bei ({x:.0f},{y:.0f}) {color}")
        return bad


def header(svg, title, sub):
    svg.text(30, 42, title, size=20, fill=W_WHITE, weight="600", mono=False)
    svg.text(30, 66, sub, size=11.5, fill=MUTED, mono=False)


def footer(svg, txt):
    svg.text(30, svg.h - 14, txt, size=10.5, fill=DIM, mono=False)


def legend(svg, x, y, items, size=10.5, gap=22):
    for i, (color, txt) in enumerate(items):
        yy = y + i * gap
        svg.parts.append(
            f'<path d="M {x},{yy-4} L {x+24},{yy-4}" stroke="{color}" stroke-width="3.6" '
            f'stroke-linecap="round"/>'
        )
        svg.text(x + 32, yy, txt, size=size, fill=MUTED, mono=False)


# ---------------------------------------------------------------------------
def diagram_power():
    s = Svg(1120, 600, "5-V-Stromverteilung")
    header(s, "Stromverteilung 5 V",
           "Eine Powerbank, eine 5-V-Schiene, ein GND-Sternpunkt. Motorstrom läuft nie über das Board.")

    s.box(40, 110, 230, 96, "Powerbank", "5 V / ≥ 2,4 A · USB-A")
    s.rail(330, 110, 500, RED, "")
    s.rail(300, 130, 520, GREY, "")
    s.wire([(270, 150), (330, 150)], RED, 6, dots=False)
    s.wire([(270, 182), (330, 182), (300, 182)], GREY, 6, dots=False)
    s.label(350, 104, "5 V", size=10.5, fill=RED, anchor="start")
    s.label(282, 124, "GND", size=10.5, fill=GREY, anchor="end")

    s.node(420, 214)
    s.node(420, 238)
    s.wire([(330, 200), (420, 200), (420, 214)], PURPLE, 3, dots=False)
    s.rect(398, 216, 44, 6, PURPLE, rx=2)
    s.rect(398, 232, 44, 6, PURPLE, rx=2)
    s.wire([(420, 238), (420, 262), (300, 262)], GREY, 3, dots=False)
    s.label(466, 224, "1000 uF + 100 nF", size=10, fill=PURPLE, anchor="start")

    for name, note, y in [("ESP32-S3-CAM", "5V-Pin · ~250 mA mit Stream", 150),
                          ("ULN2003", "+5V · 28BYJ-48, 240 mA", 260),
                          ("DRV8833", "VM · TT-Motor, 1 A Spitze", 370),
                          ("PCA9685", "V+ · Servo-Rail, 2 x 700 mA Spitze", 480)]:
        s.box(560, y - 34, 400, 68, name, note)
        s.wire([(330, y), (560, y)], RED, 4)
        s.wire([(300, y + 18), (560, y + 18)], GREY, 3.4, dots=False)
        s.parts.append(f'<circle cx="300" cy="{y+18}" r="3.6" fill="{GREY}"/>')

    s.text(560, 566, "Summe typisch 700-800 mA · Spitze ~2,5 A", size=12, fill=ORANGE, mono=False)
    legend(s, 40, 470, [(RED, "5 V"), (GREY, "GND-Sternpunkt"), (PURPLE, "Puffer-Elko")])
    footer(s, "Board nur über seinen 5V-Pin versorgen - Motoren und Servos hängen an der Schiene.")
    return s


# ---------------------------------------------------------------------------
def diagram_motors():
    s = Svg(1200, 960, "Motorverkabelung (Kamera-Variante)")
    header(s, "Motoren: Schrittmotor, TT-Motor, zwei Servos",
           "Pin für Pin vom ESP32-S3-CAM. Stromschienen rechts, Signale links.")

    bx, by, bw, bh = 60, 110, 270, 430
    s.pcb(bx, by, bw, bh, "ESP32-S3-CAM", "N16R8 · Kamera GPIO 4-18", cam=True)

    esp = {}
    for name, color, yy in [("GPIO1", ORANGE, 150), ("GPIO2", ORANGE, 180), ("GPIO3", ORANGE, 210),
                            ("GPIO14", ORANGE, 240), ("GPIO21", ORANGE, 270), ("GPIO41", ORANGE, 300),
                            ("GPIO43", BLUE, 340), ("GPIO44", BLUE, 370)]:
        esp[name] = s.cpin(bx + bw, by + yy, name, color, side="right")
    esp["5V"] = s.cpin_bottom(bx + 70, by + bh, "5V", RED)
    esp["GND"] = s.cpin_bottom(bx + 130, by + bh, "GND", GREY)

    ux, uy = 430, 110
    s.box(ux, uy, 340, 230, "ULN2003", "Treiberplatine 28BYJ-48 · 5 V")
    ul = s.pins(ux, uy, 340, ["IN1", "IN2", "IN3", "IN4"], side="left", step=30, top=100)
    s.rect(ux + 150, uy + 62, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(ux + 225, uy + 82, "28BYJ-48", size=10, fill=W_WHITE, anchor="middle")
    s.text(ux + 225, uy + 98, "~15 rpm · 0,34 kg·cm", size=8.5, fill=DIM, anchor="middle")
    ur = s.pins(ux, uy, 340, ["+5V", "GND"], side="right", step=40, top=64)

    dx, dy = 430, 380
    s.box(dx, dy, 340, 180, "DRV8833", "2 Kanäle · 1,5 A · Kanal B frei")
    dr = s.pins(dx, dy, 340, ["AIN1", "AIN2"], side="left", step=30, top=74)
    s.rect(dx + 150, dy + 62, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(dx + 225, dy + 82, "TT-Motor", size=10, fill=W_WHITE, anchor="middle")
    s.text(dx + 225, dy + 98, "3-6 V · 1:90", size=8.5, fill=DIM, anchor="middle")
    drg = s.pins(dx, dy, 340, ["VM", "GND"], side="right", step=40, top=64)

    px, py = 430, 600
    s.box(px, py, 340, 250, "PCA9685", "16 Kanäle · I2C 0x40")
    pp = s.pins(px, py, 340, ["SDA", "SCL"], side="left", step=30, top=84)
    s.rect(px + 56, py + 148, 124, 32, PIN, PIN_STROKE, rx=4)
    s.text(px + 118, py + 168, "SG90 180 (CH0)", size=8.5, fill=W_WHITE, anchor="middle")
    s.rect(px + 56, py + 190, 124, 32, PIN, PIN_STROKE, rx=4)
    s.text(px + 118, py + 210, "SG90 360 (CH1)", size=8.5, fill=W_WHITE, anchor="middle")
    s.path(f"M {px+46},{py+154} L {px+56},{py+154}", GREEN, 3)
    s.path(f"M {px+46},{py+196} L {px+56},{py+196}", GREEN, 3)
    s.text(px + 196, py + 170, "Plus an V+ (5-V-Schiene)", size=8.5, fill=DIM)
    s.text(px + 196, py + 188, "PWM 50 Hz", size=8.5, fill=DIM)
    pq = s.pins(px, py, 340, ["V+", "GND"], side="right", step=40, top=64)

    for i, g in enumerate(["GPIO1", "GPIO2", "GPIO3", "GPIO14"]):
        tx = 352 + i * 10
        s.wire([esp[g], (tx, esp[g][1]), (tx, ul[f"IN{i+1}"][1]), ul[f"IN{i+1}"]], ORANGE, 3)
    s.label(352, 196, "IN1-IN4", size=9.5, fill=ORANGE, plate=True)

    s.wire([esp["GPIO21"], (400, esp["GPIO21"][1]), (400, dr["AIN1"][1]), dr["AIN1"]], ORANGE, 3)
    s.wire([esp["GPIO41"], (412, esp["GPIO41"][1]), (412, dr["AIN2"][1]), dr["AIN2"]], ORANGE, 3)
    s.label(398, 366, "AIN1 / AIN2", size=9.5, fill=ORANGE, plate=True)

    s.wire([esp["GPIO43"], (418, esp["GPIO43"][1]), (418, pp["SDA"][1]), pp["SDA"]], BLUE, 3)
    s.wire([esp["GPIO44"], (424, esp["GPIO44"][1]), (424, pp["SCL"][1]), pp["SCL"]], BLUE, 3)
    s.label(418, 556, "I2C 43/44", size=9.5, fill=BLUE, plate=True)

    s.rail(830, 80, 880, RED, "5 V")
    s.rail(884, 96, 915, GREY, "GND")
    for pos in (ur["+5V"], drg["VM"], pq["V+"]):
        s.wire([pos, (830, pos[1])], RED, 3.4)
    for pos in (ur["GND"], drg["GND"], pq["GND"]):
        s.wire([pos, (884, pos[1])], GREY, 3)
    s.wire([esp["5V"], (200, 540), (200, 880), (830, 880)], RED, 4)
    s.wire([esp["GND"], (270, 540), (270, 915), (884, 915)], GREY, 4)

    legend(s, 920, 180, [(ORANGE, "Motor-Signal"), (BLUE, "I2C"), (RED, "5 V"),
                         (GREEN, "Servo-PWM"), (GREY, "GND")])
    s.text(920, 340, "Hinweise", size=12.5, fill=W_WHITE, weight="600", mono=False)
    for i, t in enumerate([
        "· GPIO 43/44 als I2C nur, wenn die",
        "  Konsole über USB-CDC läuft (Standard).",
        "· Servos hängen an PCA9685 V+,",
        "  nicht am Board.",
        "· ULN2003 an 3,3 V: Schrittrate",
        "  moderat halten (~600 Hz).",
        "· Kreuzung ohne Punkt = keine",
        "  Verbindung.",
    ]):
        s.text(920, 366 + i * 20, t, size=9.5, fill=MUTED, mono=False)

    footer(s, "Alle Treiber-Massen auf den GND-Sternpunkt. Logikpegel durchgehend 3,3 V.")
    return s


# ---------------------------------------------------------------------------
def diagram_sensors():
    s = Svg(1400, 740, "Sensorverkabelung (Kamera-Variante)")
    header(s, "Sensoren: Abstand, Lichtschranke, Endschalter",
           "Zwei Teilbilder: HC-SR04 direkt am ESP32 (mit Teiler) · Schalter am PCF8574 über I2C.")
    s.path("M 686,96 L 686,700", STROKE, 1.5, dash="6 6")

    # ---- Teilbild A ------------------------------------------------------
    s.text(40, 108, "A · Abstand (HC-SR04)", size=11.5, fill=MUTED, mono=False)
    s.pcb(40, 130, 240, 300, "ESP32-S3-CAM", "N16R8", cam=True)
    ea = {}
    ea["GPIO42"] = s.cpin(280, 226, "GPIO42", ORANGE, side="right")
    ea["GPIO47"] = s.cpin(280, 330, "GPIO47", ORANGE, side="right")
    ea["5V"] = s.cpin_bottom(100, 430, "5V", RED)
    ea["GND"] = s.cpin_bottom(160, 430, "GND", GREY)

    hx, hy = 430, 110
    s.box(hx, hy, 240, 220, "HC-SR04", "2-400 cm · 5 V")
    hp = s.pins(hx, hy, 240, ["TRIG", "ECHO"], side="left", step=40, top=90)
    s.rect(hx + 26, hy + 150, 54, 46, PIN, PIN_STROKE, rx=23)
    s.rect(hx + 96, hy + 150, 54, 46, PIN, PIN_STROKE, rx=23)
    s.text(hx + 53, hy + 178, "T", size=8.5, fill=DIM, anchor="middle")
    s.text(hx + 123, hy + 178, "R", size=8.5, fill=DIM, anchor="middle")
    hg = s.pins_bottom(hx, hy + 220, ["VCC", "GND"], start=60, step=60)

    s.wire([ea["GPIO42"], (330, ea["GPIO42"][1]), (330, hp["TRIG"][1]), hp["TRIG"]], ORANGE, 3)
    s.label(330, 206, "TRIG", size=9.5, fill=ORANGE, plate=True)

    ny = hp["ECHO"][1]
    s.resistor(344, ny, length=42)
    s.label(365, ny - 16, "1 kOhm", size=9.5, fill=PURPLE)
    s.wire([hp["ECHO"], (386, ny)], PURPLE, 3, dots=False)
    s.node(386, ny)
    s.node(344, ny)
    s.node(352, ny)
    s.node(352, ny + 38)
    s.wire([(344, ny), (344, ea["GPIO47"][1]), ea["GPIO47"]], ORANGE, 3)
    s.wire([(344, ny), (352, ny)], PURPLE, 3, dots=False)
    s.resistor(352, ny, length=38, vertical=True)
    s.label(374, ny + 24, "2 kOhm", size=9.5, fill=PURPLE, anchor="start")
    s.wire([(352, ny + 38), (352, 600)], GREY, 2.6)
    s.label(360, ny + 56, "nach GND", size=9.5, fill=GREY, anchor="start")

    s.wire([ea["5V"], (100, 540), (490, 540), (490, hy + 220)], RED, 3.4)
    s.label(104, 534, "5 V", size=9.5, fill=RED, anchor="start", plate=True)
    s.wire([ea["GND"], (160, 600)], GREY, 2.8)
    s.wire([hg["GND"], (550, hy + 220), (550, 600)], GREY, 2.8)
    s.busline(600, 100, 560, GREY, 3)
    s.label(300, 614, "GND", size=9, fill=GREY)

    legend(s, 40, 650, [(ORANGE, "Digitalsignal"), (PURPLE, "Teiler 1k/2k"),
                        (RED, "5 V"), (GREY, "GND")], size=9.5, gap=19)

    # ---- Teilbild B ------------------------------------------------------
    s.text(716, 108, "B · Schalter & Lichtschranke", size=11.5, fill=MUTED, mono=False)
    s.pcb(716, 130, 220, 300, "ESP32-S3-CAM", "gleiches Board", cam=True)
    eb = {}
    eb["GPIO43"] = s.cpin(936, 226, "GPIO43", BLUE, side="right")
    eb["GPIO44"] = s.cpin(936, 330, "GPIO44", BLUE, side="right")
    eb["3V3"] = s.cpin_bottom(776, 430, "3V3", GREEN)
    eb["GND"] = s.cpin_bottom(836, 430, "GND", GREY)

    qx, qy = 1010, 110
    s.box(qx, qy, 230, 320, "PCF8574", "8 Eingänge · I2C 0x20")
    qp = s.pins(qx, qy, 230, ["SDA", "SCL", "VCC"], side="left", step=40, top=90)
    qr = s.pins(qx, qy, 230, ["P0", "P1", "P2", "P3", "P4"], side="right", step=30, top=70)
    qg = s.pins_bottom(qx, qy + 320, ["GND"], start=60, step=60)

    s.wire([eb["GPIO43"], (966, eb["GPIO43"][1]), (966, qp["SDA"][1]), qp["SDA"]], BLUE, 3)
    s.wire([eb["GPIO44"], (978, eb["GPIO44"][1]), (978, qp["SCL"][1]), qp["SCL"]], BLUE, 3)
    s.label(966, 300, "I2C", size=9.5, fill=BLUE, plate=True)
    s.wire([eb["3V3"], (760, 480), (940, 480), (940, qp["VCC"][1]), qp["VCC"]], GREEN, 3)
    s.label(764, 474, "3,3 V", size=9.5, fill=GREEN, anchor="start", plate=True)

    for i in range(4):
        yy = qy + 70 + i * 30
        s.rect(1260, yy - 11, 76, 22, PIN, PIN_STROKE, rx=4)
        s.text(1298, yy + 4, f"SW{i+1}", size=9, fill=MUTED, anchor="middle")
        s.node(1260, yy)
        s.wire([qr[f"P{i}"], (1260, yy)], ORANGE, 2.6, dots=False)
    yy = qy + 70 + 4 * 30
    s.rect(1260, yy - 11, 76, 22, PIN, PIN_STROKE, rx=4)
    s.text(1298, yy + 4, "KY-010", size=9, fill=MUTED, anchor="middle")
    s.node(1260, yy)
    s.wire([qr["P4"], (1260, yy)], ORANGE, 2.6, dots=False)

    s.wire([eb["GND"], (820, 600)], GREY, 2.8)
    s.wire([qg["GND"], (1070, qy + 320), (1070, 600)], GREY, 2.8)
    s.busline(600, 820, 1080, GREY, 3)
    s.label(960, 614, "GND", size=9, fill=GREY)

    legend(s, 716, 650, [(ORANGE, "Schaltersignal"), (BLUE, "I2C"),
                         (GREEN, "3,3 V"), (GREY, "GND")], size=9.5, gap=19)

    footer(s, "Sensorkabel < 30 cm halten. Endschalter gegen GND, Pull-up sitzt im PCF8574 - keine extra Widerstände.")
    return s


# ---------------------------------------------------------------------------
def diagram_no_cam_motors():
    s = Svg(1200, 960, "Motorverkabelung (ohne Kamera)")
    header(s, "Motoren ohne Kamera: ESP32-S3-DevKitC-1",
           "Alle Pins direkt am Board - kein I2C-Expander nötig, Servos direkt über LEDC-PWM.")

    bx, by, bw, bh = 40, 110, 250, 640
    s.pcb(bx, by, bw, bh, "ESP32-S3-DevKitC-1", "WROOM-1 N8R2 · keine Kamera", cam=False, chip="WROOM-1 N8R2")

    esp = {}
    for name, color, yy in [("GPIO4", ORANGE, 100), ("GPIO5", ORANGE, 130), ("GPIO6", ORANGE, 160),
                            ("GPIO7", ORANGE, 190), ("GPIO8", ORANGE, 320), ("GPIO9", ORANGE, 350),
                            ("GPIO12", TEAL, 564), ("GPIO13", TEAL, 604)]:
        esp[name] = s.cpin(bx + bw, by + yy, name, color, side="right")
    esp["5V"] = s.cpin_bottom(bx + 70, by + bh, "5V", RED)
    esp["GND"] = s.cpin_bottom(bx + 130, by + bh, "GND", GREY)

    ux, uy = 430, 110
    s.box(ux, uy, 340, 230, "ULN2003", "Treiberplatine 28BYJ-48 · 5 V")
    ul = s.pins(ux, uy, 340, ["IN1", "IN2", "IN3", "IN4"], side="left", step=30, top=100)
    s.rect(ux + 150, uy + 62, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(ux + 225, uy + 82, "28BYJ-48", size=10, fill=W_WHITE, anchor="middle")
    s.text(ux + 225, uy + 98, "~15 rpm", size=8.5, fill=DIM, anchor="middle")
    ur = s.pins(ux, uy, 340, ["+5V", "GND"], side="right", step=40, top=64)

    dx, dy = 430, 380
    s.box(dx, dy, 340, 180, "DRV8833", "2 Kanäle · 1,5 A · Kanal B frei")
    dr = s.pins(dx, dy, 340, ["AIN1", "AIN2"], side="left", step=30, top=50)
    s.rect(dx + 150, dy + 62, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(dx + 225, dy + 82, "TT-Motor", size=10, fill=W_WHITE, anchor="middle")
    s.text(dx + 225, dy + 98, "3-6 V · 1:90", size=8.5, fill=DIM, anchor="middle")
    drg = s.pins(dx, dy, 340, ["VM", "GND"], side="right", step=40, top=64)

    sx, sy = 430, 600
    s.box(sx, sy, 340, 250, "SG90 (direkt)", "PWM über LEDC · kein Treiber nötig")
    sg = s.pins(sx, sy, 340, ["SIG1", "SIG2"], side="left", step=40, top=74)
    s.rect(sx + 150, sy + 100, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(sx + 225, sy + 120, "SG90 180° · GPIO12", size=8.5, fill=W_WHITE, anchor="middle")
    s.rect(sx + 150, sy + 160, 150, 46, PIN, PIN_STROKE, rx=5)
    s.text(sx + 225, sy + 180, "SG90 360° · GPIO13", size=8.5, fill=W_WHITE, anchor="middle")
    sgp = s.pins(sx, sy, 340, ["V+", "GND"], side="right", step=40, top=64)

    for i, g in enumerate(["GPIO4", "GPIO5", "GPIO6", "GPIO7"]):
        s.wire([esp[g], ul[f"IN{i+1}"]], ORANGE, 3)
    s.label(352, 196, "IN1-IN4", size=9.5, fill=ORANGE, plate=True)
    s.wire([esp["GPIO8"], dr["AIN1"]], ORANGE, 3)
    s.wire([esp["GPIO9"], dr["AIN2"]], ORANGE, 3)
    s.label(398, 366, "AIN1 / AIN2", size=9.5, fill=ORANGE, plate=True)
    s.wire([esp["GPIO12"], sg["SIG1"]], TEAL, 3)
    s.wire([esp["GPIO13"], sg["SIG2"]], TEAL, 3)
    s.label(398, 556, "Servo-PWM", size=9.5, fill=TEAL, plate=True)

    s.rail(830, 80, 880, RED, "5 V")
    s.rail(884, 96, 915, GREY, "GND")
    for pos in (ur["+5V"], drg["VM"], sgp["V+"]):
        s.wire([pos, (830, pos[1])], RED, 3.4)
    for pos in (ur["GND"], drg["GND"], sgp["GND"]):
        s.wire([pos, (884, pos[1])], GREY, 3)
    s.wire([esp["5V"], (110, 880), (830, 880)], RED, 4)
    s.wire([esp["GND"], (170, 915), (884, 915)], GREY, 4)

    legend(s, 920, 180, [(ORANGE, "Motor-Signal"), (TEAL, "Servo-PWM (LEDC)"),
                         (RED, "5 V"), (GREY, "GND")])
    s.text(920, 340, "Hinweise", size=12.5, fill=W_WHITE, weight="600", mono=False)
    for i, t in enumerate([
        "· Kein Expander, kein Servo-Board:",
        "  Servos direkt an GPIO12/13 (LEDC,",
        "  50 Hz, 0-180°).",
        "· 14 Pins bleiben frei (GPIO 21,",
        "  35-42, 47, 48 ...).",
        "· ULN2003 an 3,3 V: Schrittrate",
        "  moderat halten (~600 Hz).",
        "· Kreuzung ohne Punkt = keine",
        "  Verbindung.",
    ]):
        s.text(920, 366 + i * 20, t, size=9.5, fill=MUTED, mono=False)

    footer(s, "Servos an die 5-V-Schiene (V+), nicht an den 3,3-V-Pin des Boards.")
    return s


# ---------------------------------------------------------------------------
def diagram_no_cam_sensors():
    s = Svg(1400, 740, "Sensorverkabelung (ohne Kamera)")
    header(s, "Sensoren ohne Kamera: alles direkt am ESP32-S3-DevKitC-1",
           "Kein PCF8574 nötig - Endschalter und Lichtschranke direkt an GPIO, mit internen Pull-ups.")
    s.path("M 686,96 L 686,700", STROKE, 1.5, dash="6 6")

    # ---- Teilbild A ------------------------------------------------------
    s.text(40, 108, "A · Abstand (HC-SR04)", size=11.5, fill=MUTED, mono=False)
    s.pcb(40, 130, 250, 300, "ESP32-S3-DevKitC-1", "WROOM-1 N8R2", cam=False, chip="WROOM-1 N8R2")
    ea = {}
    ea["GPIO10"] = s.cpin(290, 226, "GPIO10", ORANGE, side="right")
    ea["GPIO11"] = s.cpin(290, 330, "GPIO11", ORANGE, side="right")
    ea["5V"] = s.cpin_bottom(110, 430, "5V", RED)
    ea["GND"] = s.cpin_bottom(170, 430, "GND", GREY)

    hx, hy = 430, 110
    s.box(hx, hy, 240, 220, "HC-SR04", "2-400 cm · 5 V")
    hp = s.pins(hx, hy, 240, ["TRIG", "ECHO"], side="left", step=40, top=90)
    s.rect(hx + 26, hy + 150, 54, 46, PIN, PIN_STROKE, rx=23)
    s.rect(hx + 96, hy + 150, 54, 46, PIN, PIN_STROKE, rx=23)
    s.text(hx + 53, hy + 178, "T", size=8.5, fill=DIM, anchor="middle")
    s.text(hx + 123, hy + 178, "R", size=8.5, fill=DIM, anchor="middle")
    hg = s.pins_bottom(hx, hy + 220, ["VCC", "GND"], start=60, step=60)

    s.wire([ea["GPIO10"], (340, ea["GPIO10"][1]), (340, hp["TRIG"][1]), hp["TRIG"]], ORANGE, 3)
    s.label(340, 206, "TRIG", size=9.5, fill=ORANGE, plate=True)

    ny = hp["ECHO"][1]
    s.resistor(344, ny, length=42)
    s.label(365, ny - 16, "1 kOhm", size=9.5, fill=PURPLE)
    s.wire([hp["ECHO"], (386, ny)], PURPLE, 3, dots=False)
    s.node(386, ny)
    s.node(344, ny)
    s.node(352, ny)
    s.node(352, ny + 38)
    s.wire([(344, ny), (344, ea["GPIO11"][1]), ea["GPIO11"]], ORANGE, 3)
    s.wire([(344, ny), (352, ny)], PURPLE, 3, dots=False)
    s.resistor(352, ny, length=38, vertical=True)
    s.label(374, ny + 24, "2 kOhm", size=9.5, fill=PURPLE, anchor="start")
    s.wire([(352, ny + 38), (352, 600)], GREY, 2.6)
    s.label(360, ny + 56, "nach GND", size=9.5, fill=GREY, anchor="start")

    s.wire([ea["5V"], (110, 540), (490, 540), (490, hy + 220)], RED, 3.4)
    s.label(114, 534, "5 V", size=9.5, fill=RED, anchor="start", plate=True)
    s.wire([ea["GND"], (170, 600)], GREY, 2.8)
    s.wire([hg["GND"], (550, hy + 220), (550, 600)], GREY, 2.8)
    s.busline(600, 110, 560, GREY, 3)
    s.label(310, 614, "GND", size=9, fill=GREY)

    legend(s, 40, 650, [(ORANGE, "Digitalsignal"), (PURPLE, "Teiler 1k/2k"),
                        (RED, "5 V"), (GREY, "GND")], size=9.5, gap=19)

    # ---- Teilbild B ------------------------------------------------------
    s.text(716, 108, "B · Schalter & Lichtschranke (direkt)", size=11.5, fill=MUTED, mono=False)
    s.pcb(716, 130, 250, 300, "ESP32-S3-DevKitC-1", "WROOM-1 N8R2", cam=False, chip="WROOM-1 N8R2")
    eb = {}
    for i, name in enumerate(["GPIO14", "GPIO15", "GPIO16", "GPIO17"]):
        eb[name] = s.cpin(966, 226 + i * 30, name, ORANGE, side="right")
    eb["GPIO18"] = s.cpin(966, 346, "GPIO18", ORANGE, side="right")
    eb["3V3"] = s.cpin_bottom(776, 430, "3V3", GREEN)
    eb["GND"] = s.cpin_bottom(836, 430, "GND", GREY)

    for i in range(4):
        yy = 226 + i * 30
        s.rect(1010, yy - 11, 76, 22, PIN, PIN_STROKE, rx=4)
        s.text(1048, yy + 4, f"SW{i+1}", size=9, fill=MUTED, anchor="middle")
        s.node(1010, yy)
        s.wire([eb[f"GPIO{14+i}"], (1010, yy)], ORANGE, 2.6, dots=False)
    yy = 346
    s.rect(1010, yy - 11, 76, 22, PIN, PIN_STROKE, rx=4)
    s.text(1048, yy + 4, "KY-010", size=9, fill=MUTED, anchor="middle")
    s.node(1010, yy)
    s.wire([eb["GPIO18"], (1010, yy)], ORANGE, 2.6, dots=False)

    s.wire([eb["GND"], (850, 600)], GREY, 2.8)
    for i in range(4):
        yy = 226 + i * 30
        s.node(1086, yy)
        s.node(1100, yy)
        s.wire([(1086, yy), (1100, yy)], GREY, 2.2)
    s.node(1086, 346)
    s.node(1100, 346)
    s.wire([(1086, 346), (1100, 346)], GREY, 2.2)
    s.wire([(1100, 226), (1100, 600)], GREY, 2.2)
    s.busline(600, 850, 1100, GREY, 3)
    s.label(960, 614, "GND", size=9, fill=GREY)
    s.text(1010, 400, "Schalter gegen GND (Pull-up intern im Board)", size=9, fill=MUTED, mono=False)
    s.text(1010, 416, "KY-010: VCC an 3,3 V · DO an GPIO18", size=9, fill=MUTED, mono=False)

    legend(s, 716, 650, [(ORANGE, "Schaltersignal"), (GREEN, "3,3 V"), (GREY, "GND")], size=9.5, gap=19)

    footer(s, "Interne Pull-ups aktivieren (INPUT_PULLUP). KY-010 VCC an 3,3 V, GND an GND.")
    return s


# ---------------------------------------------------------------------------
def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "wiring")
    os.makedirs(out, exist_ok=True)
    import xml.etree.ElementTree as ET

    total = 0
    for name, fn in (("strom.svg", diagram_power),
                     ("motoren.svg", diagram_motors),
                     ("sensoren.svg", diagram_sensors),
                     ("motoren_ohne_kamera.svg", diagram_no_cam_motors),
                     ("sensoren_ohne_kamera.svg", diagram_no_cam_sensors)):
        svg = fn()
        problems = svg.check_labels() + svg.check_wiring()
        path = os.path.join(out, name)
        with open(path, "w") as f:
            f.write(svg.render())
        ET.parse(path)
        print(f"{name}: {len(svg.parts)} Elemente · {len(svg.labels)} Labels · "
              f"{os.path.getsize(path)} B · XML ok · {len(problems)} Befunde")
        for p in problems[:10]:
            print("   !!", p)
        total += len(problems)
    print("SAUBER" if total == 0 else f"{total} Befunde offen")


if __name__ == "__main__":
    main()
