import time
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor
import busio
from board import SCL, SDA
import dis
from gpiozero import DistanceSensor, Servo

#Bestimmung der Pole die an den Motor angeschlossen sind
DCMotor_IN1 = 15 #positiver Pol
DCMotor_IN2 = 14 #negativer Pol

#Einrichtung der I2C Adresse
i2c = busio.I2C(SCL, SDA)

#Erstellung/Deklarierung des Motors und Geschwindigkeit

pwm_motor = PCA9685(i2c, address=0x5f)
pwm_motor.frequency = 1000

DC_Motor = motor.DCMotor(pwm_motor.channels[DCMotor_IN1], pwm_motor.channels[DCMotor_IN2])
DC_Motor.decay_mode = (motor.SLOW_DECAY)

def Motor_Fahren(Geschwindigkeit):
    DC_Motor.throttle = Geschwindigkeit

Tr = 23
Ec = 24
sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)
def checkdist():
    return sensor.distance * 100 


if __name__ == '__main__':
    try:
        while True:
            distance = checkdist()
            DC_Motor.throttle = 1
            while distance < 40:
                DC_Motor.throttle = 0.5
            if distance == 10:
                DC_Motor.throttle = 0
    except KeyboardInterrupt:
        DC_Motor.throttle = 0
   
