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
      winkel = math.degrees(math.atan(distance+10/distance)) + 45
      #if distance <= 100:
       # print(distance)
        #test2.set_angle(1, winkel)
        #MotorAnsteuerung.Motor_Fahren(0.5)
        #print('fertig')
      if 5 < distance < 60:
        test2.set_angle(1, 180)
        MotorAnsteuerung.Motor_Fahren(0.3)
        print('1')
      elif 60 < distance < 80:
        test2.set_angle(1, 140)
        MotorAnsteuerung.Motor_Fahren(0.4)
        print('2')
      elif 80 < distance < 120:
        test2.set_angle(1, 110)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('3')
      elif 120 < distance < 140:
        test2.set_angle(1, 100)
        MotorAnsteuerung.Motor_Fahren(0.7)
      else:
        test2.set_angle(1,90)
        MotorAnsteuerung.Motor_Fahren(0.8)

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)


