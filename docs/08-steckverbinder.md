# 08 — Steckverbinder (Board ↔ Aktoren & Sensoren)

Hier geht es nicht um "welchen Stecker nimmt man", sondern um die Grundsatzfrage: **Wie verbindet man Board, Treiber, Servos, Motoren und Sensoren so, dass es hält, sicher ist und ein Kind es nicht kaputt macht?** Die Antwort ist ein Kompromiss aus sechs bis acht Kriterien — die man nicht alle gleichzeitig gewinnen kann.

## Die Kriterien

### 1. Kinderfreundlich
Steckbar ohne Kraft und ohne Werkzeug, grob greifbar, keine blanken/scharfen Kontakte, hörbares Einrasten. Kernfrage: *Kann ein 8-Jähriger den Stecker alleine und richtig setzen?*

### 2. Verpolungsschutz
Zwei Ebenen, die man nicht verwechseln sollte:
- **Stecker-Verpolung** (mechanisch): Das Gehäuse ist codiert, passt nur in einer Orientierung.
- **Versorgungs-Verpolung** (elektrisch): Selbst wenn jemand Plus und Minus vertauscht, geht nichts kaputt (P-MOSFET oder Schottky-Diode + Sicherung am Eingang).

### 3. Verlängerung
Gibt es fertige Verlängerungskabel oder Pigtails in 10/20/50 cm? Muss man für jede Länge neu crimpen?

### 4. Universalität
Ein Steckertyp für alles klingt schön, **kollidiert aber mit dem Verpolungsschutz**: Wenn alle Stecker gleich aussehen, steckt man den Servo in den I2C-Port. Die Lösung ist nicht "ein Stecker für alles", sondern **ein Raster (2,5 mm) mit unterschiedlichen Polzahlen je Funktion**.

### 5. Komplexität
Arbeitsschritte pro Verbindung: abisolieren, crimpen, löten, aufschrumpfen. Wie viel Werkzeug, wie hoch die Fehlerquote?

### 6. Kosten
Pro Stecker (Cent) plus das Einmal-Werkzeug (Crimpzange, 10–70 €).

### 7. Zugentlastung *(was mir noch einfiel)*
Hält der Kontakt, wenn ein Kind am Kabel zieht? Ein guter Crimp fasst **Leiter und Isolation**; lose Dupont-Stecker fallen einfach ab, blanke Stifte biegen sich.

### 8. Steckzyklen / Haltbarkeit *(auch eingefallen)*
Wie oft lässt sich die Verbindung trennen, bis sie wackelt und Kontaktfehler kommen?

### 9. Strombelastbarkeit *(auch eingefallen)*
Servo- und Motor-Spitzen erreichen ~1 A. Ein Stecker für 100-mA-Sensoren reicht für den Motor nicht.

### 10. Verwechslungs-/Positionscodierung *(auch eingefallen)*
Farben, Etiketten, unterschiedliche Polzahlen — damit Stepper-IN1 nicht mit Motor-AIN1 vertauscht wird und jedes Kabel einen eindeutigen Platz hat.

### 11. Hot-Plug-Sicherheit *(auch eingefallen)*
Stecken bei anliegender Spannung. Bei 5-V-Spielzeug unkritisch, aber wer GND zuletzt schaltet, riskiert kurzzeitig falsche Pegel. Für Kinder egal, fürs Debuggen relevant.

### 12. Diagnose / Testbarkeit *(auch eingefallen)*
Kann man mit Multimeter/Oszi noch bequem messen? Verkleidete Stecker = kindersicher, aber beim Fehlersuchen nervig.

### 13. Verfügbarkeit *(auch eingefallen)*
Überall nachkaufbar? Nachkauf einzelner Stecker oder nur im Set?

## Die Kandidaten

| System | Raster | Codiert | Strom | Kosten/Stecker | Verlängerung | Kinder? | Urteil |
|---|---|---|---|---|---|---|---|
| **Dupont/Jumper** | 2,54 mm | nein (blank) | ~1 A | ~0,5 ct | ja (fertige Kabel) | nein | nur zum Ausprobieren auf dem Breadboard |
| **JST-XH** | 2,5 mm | ja (Nase) | ~3 A | ~2–5 ct | ja (Pigtails) | gut | **das Arbeitstier** |
| **JST-PH** | 2,0 mm | ja | ~2 A | ~2–5 ct | ja | gut | kleiner als XH, oft an Akkus/Sensoren |
| **JST-SM** | 2,5 mm | ja + Raste | ~3 A | ~5 ct | mittel | sehr gut | verriegelt fest — gut gegen Zug |
| **Grove (Seeed)** | 4-pol keyed | ja | ~1 A | 1–2 €/Kabel | ja | sehr gut | teuer, groß, eigenes Ökosystem |
| **Qwiic/STEMMA QT** | JST-SH 1,0 mm | ja | ~0,1 A | 1–2 €/Kabel | ja | gut | nur I2C-Signal, winzig, super für Sensoren |
| **Schraubklemmen** | — | ja (Lötfrei) | ~10 A | ~20 ct | nein (Schrauben) | nein | robust, aber Werkzeug + offene Klemmen |
| **XT30** | — | ja | 30 A | ~1 € | ja | gut | nur für die Power-Zuleitung |
| **LEGO Power-Functions / Powered-Up** | — | ja | ~1 A | 2–5 € | ja | sehr gut | passt ins LEGO-System, aber proprietär + teuer |

