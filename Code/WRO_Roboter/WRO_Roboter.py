import time
from gpiozero import DistanceSensor
from gpiozero import LineSensor
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
    return (U_Sensor.distance) *100 # *100 um cm zu erhalten

