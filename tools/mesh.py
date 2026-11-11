"""Minimal pure-Python mesh toolkit: primitives, STL export, PNG render.

No numpy/PIL on this host, so everything is plain Python + zlib.
Units: millimetres, Z is up. Every primitive returns a CLOSED shell with
consistent outward winding, so slicers get a clean manifold per shell.
"""

import math
import struct
import zlib


# ------------------------------------------------------------------ helpers


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def _signed_volume(tris):
    v = 0.0
    for a, b, c in tris:
        v += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return v


def orient(tris):
    """Flip the whole shell if it is inside-out (negative signed volume)."""
    return [tuple(reversed(t)) for t in tris] if _signed_volume(tris) < 0 else tris


def _poly_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def _ear_clip(poly):
    """Triangulate a simple polygon (list of (x, y)) -> list of 3-index tuples."""
    idx = list(range(len(poly)))
    if _poly_area(poly) < 0:
        idx.reverse()
    out = []

    def is_ear(i0, i1, i2):
        a, b, c = poly[idx[i0]], poly[idx[i1]], poly[idx[i2]]
        area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if area <= 1e-12:
            return False
        for j in idx:
            if j in (idx[i0], idx[i1], idx[i2]):
                continue
            p = poly[j]
            d1 = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            d2 = (c[0] - b[0]) * (p[1] - b[1]) - (c[1] - b[1]) * (p[0] - b[0])
            d3 = (a[0] - c[0]) * (p[1] - c[1]) - (a[1] - c[1]) * (p[0] - c[0])
            if d1 >= 0 and d2 >= 0 and d3 >= 0:
                return False
        return True

    guard = 0
    while len(idx) > 3 and guard < 20000:
        guard += 1
        done = False
        for k in range(len(idx)):
            if is_ear(k, (k + 1) % len(idx), (k + 2) % len(idx)):
                out.append((idx[k], idx[(k + 1) % len(idx)], idx[(k + 2) % len(idx)]))
                idx.pop((k + 1) % len(idx))
                done = True
                break
        if not done:
            break
    if len(idx) == 3:
        out.append((idx[0], idx[1], idx[2]))
    return out


def extrude(poly, h, z0=0.0):
    """Extrude a simple 2D polygon (CCW) into a closed shell."""
    tris = []
    n = len(poly)
    tris_idx = _ear_clip(poly)
    for a, b, c in tris_idx:
        pa = (poly[a][0], poly[a][1], z0 + h)
        pb = (poly[b][0], poly[b][1], z0 + h)
        pc = (poly[c][0], poly[c][1], z0 + h)
        tris.append((pa, pb, pc))
        qa = (poly[a][0], poly[a][1], z0)
        qb = (poly[b][0], poly[b][1], z0)
        qc = (poly[c][0], poly[c][1], z0)
        tris.append((qa, qc, qb))
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        p1 = (x1, y1, z0)
        p2 = (x2, y2, z0)
        p3 = (x2, y2, z0 + h)
        p4 = (x1, y1, z0 + h)
        tris += [(p1, p2, p3), (p1, p3, p4)]
    return orient(tris)


def cylinder(r, h, segs=72, cx=0.0, cy=0.0, z0=0.0):
    poly = [
        (cx + r * math.cos(2 * math.pi * i / segs), cy + r * math.sin(2 * math.pi * i / segs))
        for i in range(segs)
    ]
    return extrude(poly, h, z0)


def box(w, d, h, cx=0.0, cy=0.0, z0=0.0):
    hw, hd = w / 2.0, d / 2.0
    poly = [(cx - hw, cy - hd), (cx + hw, cy - hd), (cx + hw, cy + hd), (cx - hw, cy + hd)]
    return extrude(poly, h, z0)


def c_ring(ri, ro, h, gap_deg=48.0, segs=64, z0=0.0):
    """Split clamp ring (C profile) — one closed shell, flexible gap."""
    a0 = math.radians(90.0 + gap_deg / 2.0)
    a1 = math.radians(90.0 + 360.0 - gap_deg / 2.0)
    n = segs
    outer = [(ro * math.cos(a0 + (a1 - a0) * i / n), ro * math.sin(a0 + (a1 - a0) * i / n))
             for i in range(n + 1)]
    inner = [(ri * math.cos(a1 - (a1 - a0) * i / n), ri * math.sin(a1 - (a1 - a0) * i / n))
             for i in range(n + 1)]
    return extrude(outer + inner, h, z0)


def rect_tube(outer, inner, h, cx=0.0, cy=0.0, z0=0.0, wall=None):
    """Square socket: 4 walls as separate closed boxes (slicer unions them)."""
    o = outer / 2.0
    i = inner / 2.0
    w = wall if wall is not None else (outer - inner) / 2.0
    shells = []
    # two walls along X (front/back), two along Y (left/right) - corners overlap
    shells.append(box(outer, w, h, cx=cx, cy=cy - o + w / 2.0, z0=z0))
    shells.append(box(outer, w, h, cx=cx, cy=cy + o - w / 2.0, z0=z0))
    shells.append(box(w, outer - 2 * w, h, cx=cx - o + w / 2.0, cy=cy, z0=z0))
    shells.append(box(w, outer - 2 * w, h, cx=cx + o - w / 2.0, cy=cy, z0=z0))
    return shells


def square_socket(ro, inner, h, z0=0.0, segs=10):
    """Round outside, square hole: 4 wedge shells (union by the slicer).

    Looks like a continuation of the clamp ring instead of a square tower,
    and keeps the wall thickness even all round.
    """
    i = inner / 2.0
    shells = []
    corner = {45: (i, i), 135: (-i, i), 225: (-i, -i), 315: (i, -i)}
    for k in range(4):
        a0 = -45.0 + 90.0 * k
        a1 = a0 + 90.0
        pts = []
        for j in range(segs + 1):
            a = math.radians(a0 + (a1 - a0) * j / segs)
            pts.append((ro * math.cos(a), ro * math.sin(a)))
        pts.append(corner[int(a1) % 360])
        pts.append(corner[int(a0) % 360])
        shells.append(extrude(pts, h, z0))
    return shells


