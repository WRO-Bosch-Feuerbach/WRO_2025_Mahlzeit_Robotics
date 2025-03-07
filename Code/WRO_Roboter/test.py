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
#import CameraColorDetection


#OrangeLine = False
#BlueLine = False
#Line1 = False
#Line2 = False
#CrossedOrangeLines = 0
#CrossedSection = 0
#RoundCounter = 0

if __name__ == "__main__":
  try:
    while True:
      distance = Ultraschallsensor.checkdist()
      print(distance)
      winkel = 90 + ((200 - distance) / (200 - 5)) * 90
      winkel_gerundet = round(winkel) + 10
      time.sleep(0.1)
      if distance <= 100:
        MotorAnsteuerung.Motor_Fahren(0)
        angle = 0
        test2.set_angle(3, angle)
        distance = Ultraschallsensor.checkdist()
        time.sleep(3)
        if angle == 180 and distance > 100:
          test2.set_angle(3, 90)
          winkel = 90 + ((200 - distance) / (200 - 5)) * 90
          winkel_gerundet = round(winkel) + 10
          print(winkel_gerundet)
          test2.set_angle(1, winkel_gerundet)
          MotorAnsteuerung.Motor_Fahren(0.5)
          print('fertig')
        elif angle == 180 and distance < 100:
          test2.set_angle(3, 90)
          winkel = 90 - ((200 - distance) / (200 - 5)) *90
          winkel_gerundet = round(winkel) + 10
          print(winkel_gerundet)
          test2.set_angle(1, winkel_gerundet)
          MotorAnsteuerung.Motor_Fahren(0.5)
          print('fertig2')

      else:
        test2.set_angle(1,130)
        MotorAnsteuerung.Motor_Fahren(0.7)

      #DetectedColor = CameraColorDetection.ColorDetection()
#
 #     if DetectedColor == "ORANGE":
  #      print("Orange erkannt")
   #     OrangeLine = True
   #     BlueLine = False
#
 #     elif DetectedColor == "BLUE":
  #      print("Blau erkannt")
   #     BlueLine = True
    #    OrangeLine = False

     # if OrangeLine == True:
      #  Line1 = True

      #elif BlueLine == True:
       # Line2 = True

     # if Line1 == True and Line2 == True:
      #  CrossedSection = CrossedSection + 1
       # Line1 = False
        #Line2 = False

     # if CrossedSection == 12:
      #  break

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)



