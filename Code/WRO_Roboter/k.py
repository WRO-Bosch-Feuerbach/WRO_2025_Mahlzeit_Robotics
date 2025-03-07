import RPi.GPIO as GPIO
import time
#import test

BUTTON_PIN = 2
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Warte auf Button-Druck...")



def button():
  Button_gedrückt = False
  if GPIO.input(BUTTON_PIN) == GPIO.LOW:
    Button_gedrückt = True
  if Button_gedrückt == True:
    print('HI')
    Button_gedrückt = False



if __name__ == "__main__":
  while True:
    button()

