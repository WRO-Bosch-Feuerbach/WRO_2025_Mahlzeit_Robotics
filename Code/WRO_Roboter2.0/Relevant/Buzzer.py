from gpiozero import TonalBuzzer
from time import sleep
import RPi.GPIO as GPIO

Buzzer = TonalBuzzer(18)
#Buzzer.play("A4")
#sleep(2)
#Buzzer.stop()

def DebugSound(duration):
    Buzzer.play("A4")
    sleep(duration)
    Buzzer.stop()

