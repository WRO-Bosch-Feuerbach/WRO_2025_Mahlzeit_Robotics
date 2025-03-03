from re import M
import time
from Examples.test import Motor
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

Motor_PosIn = 15 
Motor_NegIN = 14
Motor_ENA = 7

GPIO.setup(Motor_PosIn, GPIO.OUT)
GPIO.setup(Motor_NegIN, GPIO.OUT)
GPIO.setup(Motor_ENA, GPIO.OUT)

# PWM auf ENA-Pin, um die Geschwindigkeit zu steuern
pwm = GPIO.PWM(ENA, 100)
pwm.start(100)

# Motor-Grundfunktionen definieren

def motor_vorwärts():
    GPIO.output(Motor_PosIn, GPIO.HIGH)
    GPIO.output(Motor_NegIN, GPIO.LOW)
    print("Motor läuft vorwärts")

def motor_rückwärts():
    GPIO.output(Motor_PosIn, GPIO.LOW)
    GPIO.output(Motor_NegIN, GPIO.HIGH)
    print("Motor läuft rückwärts")

def motor_stoppen():
    GPIO.output(Motor_PosIn, GPIO.LOW)
    GPIO.output(Motor_NegIN, GPIO.LOW)
    print("Motor gestoppt")

motor_vorwärts()
time.sleep(6)
motor_rückwärts()
time.sleep(6)  
motor_stoppen()