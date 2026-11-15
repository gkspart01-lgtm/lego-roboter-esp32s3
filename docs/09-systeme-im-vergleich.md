# 09 — LEGO- und offene Motorsteuerungs-Systeme im Vergleich

*Recherche- und Preisstand: 15.11.2026. Preise sind Neupreise, wenn noch regulär gelistet, sonst beispielhafte Gebraucht-Angebote aus Deutschland; Versand und Vollständigkeit variieren.*

Diese Seite vergleicht Systeme, die LEGO-Motoren/-Sensoren oder LEGO-kompatible Mechanik steuern. Wichtig: **Geekservo ist ein einzelner Aktor, kein vollständiges Steuersystem.** Die Open-Source-Projekte sind meist Software oder DIY-Elektronik, nicht ein fertiges Set von der Stange.

## Schnellvergleich

| System | Batterie / Strom | Funk / Bedienung | Motoren & Sensoren | Steckverbinder | Preisindikator |
|---|---|---|---|---|---|
| **Mindstorms NXT 2.0** | 6× AA oder Akkupack | Bluetooth + USB; NXT-Software, PC/Mac; App/Blocks generationabhängig | 3 Motorports, 4 Sensorports | 6-polige Mindstorms-Kabel (RJ12-ähnlich, LEGO-spezifisch) | ca. **100–220 €** komplett gebraucht [24] |
| **Mindstorms EV3** | 6× AA oder EV3-Akkupack | Bluetooth + USB; PC/Mac-Software und Tablet-App, nicht browser-first | 3 Motoren, Farb-/Touch-/IR-Sensoren; 4 Eingänge | Mindstorms 6-polig | ca. **145–220 €** Home-Set; Education oft **250 €+** [23][25] |
| **MINDSTORMS Robot Inventor / SPIKE Prime** | Hub mit integriertem Akku | Bluetooth; offizielle App; Pybricks im Browser | 6 Ports, 4 Motoren plus Farb-/Distanzsensoren beim 51515 | LEGO Powered Up 6-polig | Robot Inventor gebraucht ca. **275–339 €**; SPIKE Prime neu ca. **485 €** [45][50] |
| **Power Functions** | Batteriebox 6× AA bzw. 6× AAA; 7,4-V-Akkubox verfügbar | IR-Fernbedienung, keine App/Browser-Programmierung im System | Motoren/Lichter, primär manuelle Ansteuerung; keine universellen Sensorports | LEGO-PF-4-Kontakt-Stecker; Verlängerungskabel verfügbar | gebraucht grob **20–50 €** für kleinen Motor/IR/Batterie-Aufbau [3][43] |
| **Powered Up / Control+** | City Hub 6× AAA; Technic Hub 6× AA; Technic-Hub-Akku extern zukaufbar | Bluetooth; Powered Up-/Control+-App, Pybricks im Browser | City Hub 2, Technic Hub 4 Ein-/Ausgänge; Motoren, Licht, Sensoren | LEGO Powered Up proprietär, 6 Kontakte | Hub allein: **49,99 €** (City), **79,99 €** (Technic) [19][20] |
| **DUPLO-Eisenbahn 10874** | 4× AAA in der Lok | Bluetooth zur optionalen Handy-/Tablet-App; zusätzlich Push & Go | integrierter Motor, Farbsensor erkennt Aktionssteine; keine freien Sensorports | keine externen Nutzerports; internes DUPLO-System | gebraucht etwa **45–80 €** für Zug/Set-Angebote [27][41] |
| **Geekservo** | externe 3,3–6-V-Versorgung; kein Akku/Controller eingebaut | PWM-Signal vom Mikrocontroller, keine eigene Funk-/App-Funktion | 9-g-Servo 180/270° oder Continuous Rotation; Technic-Achse | meist 3-poliges Servo-DuPont (GND/5V/Signal) | ab ca. **7 € je Servo** [15] |
| **Megahub (Open Source)** | DIY-Versorgung je nach ESP32-Aufbau; kein fertiger Akku-/Retail-Preis | BLE oder WiFi-Weboberfläche; Browser-IDE mit Blockly + Lua | 4 Powered Up/WeDo-Ports, zusätzliche GPIOs, IMU | Powered Up/LUMP-Port auf selbstgebauter Platine | **kein fertiges Kit / kein belastbarer Gesamtpreis** [9] |
| **Pybricks (Open Source)** | Batterie hängt vom verwendeten LEGO-Hub ab | Web-App im Chrome/Edge; Python + Blockly; BLE | nutzt Motoren/Sensoren des LEGO-Hubs, 2–6 Ports je Hub | originale Powered Up-/Mindstorms-Stecker des jeweiligen Hubs | Software kostenlos; Hub/Set separat, gebraucht meist teuer [7][8] |
| **Legoino / esp32_PoweredUp (Open Source)** | ESP32 + vorhandener Powered Up-/WeDo-Hub; Strom je nach Hardware | BLE-Library; Beispiel für WiFi-Web-Fernbedienung | steuert LEGO-Hubs, Motoren und Sensoren; keine eigene Leistungselektronik für TT-/SG90-Motoren | ESP32 ↔ Hub über BLE; LEGO-Ports bleiben Powered Up | Software kostenlos; Hardwarekosten abhängig von vorhandenem Hub [10][11] |

