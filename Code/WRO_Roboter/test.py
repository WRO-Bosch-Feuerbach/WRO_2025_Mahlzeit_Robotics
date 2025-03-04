import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import lenkung_funktion
import MotorAnsteuerung

try:
  while True: 
    if Ultraschallsensor.checkdist() <= 30:
      MotorAnsteuerung.Motor_Fahren(0.35)
      lenkung_funktion.lenken_links() 
    if Ultraschallsensor.checkdist() <= 50:
      MotorAnsteuerung.Motor_Fahren(0.5)
      lenkung_funktion.lenken_gerade()
    MotorAnsteuerung.Motor_Fahren(1)
    lenkung_funktion.lenken_gerade()






except KeyboardInterrupt:
  MotorAnsteuerung.Motor_Fahren(0)