**Dupont** ist der Standard des Maker-Boards und perfekt zum Entwickeln — aber genau die Eigenschaften, die es auf dem Steckbrett bequem machen (lose, blank, einzeln), machen es im fertigen Aufbau zum Schwachpunkt.

**Grove/Qwiic** sind die eleganteste "kindersichere" Lösung, scheitern hier aber an zwei Dingen: Preis (1–2 € pro Kabel gegenüber Cent-Beträgen bei JST-XH) und — bei Grove — dem eigenen Ökosystem (Sensoren müssen Grove-Stecker haben). **Qwiic** ist für später (I2C-Sensoren) durchaus attraktiv.

## Empfehlung: Stufenmodell

**Stufe 0 — Bench (Entwicklung):** Dupont-Jumper. Schnell, billig, aber nur am Tisch. Vor dem finalen Aufbau ersetzen.

**Stufe 1 — final (Standard):** **JST-XH 2,5 mm** als einheitliches Raster für alles. Codierte Gehäuse (Verpolungsschutz), ~3 A (reicht für Servo/Motor-Spitzen), Pigtails in 10/20/50 cm (Verlängerung ohne Crimpen), Cent-Preise. Verwechslungsschutz über **unterschiedliche Polzahlen**:

| Verbindung | Polzahl | Belegung (Pin 1 = GND/dunkle Ader) |
|---|---|---|
| SG90-Servo | 3-pol | GND · 5V · SIG |
| HC-SR04 | 4-pol | GND · ECHO · TRIG · VCC |
| KY-010 | 3-pol | GND · DO · VCC |
| Endschalter | 2-pol | GND · Signal |
| Stepper IN1–IN4 | 4-pol | IN1 · IN2 · IN3 · IN4 |
| TT-Motor (ab DRV8833) | 2-pol | M+ · M− |
| Powerbank-Eingang | XT30 oder Schraubklemme | — |

**Stufe 2 — kindersicher:** JST-XH **plus** drei Zutaten:
1. **Farb-/Positionscodierung**: eine Aderfarbe = eine Funktion, Etiketten/Bilder am Stecker.
2. **Zugentlastung**: Kabelbinder am Gehäuse, Schrumpfschlauch über dem Crimp.
3. **Elektrischer Verpolungsschutz am Power-Eingang** (gilt für beide Varianten):
   - **P-MOSFET** (z. B. AO3401) als High-Side-Schalter: sperrt bei Falschpolung einfach, fast kein Spannungsverlust (besser als Diode).
   - **Polyfuse ~2 A** in Reihe: schützt bei Kurzschluss.
   - 1000 µF/10 V + 100 nF direkt dahinter.

## Konkrete Antworten auf deine Punkte

- **Kinderfreundlich** → JST-XH codiert + Zugentlastung; Dupont raus, blanke Pins unter Schrumpfschlauch.
- **Verpolungsschutz** → mechanisch über die XH-Nase + Polzahl; elektrisch über P-MOSFET/Polyfuse am Eingang.
- **Verlängerung** → fertige XH-Pigtails; wer selbst crimpt, nimmt das 230-Stk.-Set + SN-28B-Zange.
- **Universalität** → ein Raster (2,5 mm), aber bewusst verschiedene Polzahlen statt eines Universal-Steckers.
- **Komplexität** → ohne Crimpen (Pigtails) nur abisolieren + löten; mit Crimpen ein zusätzlicher Schritt pro Ader.
- **Kosten** → XH-Kit ~9 € einmalig, danach Cent-Beträge pro Stecker; Pigtails ~6 €.

## Fazit

| Kriterium | Lösung |
|---|---|
| Raster | JST-XH 2,5 mm (einheitlich) |
| Verpolungsschutz | XH-Nase + Polzahl-Codierung + P-MOSFET/Polyfuse am Eingang |
| Verlängerung | fertige Pigtails (oder Set + Crimpzange) |
| Universalität | ein Raster, Polzahl je Funktion |
| Komplexität | Pigtails, wenn keine Crimpzange gewünscht |
| Kosten | ~9 € Kit, Cent/Stecker |
| Kindersicher | Codierung + Zugentlastung + Schrumpfschlauch |
| Strom | XH 3 A deckt Servo/Motor-Spitzen ab |
| I2C später | Qwiic/STEMMA QT (JST-SH) als Add-on, oder XH 4-pol |
| Power-Zuleitung | XT30 mit P-MOSFET-Verpolschutz + Polyfuse |

Einzige Ausnahme von der XH-Regel: Die **Powerbank-Zuleitung** als XT30 oder Schraubklemme — die muss mehr Strom, ist aber kein "Steckplatz", den ein Kind ständig zieht.
