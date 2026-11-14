# LEGO-Roboter auf ESP32-S3

Steuerplattform für ein LEGO-Projekt: **2 Servos** (SG90 180° + 360°), **Schrittmotor 28BYJ-48**, **TT-Motor**, **Endschalter**, **HC-SR04**, **IR-Lichtschranke** — bedient per Browser vom PC und vom Android-Handy, programmierbar mit **Blockly**. Kamera optional (2. Wahl).

> Kurzfassung: Ein **ESP32-S3-DevKitC-1** (62,7 × 25,4 mm, 5 V, WiFi + BLE 5, alle 36 GPIOs auf Stiftleisten) übernimmt alles — **ohne Expander**, Servos und Sensoren direkt am Board. Steuerplattform **~17,60 €**, komplettes Set **~43,40 €** (Preise Stand 11.11.2026, ohne Versand).

> **Mit Kamera (2. Wahl)?** Dann ESP32-S3-WROOM-1 N16R8 CAM + PCA9685 + PCF8574, Aufpreis ~12 € (Pinplan: [docs/03-verkabelung.md](docs/03-verkabelung.md#3-variante-mit-kamera-2-wahl)).

![ESP32-S3-CAM Board](img/board_esp32s3.jpg)

## Anforderungen → Lösung

| Anforderung | Lösung |
|---|---|
| Motoren: 2× SG90 (180° + Continuous), 28BYJ-48 + ULN2003, TT-Motor 3–6 V | ULN2003 (Stepper, GPIO 4–7) + DRV8833 (TT-Motor, GPIO 8/9) + Servos direkt (GPIO 12/13, LEDC) |
| Sensoren: Endschalter, HC-SR04, IR-Lichtschranke | Direkt an GPIO 10/11 (HC-SR04), 14–17 (Endschalter), 18 (KY-010) — keine Expander |
| Nicht bulky, max. 8 × 10 × 3 cm | Board 6,3 × 2,5 cm, alles gestapelt < 7 × 9 × 2,5 cm |
| 5-V-Powerbank | 5 V / ~80 mA Board, Motoren direkt an 5 V (≥ 2,4 A Powerbank) |
| Bluetooth **und** WLAN | WiFi 2.4 GHz + BLE 5 (Web Bluetooth im Browser) |
| Steuerung per Browser (PC + Android) | Web-UI kommt direkt vom Board (`http://legobot.local`) |
| Blockly | Blockly im selben Web-UI + BIPES/Mixly als Alternative |
| Kamera (optional) | Kamera-Variante als 2. Wahl (OV2640, MJPEG-Stream) |
| Günstig | Steuerplattform **~17,60 €**, komplett **~43,40 €** |

## Kosten

| Paket | Preis |
|---|---|
| **Steuerplattform ohne Kamera** (Board, Treiber, Kleinteile) | **~17,60 €** |
| **+ Aktoren & Sensoren** (Falkos Liste komplett) | **16,82 €** |
| **+ Steckverbinder** (JST-XH-Set) | **~9,00 €** |
| **Komplett ohne Kamera** | **~43,40 €** |
| + Kamera-Erweiterung (CAM-Board + PCA9685 + PCF8574) | + **~12,00 €** |

Details mit Links und Bildern: **[docs/02-einkaufsliste.md](docs/02-einkaufsliste.md)**

## Dokumentation

| Datei | Inhalt |
|---|---|
| [docs/01-hardware.md](docs/01-hardware.md) | Board-Steckbrief, warum ESP32-S3, Kamera-Variante (2. Wahl), verworfene Alternativen, Grenzen |
| [docs/02-einkaufsliste.md](docs/02-einkaufsliste.md) | Stückliste mit Bildern, Preisen, Shop-Links, Bestellhinweise |
| [docs/03-verkabelung.md](docs/03-verkabelung.md) | Pinplan, Stromversorgung, Pegelwandler, Fallstricke — ohne Kamera als Standard |
| [docs/04-software-blockly.md](docs/04-software-blockly.md) | Die drei Software-Wege, Blockly-Architektur, Protokoll, Flashen |
| [docs/05-mechanik-3d-druck.md](docs/05-mechanik-3d-druck.md) | LEGO-Kupplungen, 3D-Druck-Teile, Toleranzen, Montage |
| [docs/06-erweiterungen.md](docs/06-erweiterungen.md) | Günstige Zusatzsensoren und -aktoren mit Preis |
| [docs/07-3d-adapter.md](docs/07-3d-adapter.md) | Eigene 3D-Adapter (STL + OpenSCAD), Rendering-Bilder, geprüfte Fremdmodelle |
| [docs/08-steckverbinder.md](docs/08-steckverbinder.md) | Steckverbinder Board↔Aktoren/Sensoren: Kriterien, Vergleich, Empfehlung |

## Projektstatus

- [x] Hardware ausgewählt und bepreist (Standard: ohne Kamera)
- [x] Pinplan und Stromkonzept (beide Varianten)
- [x] Teile bestellen ([Einkaufsliste](docs/02-einkaufsliste.md))
- [ ] Board flashen (PlatformIO, Arduino-Framework)
- [ ] Firmware v0.1: Web-UI + Motor-/Sensor-API
- [ ] Blockly-Blöcke im Web-UI
- [x] 3D-Adapter konstruiert (`hardware/3d/`, STL + parametrisches OpenSCAD)
- [ ] Adapter drucken und Passung testen (Bohrungen ggf. nachziehen)

## Struktur

```
.
├── README.md
├── docs/
│   ├── 01-hardware.md
│   ├── 02-einkaufsliste.md
│   ├── 03-verkabelung.md
│   ├── 04-software-blockly.md
│   ├── 05-mechanik-3d-druck.md
│   ├── 06-erweiterungen.md
│   ├── 07-3d-adapter.md
│   └── 08-steckverbinder.md
├── hardware/3d/     Eigene Adapter: STL + parametrisches OpenSCAD
├── tools/           Generatoren (Adapter, Verdrahtungsbilder) + SVG-Rasterizer
├── img/wiring/      Pin-für-Pin-Verdrahtungsbilder (SVG)
└── img/             Produktfotos und Renderings (Quelle in der Einkaufsliste verlinkt)
```

## Hinweise

- Preise sind Momentaufnahmen (11.11.2026) und schwanken, besonders bei Amazon-Marketplace und AliExpress.
- Produktfotos in `img/` stammen von den verlinkten Shop-Seiten und dienen nur der Zuordnung der Bauteile.
- Lizenz: [MIT](LICENSE)
