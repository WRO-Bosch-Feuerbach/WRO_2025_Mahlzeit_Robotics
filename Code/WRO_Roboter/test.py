from encodings.punycode import T
import math
import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import test2
import CameraColorDetection


OrangeLine = False
BlueLine = False
CrossedOrangeLines = 0
CrossedSection = 0
RoundCounter = 0

if __name__ == "__main__":
  try:
    while True:
      distance = Ultraschallsensor.checkdist()
      winkel = math.degrees(math.atan((distance+5)/distance))
      DetectedColor = CameraColorDetection.ColorDetection()

      if DetectedColor == "ORANGE":
          OrangeLine = True
          BlueLine = False

      elif DetectedColor == "BLUE":
          BlueLine = True
          OrangeLine = False

      if distance <= 90:
        print(distance)
        print(winkel)
        test2.set_angle(0,winkel)

      distance = Ultraschallsensor.checkdist()   
      winkel = 90 + ((200 - distance) / (200 - 5)) * 90 
      winkel_gerundet = round(winkel) - 50 
      if distance <= 100:
        print(winkel_gerundet)
        test2.set_angle(1, winkel_gerundet)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('fertig')

      else:
        test2.set_angle(0,35)
        MotorAnsteuerung.Motor_Fahren(0.7)

      if OrangeLine == True and BlueLine == True:
          CrossedSection = CrossedSection + 1

      if CrossedSection == 4:
          break
     
      test2.set_angle(1,90)
      MotorAnsteuerung.Motor_Fahren(0.8)

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)


 
