import math
import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import test2

if __name__ == "__main__":
  try:
    while True:
      distance = Ultraschallsensor.checkdist()   
      winkel = 90 + ((200 - distance) / (200 - 5)) * 90 
      winkel_gerundet = round(winkel) - 50 
      if distance <= 100:
        print(winkel_gerundet)
        test2.set_angle(1, winkel_gerundet)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('fertig')

      else:
        test2.set_angle(1,90)
        MotorAnsteuerung.Motor_Fahren(0.8)

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)


 
