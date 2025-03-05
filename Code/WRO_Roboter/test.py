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
      winkel = math.degrees(math.atan((distance+5)/distance)) 
   
      if distance <= 90:
        print(distance)
        print(winkel)
        test2.set_angle(0,winkel)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('fertig')

      else:
        test2.set_angle(0,35)
        MotorAnsteuerung.Motor_Fahren(0.7)
      

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(0,80)
