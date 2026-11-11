// LEGO-Kreuzachsen-Adapter für Servo / Schrittmotor / TT-Motor
// Parametrisch: Klemmring (geschlitzt) + Vierkant-Stecksockel für LEGO-Technic-Achse
//
// Benutzung: part wählen, in OpenSCAD F5 (Vorschau) / F6 (Rendern) und als STL exportieren.
// Die STLs im Ordner wurden mit tools/make_parts.py erzeugt und sind geometrisch identisch.

part = "sg90";   // "sg90" | "byj48" | "tt"

//         [Bohrung, Wandstärke, Ringhöhe]  mm
params = [
  ["sg90",  [4.75, 3.40, 10.0]],   // SG90 20T-Spline, ~4,85 mm
  ["byj48", [4.90, 3.40, 11.0]],   // 28BYJ-48, 5-mm-Welle mit Fläche
  ["tt",    [2.90, 4.50,  9.0]]    // TT-Motor, 3-mm-D-Welle
];

function pick(name) = [for (p = params) if (p[0] == name) p[1]][0];

bore    = pick(part)[0];
wall    = pick(part)[1];
ring_h  = pick(part)[2];

sock    = 4.95;   // LEGO-Kreuzachse: 4,8 mm über Kreuz, 4,9 mm Bohrung im Stein
sock_h  = 8.0;
gap_deg = 48;     // Schlitzwinkel des Klemmrings
$fn     = 120;

ro = bore / 2 + wall;

module clamp_ring() {
    difference() {
        cylinder(h = ring_h, r = ro);
        translate([0, 0, -1]) cylinder(h = ring_h + 2, r = bore / 2);
        // Schlitz: Keil nach +Y, Breite über den Winkel
        translate([0, 0, -1]) rotate([0, 0, 90 - gap_deg / 2])
            cube([ro * 2, ro * 2 * sin(gap_deg / 2) / cos(gap_deg / 2), ring_h + 2]);
    }
}

module axle_socket() {
    translate([0, 0, ring_h - 1.5])
        difference() {
            cylinder(h = sock_h, r = ro);
            translate([-sock / 2, -sock / 2, -1]) cube([sock, sock, sock_h + 2]);
        }
}

module adapter() {
    union() {
        clamp_ring();
        axle_socket();
    }
}

adapter();
