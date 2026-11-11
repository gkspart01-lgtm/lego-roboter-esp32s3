"""Generate the LEGO/actuator adapters: STL + preview PNGs + geometry checks."""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import mesh

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_STL = os.path.join(HERE, "..", "hardware", "3d")
OUT_IMG = os.path.join(HERE, "..", "img", "3d")
os.makedirs(OUT_STL, exist_ok=True)
os.makedirs(OUT_IMG, exist_ok=True)

SOCK_IN = 4.95     # LEGO Technic cross axle: 4.8 mm across, 4.9 mm bore in bricks
GAP_DEG = 48.0

PARTS = {
    # name                 clamp bore  wall  ring height  socket height
    "adapter_sg90_lego":   (4.75, 3.40, 10.0, 8.0),   # SG90 20T spline ~4.85 mm
    "adapter_byj48_lego":  (4.90, 3.40, 11.0, 8.0),   # 28BYJ-48 shaft 5 mm + flat
    "adapter_tt_lego":     (2.90, 4.50, 9.0, 8.0),    # TT motor 3 mm D shaft
}


def build(bore, wall, ring_h, sock_h):
    ri, ro = bore / 2.0, bore / 2.0 + wall
    shells = [mesh.c_ring(ri, ro, ring_h, gap_deg=GAP_DEG, segs=48, z0=0.0)]
    shells += mesh.square_socket(ro, SOCK_IN, sock_h, z0=ring_h - 1.5, segs=10)
    return shells, ri, ro


if __name__ == "__main__":
    ok = True
    for name, (bore, wall, ring_h, sock_h) in PARTS.items():
        shells, ri, ro = build(bore, wall, ring_h, sock_h)
        stl = os.path.join(OUT_STL, name + ".stl")
        mesh.write_stl(shells, stl, name)
        (mn, mx) = mesh.bbox(shells)
        vol = mesh.volume(shells) / 1000.0
        oe = mesh.open_edges(shells)
        ring_frac = 1.0 - GAP_DEG / 360.0
        expect = (
            math.pi * (ro ** 2 - ri ** 2) * ring_frac * ring_h
            + (math.pi * ro ** 2 - SOCK_IN ** 2) * sock_h
        ) / 1000.0
        dev = 100.0 * (vol - expect) / expect
        good = oe == 0 and abs(dev) < 2.0
        ok &= good
        print(
            f"{'OK ' if good else '!! '}{name:20s} tris={len(mesh.flat(shells)):4d} "
            f"open_edges={oe} vol={vol:4.2f} cm3 (analytisch {expect:4.2f}, {dev:+.1f}%) "
            f"{mx[0]-mn[0]:.1f}x{mx[1]-mn[1]:.1f}x{mx[2]-mn[2]:.1f} mm "
            f"stl={os.path.getsize(stl)} B"
        )
        mesh.render(shells, os.path.join(OUT_IMG, name + ".png"), w=720, h=640, azim=38, elev=22)
        mesh.render(shells, os.path.join(OUT_IMG, name + "_top.png"), w=720, h=640, azim=25, elev=68)
    print("ALLE TEILE OK" if ok else "PRUEFUNG FEHLGESCHLAGEN")
