import RPi.GPIO as GPIO
import time

# Setze die GPIO-Modus
GPIO.setmode(GPIO.BCM)

# Definiere den Pin für den Button (z.B. CON7 ist Pin 17)
BUTTON_PIN = 28

# Setze den Button-Pin als Eingang
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Warte auf Buttondruck...")
    while True:
        # Überprüfen, ob der Button gedrückt wurde
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button gedrückt
            print("Hallo")
            time.sleep(0.2)  # Eine kleine Verzögerung, um mehrfaches Auslösen zu verhindern
except KeyboardInterrupt:
    print("Programm beendet")
finally:
    GPIO.cleanup()  # GPIO zurücksetzen, wenn das Programm beendet wird
