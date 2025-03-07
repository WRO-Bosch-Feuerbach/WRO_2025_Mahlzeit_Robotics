import RPi.GPIO as GPIO
import time
import test

BUTTON_PIN = 15
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Warte auf Button-Druck...")



def button():
  if GPIO.input(BUTTON_PIN) == GPIO.LOW:
    time.sleep(0.2)
    test.fahren()



if __name__ == "__main__":
  while True:
    button()

