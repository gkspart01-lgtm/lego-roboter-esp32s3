# 10 — Steckerbelegung: Board, Motoren, Sensoren & Erweiterungen

Diese Seite legt fest, **welcher externe Anschluss wie viele Kontakte braucht, wie sie belegt sind und welche gleichpoligen Stecker wirklich austauschbar sind**. Standard bleibt die Variante ohne Kamera aus [03 — Verkabelung](03-verkabelung.md). Hier bedeutet *Polzahl* die Zahl der elektrischen Kontakte des Steckers, nicht die Zahl der ESP32-GPIOs.

## Grundregel: gleiche Polzahl heißt nicht gleiche Belegung

Ein JST-XH-3-Stecker kann mechanisch in jede XH-3-Buchse passen — aber ein Servo, ein IR-Modul und ein LED-Streifen haben unterschiedliche Signale/Spannungen. **Polzahl codiert nur die Größe, nicht die Funktion.** Verwechslungsgefahr reduzieren wir so:

- **JST-XH 2,5 mm:** Aktoren (Servos, DC-Motor). Höhere Stromreserve, gut greifbar.
- **JST-PH 2,0 mm:** Sensoren und Schalter (niedrige Ströme). PH-Stecker passen nicht in XH-Buchsen.
- **28BYJ-48:** Originalen 5-poligen Stecker zwischen Stepper und ULN2003-Platine beibehalten; nicht neu belegen.
- **Powerbank:** USB-A-Stecker bleibt am Akku. Das 5-V-Kabel endet fest an der Stromverteilung/Schraubklemme — kein kleiner Sensorstecker für den gesamten Motorstrom.

Auf der DevKitC-1-Platine selbst gibt es keine JST-Buchsen. Die Anschlüsse kommen auf eine kleine Löt-/Adapterplatine neben dem ESP32; GPIO-Leitungen werden von dort auf die Stecker geführt. Stromverteilung und Motorversorgung werden getrennt von den GPIO-Signalen verdrahtet (siehe [03](03-verkabelung.md)).

## Standardaufbau: vorhandene Geräte

| Gerät / Verbindung | Anzahl | JST / Stecker | Kontakte | Belegung am Kabel | Austauschbarkeit |
|---|---:|---|---:|---|---|
| **SG90 180° Servo** | 1 | XH 2,5 mm, 3-pol | 3 | 1 GND · 2 +5 V Servo-Rail · 3 PWM GPIO12 | Mit dem 360°-Servo untereinander kompatibel |
| **SG90 360° Servo** | 1 | XH 2,5 mm, 3-pol | 3 | 1 GND · 2 +5 V Servo-Rail · 3 PWM GPIO13 | Mit dem 180°-Servo untereinander kompatibel; Verhalten im Programm ist anders |
| **TT-Getriebemotor** | 1 | XH 2,5 mm, 2-pol | 2 | AOUT1 · AOUT2 vom DRV8833 | Nur mit einem anderen DC-Motor-Ausgang gleicher Art; vertauschen kehrt die Drehrichtung um |
| **28BYJ-48 Stepper ↔ ULN2003** | 1 | Originaler Motorstecker, 5-pol | 5 | Werksbelegung/Phasenfolge | Nur das passende 28BYJ-48-Kabel an die passende ULN2003-Buchse; Kabel nicht nach Farben neu crimpen |
| **HC-SR04 Ultraschall** | 1 | PH 2,0 mm, 4-pol | 4 | 1 GND · 2 ECHO (über 1 kΩ/2 kΩ-Teiler) · 3 TRIG GPIO10 · 4 VCC +5 V | Nur mit gleicher HC-SR04-Belegung. Nicht mit 4-poligen Steuer- oder I2C-Kabeln tauschen |
| **KY-010 Lichtschranke** | 1 | PH 2,0 mm, 3-pol | 3 | 1 GND · 2 +3,3 V · 3 DO GPIO18 | Nur mit einem 3-adrigen Sensor gleicher Pinfolge und 3,3-V-Logik |
| **Endschalter / Mikroschalter** | 3 gekauft; bis 4 anschließbar | PH 2,0 mm, je 2-pol | 2 je Schalter | 1 GND · 2 Signal (GPIO14–17, `INPUT_PULLUP`) | Alle einfachen Schalter mit zwei potentialfreien Kontakten sind untereinander kompatibel; keine Versorgung auf den Schalterstecker legen |
| **Powerbank → Stromverteilung** | 1 | USB-A-Ausgang der Powerbank → fest verdrahtetes Kabel/Schraubklemme | 2 Adern | +5 V · GND | Kein JST-XH-Stecker in der 2,4-A-Hauptzuleitung. Danach auf der Verteilung separat zu Board und Treibern |

