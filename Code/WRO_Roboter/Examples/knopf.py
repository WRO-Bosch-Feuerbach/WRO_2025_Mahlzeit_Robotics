import time
import subprocess

button = ADC("A2")  # Falls du A1–A5 nutzt, ändere das entsprechend

while True:
    value = button.read()
    print("ADC-Wert:", value)
    if value < 100:  # Falls der Button gedrückt wird (Wert sinkt)
        print("Button gedrückt! Starte Skript...")
        time.sleep(1)  # Verhindert mehrfaches Auslösen
