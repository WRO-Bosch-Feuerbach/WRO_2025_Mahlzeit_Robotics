from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Verwende die PiGPIOFactory für stabilere PWM-Steuerung
factory = PiGPIOFactory()

# Servo an GPIO17 anschließen (Pin 11 auf dem Raspberry Pi) mit pigpio
servo = Servo(17, pin_factory=factory)

while True:
    servo.min()  # Lenkung ganz nach links
    sleep(1)
    servo.mid()  # Lenkung in die Mittelstellung
    sleep(1)
    servo.max()  # Lenkung ganz nach rechts
    sleep(1)