**Pinplan-Hinweis:** Die Einkaufsliste enthält derzeit drei Mikroschalter. Damit werden GPIO14–16 benutzt; GPIO17 bleibt frei. Für vier Schalter einen vierten Schalter samt PH-2-Kabel ergänzen.

### Interne Anschlüsse (im Gehäuse, nicht als Kinder-Steckplätze)

| Von → nach | Kontakte | Belegung | Empfehlung |
|---|---:|---|---|
| ESP32 → ULN2003 | 4 Signaladern | GPIO4, 5, 6, 7 → IN1, IN2, IN3, IN4 | Kurz und fest verdrahten; keine gemeinsame 4-polige Sensorbuchse |
| ESP32 → DRV8833 | 2 Signaladern | GPIO8 → AIN1, GPIO9 → AIN2 | Fest verdrahten oder klar als `MOTOR-CTRL` beschriften |
| 5-V-Verteilung → Board | 2 Adern | +5 V → 5V-Pin, GND → GND-Pin | Fest verdrahten; USB und externe 5-V-Einspeisung nicht gleichzeitig anschließen |
| 5-V-Verteilung → ULN2003 / DRV8833 | je 2 Adern | +5 V und GND zu den Treibern | Eigene Stromabgänge; Motorstrom nie durch ESP32-Leiterbahnen führen |

Beim DRV8833 ist `AIN1/AIN2` ein **Steuereingang**, nicht der Motoranschluss. Der TT-Motor hängt an `AOUT1/AOUT2`. Der zweite Motorkanal bleibt für einen späteren DC-Motor frei.

## Welche gleichpoligen Stecker sind kompatibel?

Diese Tabelle beantwortet ausdrücklich die Frage nach den gleichen Polzahlen. **„Mechanisch passend“ bedeutet nicht automatisch „elektrisch richtig“.**

| Polzahl + Serie | Geräte mit dieser Belegung | Untereinander kompatibel? | Nicht damit verwechseln |
|---|---|---|---|
| **PH-2** | Endschalter 1–4: GND + Schaltsignal | **Ja**, einfache Schalter können zwischen den vier Schalterports getauscht werden | XH-2-TT-Motorausgang; Batterie-/5-V-Leitung; DRV8833-Steuereingang |
| **XH-2** | TT-Motor-Ausgang: AOUT1 + AOUT2 | **Ja**, mit einem weiteren DC-Motor-Ausgang mit derselben Belegung | PH-2-Schalter oder +5-V/GND-Versorgung |
| **XH-3** | Servo 180° und Servo 360°: GND +5 V + PWM | **Ja**, die Servos können an den zwei Servoports getauscht werden; das Programm muss dann den passenden Servo-Modus verwenden | PH-3-KY-010, LED-Streifen oder andere 3-adrige Sensoren |
| **PH-3** | KY-010: GND +3,3 V + DO | Nur mit einem Sensor, der **dieselbe Pinfolge und 3,3-V-Logik** hat | XH-3-Servo, der 5 V und PWM erwartet |
| **PH-4** | HC-SR04: GND + ECHO + TRIG + +5 V | Nur mit einem Sensor-/Kabelsatz mit genau derselben Belegung; ECHO-Teiler muss im Kabel/Adapter bleiben | ULN2003 IN1–IN4 oder I2C (SDA/SCL) — gleiche Polzahl, andere Signale |
| **4-poliger ULN-Steueranschluss** *(innen)* | IN1, IN2, IN3, IN4 | Nur mit identischem ULN2003-Steuerkabel | HC-SR04 oder I2C-Modul |
| **5-poliger Stepperanschluss** | 28BYJ-48 ↔ ULN2003 | Nur die passende Motor-/Treiberkombination und Werksbelegung | Kein allgemeiner 5-poliger Sensoranschluss |

