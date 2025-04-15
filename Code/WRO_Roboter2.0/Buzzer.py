from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(18)

def DebugSound(duration):
    buzzer.on()
    sleep(duration)
    buzzer.off()