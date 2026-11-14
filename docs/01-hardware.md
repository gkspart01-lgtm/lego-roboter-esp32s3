# 01 — Hardware

## Die Wahl: ESP32-S3-DevKitC-1 (ohne Kamera)

| Merkmal | Wert |
|---|---|
| MCU | ESP32-S3, Dual-Core Xtensa LX7 @ 240 MHz |
| Speicher | 8 MB Flash (N8R2/N8R8) — PSRAM ohne Kamera nicht nötig |
| Funk | WiFi 802.11 b/g/n 2.4 GHz + Bluetooth **LE 5** |
| GPIO | **~36 auf Stiftleisten** (45 intern), alle frei nutzbar |
| Spannung | 5 V (USB oder 5V-Pin), im Betrieb ~80 mA |
| Maße | 62,7 × 25,4 mm |
| Anschluss | 2× USB (Micro-USB UART zum Flashen + USB-C OTG) |
| Preis | ~13–17 € (N8R2-Clones ab ~9 €) |

**Warum dieses Board:** Es ist die schlankste Variante, die alles erfüllt. Alle 36 GPIOs sind auf Stiftleisten herausgeführt — dadurch fallen die zwei Expander (PCA9685, PCF8574) **komplett weg**: Servos hängen direkt an GPIO (LEDC-PWM), Endschalter und Lichtschranke direkt an GPIO mit internen Pull-ups. Weniger Bauteile, kleiner, billiger, einfacher zu verdrahten. Dual-Core: ein Kern Motor-/Servo-Regelung, einer WiFi/Web-UI.

Pinplan und Bilder: [docs/03-verkabelung.md](03-verkabelung.md).

## Variante mit Kamera (2. Wahl)

![ESP32-S3-CAM (mit OV2640)](../img/board_esp32s3.jpg)

Wenn das Kamerabild im Browser Pflicht ist, nimm stattdessen das **ESP32-S3-WROOM-1 N16R8 CAM** Board (mit OV2640, 16 MB Flash / 8 MB PSRAM, ~17 €).

**Warum nur 2. Wahl:** Die Kamera belegt 14 GPIOs — es bleiben nur ~11 Pins frei. Deshalb braucht diese Variante die beiden Expander zurück (PCA9685 für die Servos, PCF8574 für die Schalter), mehr Bauteile, ~9 € Mehrkosten, und der Kamerapuffer zieht zusätzlichen Strom. Genau die Punkte, die deine "schlanke Plattform" vermeiden wollte.

Details zur Kamera-Variante: [docs/03-verkabelung.md](03-verkabelung.md#3-variante-mit-kamera-2-wahl).

## Verworfene Alternativen

| Kandidat | Preis | Warum nicht |
|---|---|---|
| **ESP32-CAM (AI-Thinker)** | ~8 € | Nur 1 freier UART, **kein USB** (FTDI-Adapter nötig), ~6 nutzbare Pins, kein PSRAM → zu wenig für 4× Stepper + 2 Servos + 2 Motoren + 4 Sensoren |
| **Raspberry Pi Zero 2 W** | 19,40 € + Kamera ~7 € + SD ~5 € = ~31 € | Technisch stärker (echtes Video, Python/OpenCV), aber: 65 × 30 mm, 2 A Strom, ~20 s Bootzeit, über Budget. Richtige Wahl, wenn später Bildverarbeitung dazukommt |
| **micro:bit v2** | ~22 € | Blockly top, aber kein WiFi |
| **Arduino Uno / Nano (Clone)** | 3–8 € | 2 KB RAM, kein WiFi |
| **Raspberry Pi Pico W** | ~6 € | WiFi/BLE ja, aber schwächere Arduino-Unterstützung als beim S3 und kein Kamera-Upgrade-Pfad |
| **Seeed XIAO ESP32S3 Sense** | ~18 € | Winzig, aber nur ~11 Pins in 2,54-mm-Raster, kein Platz für Steckerleisten |

## Grenzen (bewusst akzeptiert)

- **Kein Kamerabild** im Browser — die "ohne Kamera"-Variante ist rein Steuerung + Sensorik. Wer ein Bild will, nimmt die Kamera-Variante (2. Wahl) oder später einen Pi.
- **Bluetooth:** nur BLE, kein Bluetooth Classic. Web Bluetooth läuft in Chrome/Edge (PC) und Chrome (Android), **nicht** in Safari/iOS.
- **Strom:** Motoren und Servos hängen an derselben 5-V-Powerbank wie das Board. Spitzen bis ~2,5 A → Powerbank mit ≥ 2,4 A, Elko an die Motorschiene.