Bei einer Ein-Familien-Lösung (nur XH) würden alle Stecker gleicher Polzahl mechanisch passen; dieselbe Kompatibilitätsmatrix gilt dann trotzdem. Die Empfehlung XH für Aktoren und PH für Sensoren macht Fehlstecken zwischen Motor/Servo und Sensor zumindest mechanisch schwieriger. **PH-Sensorstecker gleicher Polzahl können sich weiterhin gegenseitig stecken lassen.**

## Optionale spätere Erweiterungen

| Zusatz | Kontakte | Sinnvolle Belegung | Achtung / Kompatibilität |
|---|---:|---|---|
| **Zusätzlicher Taster** | 2 | GND · Signal mit internem Pull-up | Gleiche PH-2-Belegung wie Endschalter; mit den Endschalterkabeln austauschbar |
| **Einzelne Status-LED** | 2 | GPIO · GND, mit Vorwiderstand in Reihe; falls steckbar: eigene SM-2-Buchse oder fest verlöten | Nicht an 5 V oder direkt an einen Motorstecker; polaritätsabhängig; nicht mit dem PH-2-Schalterkabel verwechseln |
| **WS2812/NeoPixel** | 3 | JST-SM-3 (oder eigene, klar getrennte Buchse): GND · +5 V · DATA | Nicht mit Servo-XH-3 verbinden. 5-V-LED-Streifen können einen 3,3-V-zu-5-V-Datenpuffer benötigen; Stromversorgung separat auslegen |
| **Analoger/digitaler 3-Draht-Sensor** | 3 | GND · +3,3 V · OUT | Nur wenn OUT nie über 3,3 V geht. Nicht automatisch zum KY-010 kompatibel |
| **I2C-Sensor** | 4 | JST-SH-4 (Qwiic/STEMMA QT): GND · +3,3 V · SDA · SCL | Gleiche Polzahl wie HC-SR04, aber anderer Steckertyp und andere Belegung; nicht verbinden |
| **Buzzer-Modul** | 2 oder 3 | passiv: zwei Anschlüsse; Modul: GND · VCC · SIG; falls steckbar, eigener SM-Stecker | Buzzer nicht ohne passenden Treiber direkt aus einem GPIO speisen; kein Switch-/Servoport |
| **Zweiter TT-Motor** | 2 Motoradern + 2 Steueradern | Motorausgang DRV8833 Kanal B; GPIOs für BIN1/BIN2 | Motorstecker passt zum TT-Ausgang; die 2 Steueradern bleiben intern am Treiber |
| **Externer Akku statt Powerbank** | 2 Versorgungsadern | nur nach bestätigter Spannung, Polarität und Schutzbeschaltung | Nicht in PH-2-Endschalterbuchse stecken. Akkuanschluss separat codieren und absichern |

## Wie viele Stecker braucht die aktuelle Standardversion?

Gezählt sind nur **abziehbare Verbindungen zu Motoren und Sensoren**; interne Löt-/Stromverteilungsleitungen und der USB-A-Stecker der Powerbank sind nicht mitgezählt.

