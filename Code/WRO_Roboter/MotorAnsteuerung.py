
import time
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor
import busio
from board import SCL, SDA
import time
#Bestimmung der Pole die an den Motor angeschlossen sind
DCMotor_IN1 = 15 #positiver Pol
DCMotor_IN2 = 14 #negativer Pol


#Einrichtung der I2C Adresse
i2c = busio.I2C(SCL, SDA)

#Erstellung/Deklarierung des Motors und Geschwindigkeit

pwm_motor = PCA9685(i2c, address=0x5f)
pwm_motor.frequency = 1000

DC_Motor = motor.DCMotor(pwm_motor.channels[DCMotor_IN1], pwm_motor.channels[DCMotor_IN2])


DC_Motor.duty_cycle = 4000

time.sleep(2)
DC_Motor.duty_cycle = 1000

time.sleep(2)

DC_Motor.duty_cycle = 0
