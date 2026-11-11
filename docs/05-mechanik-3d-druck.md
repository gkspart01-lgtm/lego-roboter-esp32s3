# 05 — Mechanik & 3D-Druck

> Fertige, druckbare Adapter (SG90, 28BYJ-48, TT-Motor → LEGO-Kreuzachse) liegen in **[07-3d-adapter.md](07-3d-adapter.md)** — als STL, OpenSCAD und mit Renderings.

## LEGO-Maße, die man kennen muss

| Größe | Wert |
|---|---|
| Rastermaß (Stud-Abstand) | 8,0 mm |
| Technic-Kreuzachse | 4,8 mm über Kreuz, Länge in 8-mm-Schritten (1L = 8 mm) |
| Technic-Bohrung | 4,9 mm (Axialspiel ~0,1 mm) |
| Stud-Durchmesser | 4,8 mm |
| Plattenhöhe | 3,2 mm (Brick 9,6 mm) |

Eine 8 × 10 Noppen Grundplatte ist **64 × 80 mm** — passt genau in dein 8 × 10 × 3 cm Gehäuse.

## Zu druckende Adapter

| Teil | Zweck | Konstruktionshinweis |
|---|---|---|
| **Servohorn → Kreuzachse** | SG90 treibt LEGO-Welle | Aufnahme für 20T-Verzahnung (SG90) mit 4,8-mm-Kreuzloch; PETG, 4 Perimeter — PLA reißt bei Drehmoment |
| **SG90-Halter** | Servo im LEGO-Raster | 2× M2-Bohrung im Abstand 28 mm, Gehäuse 23 × 12,3 mm Taschen, seitliche 8-mm-Rasterlöcher für Technic-Pins |
| **TT-Motor → Radnabe/Kreuzachse** | Fahrwerk | 3-mm-D-Welle; Nabe mit 4,8-mm-Kreuzloch oder direkt LEGO-Radaufnahme |
| **28BYJ-48 → Drehteller** | Drehteller, Dosierer, Schnecke | 5-mm-Welle mit Fläche; Adapter auf LEGO-Drehteller 4×4 oder Schneckenrad |
| **Board-Tray** | ESP32 + Treiber stapeln | 2× M2-Distanzbolzen, Kabelauslässe seitlich, 8-mm-Raster unten für Technic-Pins |
| **Elko-Halter / Kabelkanal** | Ordnung, Zugentlastung | optional, spart Nerven |

**Suchbegriffe für fertige Modelle:** `SG90 LEGO adapter`, `micro servo to LEGO technic axle`, `TT motor LEGO wheel hub`, `28BYJ-48 LEGO turntable`.

## Druckeinstellungen (Erfahrungswerte)

- Material: **PETG** für alles, was Drehmoment überträgt (Verzahnung, Naben), PLA für Halter und Tray
- Düse 0,4 mm, Schichthöhe 0,16–0,2 mm
- 4 Perimeter, 30 % Infill (Wandstärke zählt, nicht Infill)
- **Toleranzen:** Kreuzloch als 4,9–5,0 mm konstruieren, bei PETG 0,05 mm Zugabe; Verzahnung 0,1 mm Spiel
- Verzahnung/Achssitz lieber zweimal testen: kleines Teststück drucken, bevor das ganze Getriebe gedruckt wird

## Montage

1. Board-Tray auf die Grundplatte, ESP32 mit M2-Distanzbolzen (5 mm) verschraubt — genug Luft, dass die Kamera frei sieht.
2. Treiber (DRV8833, ULN2003, PCA9685) auf die Rückseite des Tray-Deckels, kurze Kabel zu den Motoren.
3. 5-V-Verteilung als Lötleiste oder Wago-Klemme am Rand, Elko direkt daneben.
4. Powerbank mit Klettband außen — nicht mit ins Gehäuse, sonst wird der Deckel zu hoch.
5. Kabel für Servos mit etwas Schlaufe führen, sonst reißt die Litze beim Einschlag.

## Wichtige Mechanik-Hinweise

- **SG90 ist schwach** (~1,8 kg·cm bei 4,8 V). LEGO-Getriebe haben viel Reibung — für Lasten lieber MG90S (Metallgetriebe) oder eine Untersetzung einplanen.
- **360°-Servo kann nur Drehzahl**, keine Position. Für Positionieren den 180°-Servo nehmen, für Antrieb den 360°-Servo.
- **28BYJ-48 ist langsam** (~15 rpm) und schwach (~0,34 kg·cm), dafür billig und mit exakten Schritten. Perfekt für Drehteller und Schneckenantrieb, nicht fürs Fahrwerk.
- **Endschalter immer als Hardware-Stopp** vorsehen (Stepper stoppt bei Endlage), nicht nur in Software.
- Beim Fahren mit TT-Motor: Räder nicht starr auf die Welle kleben — gedruckte Nabe mit Madenschraube oder Presssitz, sonst rundet die Welle aus.