| Polzahl | Buchsen / Kabelenden | Anzahl bei 3 Schaltern | Bei 4 Schaltern |
|---:|---|---:|---:|
| 2 | PH-2 Endschalter plus XH-2 TT-Motor | 4 | 5 |
| 3 | 2× XH-3 Servo plus 1× PH-3 KY-010 | 3 | 3 |
| 4 | 1× PH-4 HC-SR04 | 1 | 1 |
| 5 | vorhandener 28BYJ-48-Motorstecker | 1 | 1 |
| **Summe Steckverbindungen** | | **9** | **10** |
| **Summe Kontaktpositionen** | | **26** | **28** |

Das heißt für die Erstbestellung: **XH-2 (TT), XH-3 (2 Servos), PH-2 (3 Schalter), PH-3 (KY-010), PH-4 (HC-SR04)**. Der Stepperstecker ist am Motor meist bereits vorhanden; dafür vor dem Kauf den Lieferumfang des 28BYJ-48-Sets prüfen. Zusätzlich kleine 2- und 4-polige XH-Stecker nur für die internen ULN2003-/DRV8833-Verbindungen verwenden, falls diese nicht fest gelötet werden.

Die Stückzahlen oben zählen **Steckverbindungen**; die Pinplätze werden pro Seite gezählt. Ein abziehbares Paar mit 4 Polen hat also 4 Pinplätze im Stecker und 4 im Gegenstück (8 einzelne Metallkontakte zusammen). Mit drei Mikroschaltern sind es **9 Verbindungen / 26 Pinplätze je Seite**; mit vier **10 / 28**.

**Einkaufslisten-Hinweis:** Die derzeitige Summe in [02 — Einkaufsliste](02-einkaufsliste.md) enthält nur ein JST-XH-Set. Für die XH/PH-Trennung dieser Seite ist zusätzlich ein JST-PH-2,0-mm-Sortiment nötig; dessen Preis ist noch nicht in der Gesamt-Summe enthalten. Wenn du zuerst nur das XH-Set kaufst, nimm XH auch für die Sensoren, aber markiere Buchsen und Stecker sehr deutlich — gleichpolige XH-Stecker passen mechanisch ineinander.

## Montage- und Sicherheitsregeln

1. Auf der Adapterplatine jeden Anschluss mit **Funktion + Polfolge** beschriften, z. B. `SERVO 0: GND / +5V / PWM` oder `HC-SR04: GND / ECHO / TRIG / +5V`.
2. Kabel zusätzlich farblich kennzeichnen; die Farbe allein ist keine ausreichende Codierung. Markiere +5 V rot, GND schwarz, Signal mit einer dritten Farbe.
3. Stromversorgung über eine feste Verteilung führen. Die Hauptzuleitung darf nicht durch einen kleinen Sensorstecker oder das DevKit-Board laufen.
4. HC-SR04-ECHO ist 5-V-Logik: der Spannungsteiler gehört dauerhaft in den Sensor-Kabelsatz; niemals ECHO direkt an den ESP32.
5. Vor dem ersten Einstecken mit dem Multimeter Durchgang, Polfolge und Kurzschlussfreiheit prüfen. Steckverbindungen nicht unter Motorlast oder bei laufendem Programm umstecken.
6. Gleichpolige Buchsen verschiedener Funktion räumlich trennen, mit Portnummer/Funktion markieren und – wenn Kinder frei umstecken – mit einer gedruckten Abdeckung gruppieren. JST-XH/PH sind codiert gegen Verdrehen, aber nicht individuell je Funktion; die Beschriftung bleibt notwendig.

## Bezug zu den übrigen Seiten

- [03 — Verkabelung & Strom](03-verkabelung.md): GPIO-Belegung und Schaltbilder
- [08 — Steckverbinder-Grundsatz](08-steckverbinder.md): Familienvergleich und Kriterien
- [02 — Einkaufsliste](02-einkaufsliste.md): Aktoren, Sensoren und JST-XH-Sortiment
