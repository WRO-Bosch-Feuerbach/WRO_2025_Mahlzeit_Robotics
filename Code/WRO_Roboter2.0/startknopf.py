import time
import test
import RPi.GPIO as GPIO

BUTTON_PIN = 5  # GPIO2 (SDA)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

state = False

def button_callback(channel):
  global state
  if state:
    test.stoppen()
  else:
    test.fahren()

  state = not state

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()