# ------------------------------------------------------------------ shell ops


def translate(shells, dx=0.0, dy=0.0, dz=0.0):
    return [
        [tuple((v[0] + dx, v[1] + dy, v[2] + dz) for v in t) for t in s] for s in shells
    ]


def bbox(shells):
    vs = [v for s in shells for t in s for v in t]
    return (
        (min(v[0] for v in vs), min(v[1] for v in vs), min(v[2] for v in vs)),
        (max(v[0] for v in vs), max(v[1] for v in vs), max(v[2] for v in vs)),
    )


def volume(shells):
    return abs(sum(_signed_volume(s) for s in shells))


def open_edges(shells):
    """Edges not shared by exactly two triangles; 0 => each shell is closed."""
    from collections import Counter

    bad = 0
    for s in shells:
        cnt = Counter()
        for t in s:
            for i in range(3):
                a = tuple(round(c, 4) for c in t[i])
                b = tuple(round(c, 4) for c in t[(i + 1) % 3])
                cnt[(a, b) if a <= b else (b, a)] += 1
        bad += sum(1 for _, n in cnt.items() if n != 2)
    return bad


def flat(shells):
    return [t for s in shells for t in s]


# ------------------------------------------------------------------ STL export


def write_stl(shells, path, name="part"):
    tris = flat(shells)
    with open(path, "wb") as f:
        f.write(name.encode()[:80].ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            n = _cross(_sub(b, a), _sub(c, a))
            ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0
            n = (n[0] / ln, n[1] / ln, n[2] / ln)
            f.write(struct.pack("<3f", *n))
            for p in (a, b, c):
                f.write(struct.pack("<3f", *p))
            f.write(struct.pack("<H", 0))


# ------------------------------------------------------------------ PNG render


def _png(path, w, h, rgb):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rgb[y * w * 3 : (y + 1) * w * 3]

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def render(shells, path, w=900, h=700, azim=38.0, elev=24.0, bg=(13, 17, 23)):
    """Orthographic z-buffer render with flat shading and crease outlines."""
    tris = flat(shells)
    az, el = math.radians(azim), math.radians(elev)
    u = (math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el))
    right = (-math.sin(az), math.cos(az), 0.0)
    up = (-math.sin(el) * math.cos(az), -math.sin(el) * math.sin(az), math.cos(el))

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    P = []
    for t in tris:
        vs = [None, None, None]
        ns = [None, None, None]
        for i, v in enumerate(t):
            vs[i] = (dot(v, right), dot(v, up), dot(v, u))
        a, b, c = vs
        n = _cross(_sub(b, a), _sub(c, a))
        ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0
        P.append((a, b, c, (n[0] / ln, n[1] / ln, n[2] / ln)))

    xs = [p[0] for t in P for p in t[:3]]
    ys = [p[1] for t in P for p in t[:3]]
    span_x, span_y = max(xs) - min(xs), max(ys) - min(ys)
    scale = 0.82 * min(w / span_x, h / span_y)
    cx = (max(xs) + min(xs)) / 2.0
    cy = (max(ys) + min(ys)) / 2.0

    def to_px(p):
        return ((p[0] - cx) * scale + w / 2.0, h / 2.0 - (p[1] - cy) * scale, p[2])

    buf = bytearray(bg * (w * h))
    zbuf = [-1e18] * (w * h)
    light = (-0.45, 0.42, 0.79)
    for a, b, c, n in P:
        if n[2] <= 0.0:  # facing away from camera
            continue
        lam = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        shade = 0.26 + 0.74 * lam
        col = (
            min(255, int(92 * shade + 16)),
            min(255, int(156 * shade + 24)),
            min(255, int(212 * shade + 32)),
        )
        A, B, C = to_px(a), to_px(b), to_px(c)
        minx = max(0, int(min(A[0], B[0], C[0])))
        maxx = min(w - 1, int(max(A[0], B[0], C[0])) + 1)
        miny = max(0, int(min(A[1], B[1], C[1])))
        maxy = min(h - 1, int(max(A[1], B[1], C[1])) + 1)
        d = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
        if abs(d) < 1e-12:
            continue
        for py in range(miny, maxy + 1):
            yy = py + 0.5
            row = py * w
            for px in range(minx, maxx + 1):
                xx = px + 0.5
                w1 = ((B[0] - xx) * (C[1] - yy) - (B[1] - yy) * (C[0] - xx)) / d
                w2 = ((C[0] - xx) * (A[1] - yy) - (C[1] - yy) * (A[0] - xx)) / d
                w3 = 1.0 - w1 - w2
                if w1 < 0 or w2 < 0 or w3 < 0:
                    continue
                z = w1 * A[2] + w2 * B[2] + w3 * C[2]
                idx = row + px
                if z > zbuf[idx]:
                    zbuf[idx] = z
                    o = idx * 3
                    buf[o], buf[o + 1], buf[o + 2] = col

    thr = 0.30
    for py in range(1, h - 1):
        row = py * w
        for px in range(1, w - 1):
            z = zbuf[row + px]
            if z < -1e17:
                continue
            if abs(z - zbuf[row + px + 1]) > thr or abs(z - zbuf[row + w + px]) > thr:
                o = (row + px) * 3
                buf[o] //= 3
                buf[o + 1] //= 3
                buf[o + 2] //= 3
    _png(path, w, h, bytes(buf))
    return path
