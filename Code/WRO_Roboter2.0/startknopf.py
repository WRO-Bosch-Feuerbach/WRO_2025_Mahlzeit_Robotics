import RPi.GPIO as GPIO
import time
import test


# GPIO-Setup
BUTTON_PIN = 5  # GPIO2 (SDA)

# Verwende das BCM-Layout für die GPIO-Nummerierung
GPIO.setmode(GPIO.BCM)

# Button-Pin als Eingabe konfigurieren (ohne Pull-Up)
GPIO.setup(BUTTON_PIN, GPIO.IN)

state = False

def button_callback(channel):
  global state 
  if state:
    test.stoppen()
  else:
    test.fahren()

  state = not state

# Ereignisüberwachung für den Button
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    # Endlosschleife, um das Programm am Laufen zu halten
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Aufräumen der GPIOs beim Beenden
    GPIO.cleanup()