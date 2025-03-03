import time
from gpiozero import DistanceSensor
from gpiozero import LineSensor
import RPi.GPIO as GPIO
from board import SCL, SDA
import busio 
from adfruit_pca9685 import PCA9685
from adfruit_motor import motor
from time import sleep

# Ultraschallsensor wird deklariert und kalibriert

Tr = 23
Ec = 24

U_Sensor = DistanceSensor(echo=Ec, trigger=Tr,max_distance=2)

# Daten auslesen

def ReadData():
    return (U_sensor.distance) *100 # *100 um cm zu erhalten

# Motor wird deklariert und kalibriert

GPIO.setmode(GPIO.BCM)

Motor_PIN = 14 
Motor_PWM = 15

GPIO.setup(Motor_PIN, GPIO.OUT)
GPIO.setup(Motor_PWM, GPIO.OUT)

# PWM auf ENA-Pin, um die Geschwindigkeit zu steuern
pwm = GPIO.PWM(Motor_PWM, 100)
pwm.start(0)

# Motor-Grundfunktionen definieren

def motor_running(Geschwindigkeit):
    GPIO.output(Motor_PIN, GPIO.HIGH)
    pwm.ChangeDutyCycle(Geschwindigkeit)
    print("Motor läuft vorwärts")

def motor_stop():
    GPIO.output(Motor_PIN, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    print("Motor gestoppt")

motor_running(50)
time.sleep(6)
motor_stop()