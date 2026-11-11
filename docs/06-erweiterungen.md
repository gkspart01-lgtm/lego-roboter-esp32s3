# 06 — Günstige Erweiterungen

Alles hier hängt an den schon vorhandenen Schnittstellen (I2C, freier GPIO, DRV8833-Kanal B) — kein neues Board nötig. Preise sind Richtwerte.

## Sensoren

| Bauteil | Preis | Nutzen |
|---|---|---|
| **VL53L0X ToF** | ~2,50 € | Abstand 3 cm–2 m, viel präziser als HC-SR04 auf kurze Distanz, I2C, 3,3 V |
| **TCRT5000 Reflexlichtschranke** | ~0,70 € | Linienverfolgung, Kantenerkennung, Umdrehungszählung |
| **MPU6050 IMU** | ~1,50 € | Neigung, Drehrate, Kollisionserkennung — I2C |
| **AS5600 Magnetencoder** | ~3,00 € | Echte Winkelposition für den TT-Motor (statt nur Zeitsteuerung) |
| **INA219 Stromsensor** | ~1,50 € | Erkennt Blockaden am Motor (Strom steigt) → sanftes Stoppen |
| **zweiter HC-SR04** | ~1,00 € | Rundum-Erkennung |
| **Taster-Modul / Joystick** | ~2,00 € | Lokale Bedienung ohne Handy |

## Aktoren & Anzeige

| Bauteil | Preis | Nutzen |
|---|---|---|
| **0,96" OLED SSD1306** | ~2,50 € | IP-Adresse, Status, Sensorwerte ohne Browser |
| **WS2812B-Ring (8 LEDs)** | ~2,00 € | Statuslicht, Beleuchtung, "Augen" für den Roboter |
| **Passiv-Buzzer** | ~0,30 € | Signalton, Fehlermeldung |
| **zweiter DRV8833-Kanal** | 0 € (frei) | Zweiter TT-Motor — differentielles Fahren |
| **MOSFET-Modul** | ~1,50 € | Lasten schalten (Lampe, PWM-Magnet) |
| **Kugellager-Set 5 × 10 × 4 mm** | ~2,00 € | Wellen sauber lagern, weniger Reibung |

## Wenn mehr Kraft nötig ist

| Upgrade | Preis | Anmerkung |
|---|---|---|
| **MG90S statt SG90** | ~4,00 € | Metallgetriebe, hält LEGO-Lasten deutlich besser |
| **NEMA-14 + DRV8825** | ~10,00 € | Starker Schrittmotor, aber **nicht** mehr sinnvoll an 5 V Powerbank (12 V nötig) |
| **Getriebemotor 1:298 (N20, 6 V)** | ~4,00 € | Langsamer, mehr Drehmoment als 1:90 |
| **Kamera-Upgrade OV3660/OV5640** | +1–2 € beim Boardkauf | 3–5 MP statt 2 MP, bessere Low-Light-Leistung |

## Reihenfolge, in der ich erweitern würde

1. **OLED** — sofort nützlich (IP-Adresse ablesen, Debug)
2. **INA219** — Blockadeerkennung macht die Mechanik robust
3. **VL53L0X** — präziseres Anfahren von Positionen
4. **AS5600** — echte Regelung statt "2 Sekunden laufen lassen"
5. **WS2812** — Statusanzeige, damit man ohne Browser sieht, was los ist
