# 04 — Software & Blockly

> **Standard ist die Variante ohne Kamera.** Die Kamera-Spalten und -Bibliotheken (`esp32-camera`, MJPEG-Stream) betreffen nur die Kamera-Variante (2. Wahl); ohne Kamera läuft dieselbe Firmware einfach ohne Stream und ohne `esp32-camera`.

## Die drei Wege im Vergleich

| | **Weg A — eigene Firmware + Web-UI** *(Empfehlung)* | **Weg B — BIPES** | **Weg C — Mixly / Arduinoblocks** |
|---|---|---|---|
| Werkzeug | Arduino C++ (PlatformIO), Webseite im Browser | Blockly im Browser → MicroPython über WebREPL | Blockly (Desktop/Web) → Arduino-Code |
| Wo läuft die Blocklogik? | im Browser, Befehle per WebSocket ans Board (optional als JSON-Programm aufs Board) | als Python-Programm **auf dem Board** | als C++-Programm **auf dem Board** |
| Kamerabild im Browser | **ja**, im gleichen UI wie die Steuerung | nein (Kamera in MicroPython nur mit Spezial-Firmware) | nein |
| Fertige Bedienoberfläche fürs Handy | **ja** (Joystick, Slider, Sensoranzeige) | nur BIPES-IDE bzw. separates freeboard-Dashboard | Dashboard je nach Plattform |
| Aufwand für dich | Firmware schreibe ich, du flasht | null, sofort loslegen | Installation Arduino-IDE + Mixly |
| Läuft ohne PC | teilweise (gespeicherte Programme) | **ja** | **ja** |

## Weg A im Detail

Auf dem Board läuft dauerhaft eine Firmware, die alle Motoren und Sensoren als "API" bereitstellt und die Bedienoberfläche selbst ausliefert:

```
http://legobot.local        → Web-UI mit Kamerabild + Steuerung + Blockly
ws://legobot.local/ws       → WebSocket-Befehle (Joystick, Slider, Programme)
http://legobot.local/stream → MJPEG-Kamerastream
BLE "LEGOBot"               → gleiche Befehle per Web Bluetooth (Fallback)
```

Geplanter Funktionsumfang der Firmware v0.1:

- **Kamera:** MJPEG-Stream, VGA, 10–20 fps, Helligkeit/Qualität umschaltbar
- **Antriebe:** 2 Servos (Winkel bzw. Drehzahl), 1 Schrittmotor (Schritte, Tempo, Endlage), 1 TT-Motor (PWM −255…+255)
- **Sensoren:** Abstand (HC-SR04), Lichtschranke, 4 Endschalter — live im UI
- **Sicherheit:** Not-Aus-Button, Watchdog, Motorsperre bei Brownout, Endschalter stoppt Stepper
- **Komfort:** mDNS (`legobot.local`), OTA-Update, WLAN-Setup per Captive Portal beim ersten Start, BLE-Fallback
- **Blockly:** Blockly-Bibliothek liegt mit auf dem Board (LittleFS, 16 MB Flash reichen) → gleiche Seite, offline, ohne Cloud

### Blockly-Architektur

```
Blockly (Browser)  ──generiert──►  JSON-Programm  ──WebSocket──►  Firmware
   Blöcke:                        {"prog":[
   "fahre vorwärts 2 s"             {"t":"motor","ch":0,"pwm":180},
   "servo auf 90°"                  {"t":"wait","ms":2000},
   "wenn Abstand < 20 cm"           {"t":"motor","ch":0,"pwm":0}
   "dann stoppe"                  ]}
```

Damit gibt es zwei Betriebsarten: **live** (Befehl für Befehl aus dem Browser) und **gespeichert** (JSON-Programm landet in LittleFS, das Board führt es autonom aus — der PC darf danach weg). Das nimmt Weg A die einzige echte Schwäche von Weg B.

### Technik-Stack

- PlatformIO, Framework Arduino-ESP32 3.x, Board `esp32-s3-devkitc-1`
- `esp32-camera` (Modell `CAMERA_MODEL_ESP32S3_EYE`), `ESPAsyncWebServer`, `ArduinoJson`, `NimBLE-Arduino`, `Adafruit PWM Servo Driver`, `PCF8574`
- Frontend: ein HTML-File + `blockly_compressed.js` + eigene Blockdefinitionen in `data/`

### Flashen (wenn das Board da ist)

```bash
# Toolchain
pip install platformio

# Projekt
pio run -t upload          # Upload über USB-C (UART-Port, CH340)
pio run -t uploadfs        # Web-UI nach LittleFS
pio device monitor         # Log, zeigt die IP an
```

Board-Einstellungen in `platformio.ini`:

```ini
board_build.flash_mode = dio
board_build.partitions = huge_app.csv
board_build.f_flash = 80000000L
build_flags = -DBOARD_HAS_PSRAM -DARDUINO_USB_CDC_ON_BOOT=1
```

## Weg B im Detail (BIPES)

[BIPES](https://bipes.net.br/ide/) ist quelloffen, läuft komplett im Browser (Chrome/Edge), deutsch, auch als Offline-ZIP. Ablauf:

1. MicroPython-Firmware per Web-Installer aufs Board ([bipes.net.br/flash](https://bipes.net.br/flash/))
2. Board per USB oder WLAN (WebREPL) verbinden
3. Blöcke zusammenklicken → "Run"

Stärke: in 10 Minuten der erste fahrende Roboter, ideal zum Lernen der Blocklogik.
Schwäche: **kein Kamerabild**, keine fertige Joystick-Oberfläche; Kamera in MicroPython braucht eine Sonder-Firmware (`lemariva/micropython-camera-driver`).

## Weg C im Detail

- **Mixly** (kostenlos, quelloffen): Blockly → Arduino-Code, ESP32/ESP32-S3 unterstützt, braucht aber eine lokale Arduino-IDE-Installation als Compiler.
- **Arduinoblocks** (Web, Blockly + fertige Web-Panels): bequem, aber Login/Abo-Modell.

Beide erzeugen Firmware ohne Kamerastream — gut für "Logik auf dem Board", schlecht für deine Kamera-Anforderung.

## Der Unterschied in vier Sätzen

Bei **B** ist dein Blockprogramm **das** Programm auf dem Board: Es läuft autonom, aber die Bedienoberfläche ist die Programmierumgebung selbst — und die Kamera fehlt. Bei **A** läuft auf dem Board nur ein "Motor- und Sensor-Server", deine Blöcke steuern ihn aus dem Browser — dafür bekommst du Kamerabild, Joystick und Slider in einer Oberfläche, die auf Handy und PC identisch aussieht. Mit den als JSON gespeicherten Programmen holt A zusätzlich den Autonomie-Vorteil von B zurück. Deshalb: **A als Basis, B zum Lernen** — beides geht auf demselben Board, nur mit unterschiedlicher Firmware.
