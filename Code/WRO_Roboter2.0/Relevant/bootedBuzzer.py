from gpiozero import TonalBuzzer
from time import sleep
import RPi.GPIO as GPIO

Buzzer = TonalBuzzer(18)
Buzzer.play("C5")
sleep(0.5)
Buzzer.play("E5")
sleep(0.5)
Buzzer.play("A5")
sleep(0.5)
Buzzer.stop()
