# 02 — Einkaufsliste

Preise geprüft am **11.11.2026**, jeweils ohne Versandkosten. Produktbilder stammen von den verlinkten Shop-Seiten.

> **Standard = ohne Kamera.** Die Kamera-Variante (Abschnitt D) ist optional und die 2. Wahl.

## A) Steuerplattform ohne Kamera (Standard) — ~17,60 €

| Bild | Bauteil | Warum | Preis | Shop |
|---|---|---|---|---|
| — | **ESP32-S3-DevKitC-1**, WROOM-1, 8 MB Flash (N8R2/N8R8) | Gehirn: WiFi + BLE 5, 240 MHz Dual-Core, **alle 36 GPIOs auf Stiftleisten** — keine Expander nötig | **~13,00 €** | [berrybase](https://www.berrybase.at/en/espressif-esp32-s3-devkitc-1-n8r2-esp32-s3-wroom-1-2mb-psram-8mb-flash) · AliExpress-Clones ab ~9 € |
| <img src="../img/drv8833.jpg" width="110"> | **DRV8833 Motortreiber** (2 Kanäle, 1,5 A) | TT-Motoren; kleiner und kühler als L298N, 3,3-V-Logik ok | **1,59 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/drv8833-dc-motor-treiber-modul-tb6612-alternative) |
| — | **Kleinteile**: 1000 µF/10 V Elko, 100 nF, Dupont-Kabel, Lochraster, M2-Schrauben + Distanzbolzen | Puffer, Bench-Verkabelung, Montage | **~3,00 €** | diverse |
| | **Summe** | | **~17,60 €** | |

Servos laufen **direkt am Board** (GPIO 12/13, LEDC-PWM), Endschalter und Lichtschranke **direkt an GPIO** (interne Pull-ups) — daher kein PCA9685 und kein PCF8574.

## B) Aktoren & Sensoren — 16,82 €

| Bild | Bauteil | Rolle im Projekt | Preis | Shop |
|---|---|---|---|---|
| <img src="../img/stepper.jpg" width="110"> | **28BYJ-48 5 V + ULN2003** | Schrittmotor, ~15 rpm, ~0,34 kg·cm — Drehteller, Schnecke, Dosierer | **2,19 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/schrittmotor-28byj48-inkl.-treiber) |
| <img src="../img/servo180.jpg" width="110"> | **SG90 9 g, 180°** | Positionieren: Greifer, Klappe, Lenkung | **1,65 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/sg90-9g-micro-servomotor) |
| <img src="../img/servo360.jpg" width="110"> | **SG90 360° (Continuous)** | Antrieb mit einstellbarer Drehzahl (nur Geschwindigkeit, keine Position) | **5,45 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/tower-pro-sg90-digitaler-micro-servo-9g-3600) |
| <img src="../img/ttmotor.jpg" width="110"> | **Getriebemotor 1:90, 3–6 V** (TT-Klasse, Metallgetriebe) | Fahrwerk / Förderband | **4,09 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/1-90-dc-getriebemotor-110rpm-3-6v-metallmotor-mit-doppelwelle-fuer-arduino-roboter) |
| <img src="../img/hcsr04.jpg" width="110"> | **HC-SR04** | Abstand 2–400 cm (5 V Betrieb, ECHO braucht Teiler) | **0,99 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/ultraschallsensor-hc-sr04) |
| <img src="../img/ir.jpg" width="110"> | **KY-010 Lichtschranke** (IR, digital) | Lichtschranke / Reflektionssensor, 3,3 V tauglich | **1,45 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/ky-010-lichtschranke-modul) |
| — | **3× Mikroschalter** mit Hebel/Rolle | Endlagen, Anschläge, Taster | **~1,00 €** | diverse |
| | **Summe** | | **16,82 €** | |

## C) Steckverbinder & Verkabelung (neu) — ab ~6 €

Details und Begründung: [docs/08-steckverbinder.md](08-steckverbinder.md). Empfehlung: **JST-XH 2,5 mm** (codiert, billig, verlängerbar, 3 A) für alle Aktoren/Sensoren.