**Preis-Lesart:** Kleinanzeigen-Preise sind Angebotspreise, keine garantierten Verkaufspreise; fehlende Akkus, Kabel oder Sensoren ändern den Wert deutlich.[23][24][25] Neue LEGO-Hubs sind nicht mit einem kompletten Robotik-Set vergleichbar.

## 1. LEGO MINDSTORMS: NXT, EV3, Robot Inventor

### NXT 2.0 (2009)

[![LEGO MINDSTORMS NXT 2.0](https://img.bricklink.com/S/8547-1.jpg)](https://www.bricklink.com/v2/catalog/catalogitem.page?S=8547-1)

- **Strom:** 6 AA im Brick, optionaler wiederaufladbarer Akku.[35]
- **Konnektivität:** Bluetooth und USB; PC/Mac-Programmierung, NXT-Software mit Drag-and-drop-Blöcken.[35]
- **I/O:** drei Motor-Ausgänge und vier Sensor-Eingänge; Motoren mit Positionsrückmeldung; Ultraschall-, Touch- und Farbsensor.[32][35]
- **Stecker:** proprietärer LEGO-6-poliger Mindstorms-Stecker, ähnliche Form wie RJ12, aber nicht einfach als Telefonkabel-Standard behandeln.[32]
- **Preis:** am 15.11.2026 lagen Kleinanzeigen-Angebote für komplette NXT-2.0-Sets grob bei **100–220 €**; Vollständigkeit unbedingt prüfen.[24][35]

### EV3 (2013)

[![LEGO MINDSTORMS EV3](https://img.bricklink.com/S/31313-1.jpg)](https://www.lego.com/en-us/product/lego-mindstorms-ev3-31313)

- **Strom:** 6 AA oder EV3-Lithium-Akku.[22]
- **Konnektivität:** Bluetooth und USB; PC/Mac-Software, Tablet-App und Robot-Commander-App.[1][22] Das klassische Erlebnis ist stärker Desktop/App als Browser.[1]
- **I/O:** drei Motor-Ausgänge, vier Sensor-Eingänge.[22] Home-Set mit drei Motoren sowie Farb-, Touch- und IR-Sensoren.[1][1]
- **Stecker:** gleiche Mindstorms-6-polige Familie; Sensoren/Aktoren sind robust und steckbar, aber teuer und proprietär.[22]
- **Preis:** Home-Set-Angebote etwa **145–220 €**; vollständige Education-Sets oft **250 € und höher**.[23][25]

### Robot Inventor 51515 / SPIKE Prime

[![MINDSTORMS Robot Inventor](https://www.lego.com/cdn/cs/set/assets/blt51f714bbdf84524b/51515-PDP-202010-Block-Standard-1.jpg?fit=crop&quality=80&width=400&dpr=1)](https://www.lego.com/en-us/product/robot-inventor-51515)

Das ist die jüngere MINDSTORMS-Generation: **6 Powered-Up-Ports**, ein wiederaufladbarer Hub, Bluetooth, 5×5-Lichtmatrix und Gyro/Accelerometer; Set 51515 enthält vier Motoren und Farb-/Distanzsensoren.[2][46]

- App-zentriert, später auch mit Pybricks im Browser programmierbar.[2][7]
- Powered-Up-Stecker, also nicht kompatibel mit den alten NXT/EV3-Kabeln ohne Adapter.[7]
- Gebrauchte Robot-Inventor-Sets lagen in deutschen Angeboten bei etwa **275–339 €**.[45] SPIKE Prime neu etwa **485 €**.[45][50]
- **Einordnung:** sehr leistungsfähig und gut integriert, aber für dieses LEGO-Projekt preislich überdimensioniert.[2][45]

## 2. LEGO Power Functions

[![Power Functions Batteriebox](https://www.lego.com/cdn/cs/set/assets/blteae30bc0f8b359fa/88000.jpg?fit=crop&quality=80&width=800&height=800&dpr=1)](https://www.lego.com/en-us/product/lego-power-functions-aaa-battery-box-88000)

- **Strom:** 8881-Batteriebox mit 6× AA oder 88000 mit 6× AAA; außerdem gab es eine wiederaufladbare 7,4-V-Batteriebox.[3][34] Der Hersteller nennt für seine Batteriekästen bis zu 800 mA und Überlastschutz.[3]
- **Steuerung:** klassisch mit kabelgebundenem Schalter oder IR-Empfänger + Fernbedienung.[3] Kein integriertes Bluetooth, keine App und keine frei programmierbaren Sensor-Eingänge.[3][3]
- **Aktorik:** M/L/XL-Motoren, Zugmotor, Servo, Lichter.[3] Erweiterungskabel gab es in 20 und 50 cm.[3][3]
- **Stecker:** LEGO-PF-Stecker mit vier Kontakten (zwei Versorgung, zwei Steuersignale).[3] Für Kinder gut greifbar, aber proprietär; Richtung/Polarität wird über Schalter/Empfänger statt mit Standard-H-Brücke geändert.[3][3]
- **Preis:** gebrauchte Einzelteile liegen ungefähr bei 8 € Batteriebox, 9 € IR-Empfänger und 12 € M-Motor; ein kleiner Aufbau landet damit bei **~30 €**, je nach Angebot/Versand.[43]
- **Fazit:** robuste, einfache Motorisierung ohne Programmierung.[3] Gut zum Fahren, nicht als Sensor-/Blockly-Plattform.[3]

## 3. LEGO Powered Up / Control+

[![LEGO Powered Up City Hub](https://www.lego.com/cdn/cs/set/assets/bltaf2734723652468a/88009.jpg?fit=crop&quality=80&width=800&height=800&dpr=1)](https://www.lego.com/de-de/product/hub-88009)

[![LEGO Technic Hub](https://www.lego.com/cdn/cs/set/assets/blt277a125625796629/88012_prod.png?fit=crop&quality=80&width=800&height=800&dpr=1)](https://www.lego.com/de-de/product/technic-hub-88012)

- **Strom:** City Hub 88009 mit 6× AAA; Technic Hub 88012 mit 6× AA; ein separat erhältlicher Akku ist eine weitere Option.[19][20][61]
- **Konnektivität:** Bluetooth zum Smartphone/Tablet.[19] 88009 hat zwei I/O-Ports und kostet bei LEGO **49,99 €**; der 88012 hat vier Ports, integrierten Neigungssensor, verbindet sich mit Powered Up und Control+ und kostet **79,99 €**.[19][20]
- **App/Browser:** offizielle App für einfache Steuerung und Programmierung.[19][20] Browser/Blockly über das Open-Source-Projekt Pybricks, das Chrome/Edge und Bluetooth nutzt.[7]
- **Motoren/Sensoren:** LEGO Smart-Motoren, Licht, Farb-/Distanz-/Neigungssensoren.[19][20] Der Hub überwacht LEGO-Geräte; Hobby-Servos und DC-Motoren wie TT brauchen zusätzliche Elektronik.[20]
- **Stecker:** kleiner LEGO-eigener 6-Kontakt-Stecker mit Erkennung/Kommunikation.[7] Praktisch und kompakt, aber Verlängerungen/Adapter oft teuer oder Drittanbieter.[7]
- **Fazit:** die beste fertige LEGO-native Lösung, wenn man LEGO-Motoren und -Sensoren bereits besitzt.[19][20] Für SG90/TT/HC-SR04 ist es kein direkter Ersatz für unser ESP32-Board.[20]

## 4. DUPLO-Eisenbahn

[![DUPLO Dampfeisenbahn 10874](https://www.lego.com/cdn/cs/set/assets/blt892b06b079302476/10874.jpg?fit=crop&quality=80&width=800&height=800&dpr=1)](https://www.lego.com/de-de/product/steam-train-10874)

- **Strom:** Batterien sitzen in der Lok; ältere Connected-Train-Anleitung zeigt 4× AAA.[48] Kein externes Netzteil und keine herausgeführten Strom-/GPIO-Pins.[4][48]
- **Bedienung:** Push & Go direkt an der Lok oder die optionale DUPLO-App per Bluetooth auf Smartphone/Tablet.[4][21]
- **Sensorik:** fünf farbige Aktionssteine werden von der Lok erkannt und lösen Aktionen (z. B. Horn, Halt, Richtungswechsel) aus.[4] Die Lok hat integrierten Motor; keine frei steckbaren Sensoren/Motoren.[4][4]
- **Stecker:** keine vom Nutzer zugänglichen Anschlüsse.[4] Das ist kindersicher, aber nicht erweiterbar.[4]
- **Preis:** vollständige gebrauchte 10874-Angebote etwa **45–80 €**; Preis hängt stark von Schienen und Figuren ab.[27][41]
- **Fazit:** hervorragend für sehr kleine Kinder — robust und intuitiv, aber weit weg von programmierbarer Universal-Robotik.[4][21]

## 5. Geekservo: LEGO-kompatibler Aktor

[![Geekservo](https://cdn.shopify.com/s/files/1/0174/1800/products/Geekservo_2of3_0e921e61-b341-4cf8-8d0e-fbf8b48b534c.jpg?v=1593189003)](https://www.kittenbot.cc/products/kittenbot-grey-geekservo-servo)

Geekservo ist ein **Servo mit Technic-kompatiblen Befestigungen/Achse**, kein Hub.[13] Varianten gibt es als Positionsservo (180°/270°) und als Continuous-Rotation-Antrieb.[31] Typische Betriebsspannung 3,3–6 V; Continuous-Versionen laufen per PWM-Drehzahlsignal.[15]

- **Stromversorgung:** braucht eine eigene geregelte 5-V-Schiene, nicht den 3,3-V-Pin des ESP32.[13]
- **Konnektivität/App:** keine; Signal kommt von ESP32/Arduino/Servo-Controller.[13]
- **Stecker:** meist 3-polige Servo-DuPont-Buchse (GND/Plus/Signal) — wie SG90, kein LEGO Powered-Up-Stecker.[38]
- **Preis:** etwa **7 €** für die gelistete 9-g-360°-Version; andere Ausführungen/Händlerpreise weichen ab.[15]
- **Nutzen für dein Projekt:** mechanisch besonders LEGO-freundlich; elektrisch wird er genau wie ein normaler Hobbyservo angesteuert.[13][38]

## 6. Open-Source-Projekte

### Megahub — der nächste Verwandte des eigenen Projekts

[![Megahub Hardware](https://raw.githubusercontent.com/mirkosertic/Megahub/main/docs/pcb_iteration1.jpg)](https://github.com/mirkosertic/Megahub)

[![Megahub Blockly-IDE](https://raw.githubusercontent.com/mirkosertic/Megahub/main/docs/screenshot_ide.png)](https://github.com/mirkosertic/Megahub)

ESP32-basierte, offene Plattform mit **4 Powered-Up/WeDo-Ports**, zusätzlichen GPIOs, IMU und einer Web-IDE mit Blockly/Lua.[9] Steuerung über BLE oder WiFi-Webserver; die Platine nutzt zwei I2C-zu-UART-Brücken für die LEGO-Geräteports.[9][9]

- **Stärken:** genau die Mischung aus LEGO-Steckern, Browser-Blockly und ESP32, nach der viele Maker suchen.[9]
- **Grenzen:** keine fertige Kaufplattform und kein veröffentlichter Komplettpreis; Platine/Elektronik müssen selbst gefertigt/bestückt werden.[9] BLE-IDE ist laut README auf Desktop-Chrome/Edge/Opera ausgerichtet; WiFi-Modus liefert eine Weboberfläche.[9]
- **Wichtig für uns:** die Ports sind für Powered-Up/WeDo-Geräte gedacht.[9] SG90, TT-Motor, HC-SR04 und Endschalter müssen weiterhin über eigene Treiber/GPIO angebunden werden.[9]

### Pybricks — offene Firmware/Web-IDE für LEGO-Hubs

[![Pybricks Powered Up Hubs](https://pybricks.com/learn/getting-started/pybricks-powered-up-hubs.webp)](https://pybricks.com/learn/getting-started/what-do-you-need/)

Pybricks ersetzt nicht die Hardware, sondern erweitert kompatible LEGO-Hubs: Web-App, Python und Blockly, Programme laufen direkt auf dem Hub.[7] Chrome/Edge mit Bluetooth nötig; Android wird unterstützt, iOS-Safari nicht.[7] Portzahl und Batterietyp hängen vom Hub ab.[7]

### Legoino und esp32_PoweredUp — ESP32-Bibliotheken

[Legoino](https://github.com/corneliusmunz/legoino) ist eine Arduino-Bibliothek, die ESP32 per BLE mit Powered-Up-, Boost- und DUPLO-Hubs verbindet und Motor-/Sensorwerte steuert.[10]

[esp32_PoweredUp](https://github.com/lemio/esp32_PoweredUp) bietet ebenfalls BLE-Unterstützung für Powered Up/WeDo/DUPLO; das Repo enthält ein Beispiel mit WiFi-Webseite als Fernbedienung und einen browserbasierten Flasher.[11] Es ist eine Bibliothek plus Beispiele, kein fertiges Platinen-/Stecksystem.[11][11]

### DUPLO Train Controller NG

[![Open-Source DUPLO Controller](https://raw.githubusercontent.com/rzuehlsd/DUPLO_Train_Remote_Controller/main/images/Controller_blue.jpeg)](https://github.com/rzuehlsd/DUPLO_Train_Remote_Controller)

Ein unabhängiges ESP32-S3-Handgerät für DUPLO-Züge: eigene Platine/Gehäuse (OpenSCAD), Tasten/Encoder, BLE-Steuerung, Sleep/Wake und Aufnahme/Wiedergabe.[12] Es ist eine spezialisierte Fernbedienung, keine universelle Sensor-/Motorplattform.[12] Preis ist DIY-BOM-abhängig, nicht als fertiges Produkt ausgewiesen.[52]

## Was davon passt zu deinem Vorhaben?

- **Günstig, eigene Motoren/Sensoren, 5-V-Powerbank, Browser:** das ESP32-S3-DevKitC-1 aus unserem Entwurf bleibt am flexibelsten. Geekservo ist nur ein alternativer LEGO-freundlicher Aktor.[13]
- **LEGO-native Steckbarkeit und schon LEGO-Motoren vorhanden:** Powered Up + Pybricks.[7][19][20]
- **Komplett offene LEGO-Port-Plattform mit Blockly:** Megahub ist ein interessantes Projekt zum Nachbauen, aber kein günstiges fertiges Kit und passt nicht direkt zu den SG90/TT/HC-SR04-Komponenten.[9]
- **Kleine Kinder, robuste Bedienung statt Umbau:** DUPLO Connected Train.[4][21]
- **Nur unkompliziert Motoren drehen:** Power Functions; keine Browser-Blockly- oder Sensorplattform.[3]

## Quellenhinweis

Bilder sind von Hersteller-, Händler- oder Projektseiten eingebettet und jeweils auf die Ursprungsseite verlinkt.[1][9] LEGO-Produktbilder und Namen dienen nur der Identifikation; LEGO unterstützt diese Projektseite nicht.[1]

## Sources

[1] https://www.lego.com/en-us/product/lego-mindstorms-ev3-31313
[2] https://www.lego.com/en-us/product/robot-inventor-51515
[3] https://www.lego.com/en-us/themes/power-functions/element-spec
[4] https://www.lego.com/de-de/product/steam-train-10874
[7] https://pybricks.com/learn/getting-started/what-do-you-need
[8] https://pybricks.com/learn/getting-started/install-pybricks
[9] https://github.com/mirkosertic/Megahub
[10] https://github.com/corneliusmunz/legoino
[11] https://github.com/lemio/esp32_PoweredUp
[12] https://github.com/rzuehlsd/DUPLO_Train_Remote_Controller
[13] https://www.kittenbot.cc/products/kittenbot-grey-geekservo-servo
[15] https://eu.robotshop.com/products/geekservo-9g-360-servo-compatible-with-lego
[19] https://www.lego.com/de-de/product/hub-88009
[20] https://www.lego.com/de-de/product/technic-hub-88012
[21] https://www.lego.com/en-us/service/help-topics/article/duplo-connected-train-app
[22] https://www.lego.com/cdn/cs/set/assets/bltbef4d6ce0f40363c/LMSUser_Guide_LEGO_MINDSTORMS_EV3_11_Tablet_ENUS.pdf
[23] https://www.kleinanzeigen.de/s-lego-mindstorms-31313/k0
[24] https://www.kleinanzeigen.de/s-mindstorms-nxt-2-0/k0
[25] https://www.kleinanzeigen.de/s-lego-mindstorm-45544/k0
[27] https://www.kleinanzeigen.de/s-duplo-eisenbahn/k0
[31] https://shop.pimoroni.com/en-eu/products/geekservo-270-lego-compatible-servo
[32] https://www.bricklink.com/v2/catalog/catalogitem.page?S=8547-1
[34] https://www.lego.com/en-us/product/lego-power-functions-battery-box-8881
[35] https://www.lego.com/en-us/product/lego-mindstorms-nxt-2-0-8547
[38] https://thepihut.com/products/geekservo-lego-compatible-180-rotation-servo
[41] https://www.kleinanzeigen.de/s-anzeige/lego-duplo-eisenbahn-set-10874/3345995291-23-6891
[43] https://www.kleinanzeigen.de/s-anzeige/lego-power-functions-set-8881-8883-8884-8885-88003/3557277740-23-9265
[45] https://www.kleinanzeigen.de/s-51515/k0
[46] https://www.lego.com/en-us/aboutus/news/2020/june/lego-mindstorms-robot-inventor
[48] https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6245412.pdf
[50] https://www.lego.com/en-us/product/lego-education-spike-prime-set-45678
[52] https://github.com/rzuehlsd/DUPLO_Train_Remote_Controller/blob/main/images/Controller_blue.jpeg
[61] https://keybrick.one/specs
