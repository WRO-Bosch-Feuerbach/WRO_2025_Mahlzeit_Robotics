import RPi.GPIO as GPIO
import time

BUTTON_PIN = 14  # GPIO14 (TX)

# GPIO-Modus setzen
GPIO.setmode(GPIO.BCM)

# GPIO14 als Eingang mit Pull-Up-Widerstand konfigurieren
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Warte auf Button-Druck...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Wenn der Button gedrückt wird
            print("Hallo")
            time.sleep(0.2)  # Entprellen, um Mehrfachauslösungen zu vermeiden
except KeyboardInterrupt:
    print("\nBeende Programm...")
finally:
    GPIO.cleanup()  # GPIOs aufräumen
