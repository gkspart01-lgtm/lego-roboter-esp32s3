"""Rasterize our own SVG subset to PNG so the diagram can be inspected.

The host has no rsvg/inkscape/chromium, so this reads the emitted elements
(rect, path with M/L/Q, circle, text) and paints them into an RGB buffer.
Text is drawn as its bounding box (plus baseline) — enough to judge layout.
"""

import math
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zlib

NS = "{http://www.w3.org/2000/svg}"


def _png(path, w, h, buf):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += buf[y * w * 3:(y + 1) * w * 3]

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(
            ">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 6)))
        f.write(chunk(b"IEND", b""))


def parse_color(c, default=None):
    if not c or c == "none":
        return default
    if c.startswith("#"):
        c = c[1:]
        if len(c) == 3:
            c = "".join(ch * 2 for ch in c)
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return default


class Canvas:
    def __init__(self, w, h, scale=0.75, bg=(13, 17, 23)):
        self.w, self.h, self.s = int(w * scale), int(h * scale), scale
        self.buf = bytearray(bytes(bg) * (self.w * self.h))

    def px(self, x, y, col, a=1.0):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            if a >= 1.0:
                self.buf[o:o + 3] = bytes(col)
            else:
                for i in range(3):
                    self.buf[o + i] = int(self.buf[o + i] * (1 - a) + col[i] * a)

    def rect(self, x, y, w, h, fill, stroke=None, sw=1.0, rx=0):
        x0, y0 = int(x * self.s), int(y * self.s)
        x1, y1 = int((x + w) * self.s), int((y + h) * self.s)
        for yy in range(max(0, y0), min(self.h, y1 + 1)):
            for xx in range(max(0, x0), min(self.w, x1 + 1)):
                if fill:
                    self.px(xx, yy, fill)
        if stroke:
            t = max(1, int(sw * self.s))
            for xx in range(max(0, x0), min(self.w, x1 + 1)):
                for d in range(t):
                    self.px(xx, min(self.h - 1, y0 + d), stroke)
                    self.px(xx, max(0, y1 - d), stroke)
            for yy in range(max(0, y0), min(self.h, y1 + 1)):
                for d in range(t):
                    self.px(min(self.w - 1, x0 + d), yy, stroke)
                    self.px(max(0, x1 - d), yy, stroke)

    def disc(self, cx, cy, r, col):
        cx, cy, r = cx * self.s, cy * self.s, r * self.s
        for yy in range(int(cy - r), int(cy + r) + 1):
            for xx in range(int(cx - r), int(cx + r) + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.px(xx, yy, col)

    def stroke(self, pts, col, width=3.0):
        t = max(1, int(width * self.s))
        for i in range(len(pts) - 1):
            x1, y1 = pts[i][0] * self.s, pts[i][1] * self.s
            x2, y2 = pts[i + 1][0] * self.s, pts[i + 1][1] * self.s
            n = int(max(abs(x2 - x1), abs(y2 - y1))) + 1
            for k in range(n + 1):
                x = x1 + (x2 - x1) * k / n
                y = y1 + (y2 - y1) * k / n
                for dy in range(-t // 2, t // 2 + 1):
                    for dx in range(-t // 2, t // 2 + 1):
                        self.px(int(x) + dx, int(y) + dy, col)


def path_points(d):
    """Flatten M/L/Q path data into a polyline."""
    toks = re.findall(r"[MLQ]|-?\d+\.?\d*", d)
    pts, cur, i = [], None, 0
    while i < len(toks):
        if toks[i] == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            pts.append(cur)
            i += 3
        elif toks[i] == "L":
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            pts.append(cur)
            i += 3
        elif toks[i] == "Q":
            c = (float(toks[i + 1]), float(toks[i + 2]))
            e = (float(toks[i + 3]), float(toks[i + 4]))
            for k in range(1, 7):
                t = k / 6.0
                x = (1 - t) ** 2 * cur[0] + 2 * (1 - t) * t * c[0] + t * t * e[0]
                y = (1 - t) ** 2 * cur[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]
                pts.append((x, y))
            cur = e
            i += 5
        else:
            i += 1
    return pts


TEXT_RECT = (34, 34, 42)      # dark grey text footprint
TEXT_LINE = (58, 58, 68)


def rasterize(svg_path, png_path, scale=0.75):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    w = float(root.get("width"))
    h = float(root.get("height"))
    cv = Canvas(w, h, scale)
    for el in root:
        tag = el.tag.replace(NS, "")
        if tag == "rect":
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            ww, hh = float(el.get("width")), float(el.get("height"))
            cv.rect(x, y, ww, hh, parse_color(el.get("fill")),
                    parse_color(el.get("stroke")), float(el.get("stroke-width", 1)), 0)
        elif tag == "circle":
            cv.disc(float(el.get("cx")), float(el.get("cy")), float(el.get("r")),
                    parse_color(el.get("fill")))
        elif tag == "path":
            cv.stroke(path_points(el.get("d")), parse_color(el.get("stroke")),
                      float(el.get("stroke-width", 1)))
        elif tag == "text":
            x, y = float(el.get("x")), float(el.get("y"))
            size = float(el.get("font-size", 12))
            txt = "".join(el.itertext())
            width = len(txt) * size * 0.58
            anchor = el.get("text-anchor", "start")
            x0 = x - width / 2 if anchor == "middle" else (x - width if anchor == "end" else x)
            cv.rect(x0, y - size * 0.78, width, size * 0.95, TEXT_RECT, None, 0)
            cv.stroke([(x0, y + 1.5), (x0 + width, y + 1.5)], TEXT_LINE, 1.0)
    _png(png_path, cv.w, cv.h, cv.buf)
    return png_path, cv.w, cv.h


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + "_preview.png"
    p, w, h = rasterize(src, dst, float(sys.argv[3]) if len(sys.argv) > 3 else 0.75)
    print(f"{p}: {w}x{h}px, {os.path.getsize(p)} B")