| Bauteil | Preis | Hinweis |
|---|---|---|
| **JST-XH-Set 2/3/4/5-polig** (Stecker + Buchsen + Crimpkontakte, ~230–250 Stk.) | **~9,00 €** | [botland](https://botland.de/steckverbinder-254-mm-raster/19558-satz-justpi-jst-xh254-2-3-4-5-pin-stecker-mannlich-weiblich-und-weibliche-pins-fur-das-buchsengehause-230-stk-5904422328559.html) · eBay/Amazon |
| **Crimpzange** (SN-28B oder Dupont/JST, 0,03–0,5 mm²) | **~10–15 €** | nur wenn selbst gecrimpt wird |
| *oder* **fertige JST-XH-Pigtails** (10/20 cm, je Polzahl) | **~6 €** | ersetzt Crimpzange, wenn man nicht selbst crimpen will |
| Schrumpfschlauch-Sortiment + Kabelbinder | **~3 €** | Zugentlastung, Isolierung |

## D) Optional: Kamera-Erweiterung (2. Wahl)

Kamerabild im Browser? Dann statt des DevKitC-1 das CAM-Board plus die zwei Expander:

| Bild | Bauteil | Preis | Shop |
|---|---|---|---|
| <img src="../img/board_esp32s3.jpg" width="130"> | **ESP32-S3-WROOM-1 N16R8 CAM**, OV2640, 16 MB/8 MB (statt DevKitC-1) | **16,70 €** | [Amazon.de](https://www.amazon.de/-/en/Ptdfjspt-ESP32-S3-Development-Bluetooth-ESP32-S3-WROOM-1-black/dp/B0F2QP1VTQ) |
| <img src="../img/pca9685.jpg" width="110"> | **PCA9685 16-Kanal Servo-Treiber** (I2C) | **6,50 €** | [berrybase.de](https://www.berrybase.de/en/berrybase-16-channel-pwm-servo-driver-board-pca9685-i2c-12bit-1.6khz-3.3-5v) |
| <img src="../img/pcf8574.jpg" width="110"> | **PCF8574 I2C-Expander** (8 Eingänge) | **2,09 €** | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/pcf8574-io-i2c-erweiterungsmodul) |

Netto-Aufpreis gegenüber der Standard-Variante: **~12 €** (Board-Tausch + 8,59 € Expander).

## E) Gesamt

| Paket | Summe |
|---|---|
| Steuerplattform ohne Kamera (A) | ~17,60 € |
| Aktoren & Sensoren (B) | 16,82 € |
| Steckverbinder (C, ohne Crimpzange) | ~9,00 € |
| **Komplett ohne Kamera** | **~43,40 €** |
| + Kamera-Erweiterung (D) | + ~12,00 € |
| **Komplett mit Kamera** | **~55,40 €** |

Sparvariante: Board als AliExpress-Clone (~9 €) + fertige Pigtails statt Crimp-Set (~6 €) → komplett ohne Kamera **~39 €**.

## Vorhanden / zusätzlich nötig

- 5-V-Powerbank mit **≥ 2,4 A** Ausgang (10.000 mAh ≈ 8–10 h Betrieb)
- Lötkolben, Seitenschneider; Crimpzange nur bei Abschnitt C ohne Pigtails
- 3D-Drucker (Adapter, Halter) — siehe [05-mechanik-3d-druck.md](05-mechanik-3d-druck.md)
- Optional: USB-C-/Micro-USB-Kabel **mit Datenleitung** (viele Billigkabel laden nur)

## Bestellhinweise

- **Board:** DevKitC-1 in N8R2 oder N8R8 — ohne Kamera ist PSRAM egal, daher reicht die günstigste Variante. Achtung: N8R2 ist bei Espressif EOL; lieferbar ist meist N8R8 (z. B. reichelt ~16,80 €) oder ein Clone (~9 €).
- **JST-XH:** Codierung beachten — die Gehäuse haben eine Nase, passt nur in einer Orientierung. Für Verpolungsschutz zusätzlich die Aderfarben-Konvention einhalten (Pin 1 = GND/dunkel).
- **KY-010** an 3,3 V betreiben, dann ist der Digitalausgang direkt ESP-tauglich. **HC-SR04** braucht 5 V und einen Spannungsteiler am ECHO-Pin (siehe Verkabelung).
- **Servos:** SG90-Klone streuen bei Stellstrom und Getriebespiel. Für LEGO-Lasten mit echtem Kraftbedarf: **MG90S** (Metallgetriebe, ~4 €) statt SG90.
- **Mikroschalter:** 3 Stück reichen für den Anfang; 10er-Pack kostet ~3 €.
