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
      print('Distance ist ' + Ultraschallsensor.checkdist())
      MotorAnsteuerung.Motor_Fahren(0.35)
      lenkung_funktion.lenken_links() 
    elif Ultraschallsensor.checkdist() <= 50:
      print('Distance ist ' + Ultraschallsensor.checkdist())
      MotorAnsteuerung.Motor_Fahren(0.5)
      lenkung_funktion.lenken_gerade()
    else:
      MotorAnsteuerung.Motor_Fahren(1)
      lenkung_funktion.lenken_gerade()
      print('Distance ist ' + Ultraschallsensor.checkdist())

except KeyboardInterrupt:
  MotorAnsteuerung.Motor_Fahren(0)
