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
Ein Steckertyp für alles klingt schön, **kollidiert aber mit dem Verpolungs- und Verwechslungsschutz**: gleiche Steckergehäuse lassen sich funktionsfalsch zusammenstecken. Für dieses Projekt nutzen wir deshalb zwei mechanisch getrennte JST-Serien: XH (2,5 mm) für Aktoren, PH (2,0 mm) für Sensoren/Schalter. Innerhalb jeder Serie helfen verschiedene Polzahlen weiter — sie ersetzen aber keine Pinbelegungs-Kennzeichnung.

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

**Stufe 1 — final (Standard):** JST in zwei mechanisch getrennten Familien: **XH 2,5 mm für Aktoren** (Servo, DC-Motor) und **PH 2,0 mm für Sensoren/Schalter**. Dadurch passen Motor-/Servo-Stecker nicht in die Sensorbuchsen. Der ULN2003 behält den vorhandenen 5-poligen Stepper-Stecker; die Powerbank bleibt USB-A und geht fest auf die Stromverteilung. Das kostet etwas mehr als nur XH, verhindert aber mehr Fehlsteckungen. Die genaue Kontaktbelegung und welche Stecker wirklich austauschbar sind: [docs/10-steckerbelegung.md](10-steckerbelegung.md).

| Verbindung | Serie / Polzahl | Belegung (Pin 1 entsprechend markiert) |
|---|---|---|
| SG90-Servo | XH, 3-pol | GND · 5V · SIG |
| HC-SR04 | PH, 4-pol | GND · ECHO · TRIG · VCC |
| KY-010 | PH, 3-pol | GND · 3V3 · DO |
| Endschalter | PH, 2-pol | GND · Signal |
| 28BYJ-48 ↔ ULN2003 | Originalstecker, 5-pol | Werksbelegung beibehalten |
| TT-Motor ab DRV8833 | XH, 2-pol | AOUT1 · AOUT2 |
| Powerbank | USB-A auf feste Stromverteilung | +5V · GND, kein JST in der Hauptzuleitung |

**Wichtig:** Unterschiedliche Polzahlen verhindern nur manche Fehlsteckungen. Zwei JST-XH-3-Stecker (z. B. Servo und WS2812-LED) passen mechanisch ineinander, obwohl sie elektrisch verschieden belegt sind. PH-Sensoren passen nicht in XH-Aktoren, aber gleichpolige PH-Sensoren können weiterhin falsch gesteckt werden. Die konkrete Polfolge und Austauschbarkeit steht in [docs/10-steckerbelegung.md](10-steckerbelegung.md).

**Stufe 2 — kindersicher:** JST-XH für Aktoren + JST-PH für Sensoren **plus** drei Zutaten:
1. **Farb-/Positionscodierung**: eine Aderfarbe = eine Funktion, Etiketten/Bilder am Stecker.
2. **Zugentlastung**: Kabelbinder am Gehäuse, Schrumpfschlauch über dem Crimp.
3. **Elektrischer Verpolungsschutz am Power-Eingang** (gilt für beide Varianten):
   - **P-MOSFET** (z. B. AO3401) als High-Side-Schalter: sperrt bei Falschpolung einfach, fast kein Spannungsverlust (besser als Diode).
   - **Polyfuse ~2 A** in Reihe: schützt bei Kurzschluss.
   - 1000 µF/10 V + 100 nF direkt dahinter.

## Konkrete Antworten auf deine Punkte

- **Kinderfreundlich** → XH-Aktoren und PH-Sensoren passen nicht ineinander; dazu Zugentlastung, Portbeschriftung und keine offenen Pins.
- **Verpolungsschutz** → mechanisch durch XH/PH-Familien, Stecker-Nase und Polzahl; elektrisch über P-MOSFET/Polyfuse am Versorgungseingang.
- **Verlängerung** → passende XH- oder PH-Pigtails; beim Selbstcrimpen Serien und Crimpkontakte nicht mischen.
- **Universalität** → ein Stecksystem mit zwei JST-Serien nach Funktion; Polzahl und Pinfolge je Port eindeutig festlegen.
- **Komplexität** → Pigtails, wenn keine Crimpzange gewünscht ist; zwei Familien erhöhen aber den Sortieraufwand.
- **Kosten** → das vorhandene XH-Kit kostet ~9 €; das zusätzliche PH-Sortiment ist noch nicht eingepreist.

## Fazit

| Kriterium | Lösung |
|---|---|
| Raster | JST-XH 2,5 mm für Aktoren; JST-PH 2,0 mm für Sensoren; Stepperstecker ab Werk |
| Verpolungsschutz | XH/PH-Familien getrennt + Polzahl-Codierung + P-MOSFET/Polyfuse am Eingang |
| Verlängerung | passende Pigtails je Serie (oder Set + Crimpzange) |
| Universalität | JST-Familie, getrennte Serien nach Strom/Funktion und Polzahl je Port |
| Komplexität | Pigtails, wenn keine Crimpzange gewünscht |
| Kosten | ~9 € XH-Kit, PH-Kit zusätzlich und noch nicht eingepreist |
| Kindersicher | Seriencodierung + Beschriftung + Zugentlastung + Schrumpfschlauch |
| Strom | XH für Servo/Motor; Versorgung direkt über feste Verteilung |
| I2C später | eigener JST-SH/Qwiic-Anschluss, nicht auf HC-SR04-PH4 stecken |
| Power-Zuleitung | Powerbank-USB-A an feste Stromverteilung; bei Akku separat absichern/codieren |

Die **Powerbank-Zuleitung** bleibt USB-A und endet fest an der Stromverteilung. Nur bei einem späteren Rohakku wäre ein eigener, verpolungssicherer Hochstromstecker (z. B. XT30) statt JST-PH/XH angebracht.
