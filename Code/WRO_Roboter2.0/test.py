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


def fahren():
  OrangeLine = False
  BlueLine = False
  Line1 = False
  Line2 = False
  CrossedOrangeLines = 0
  CrossedSection = 0
  RoundCounter = 0

  try:
    FahrenLinks = True
    FahrenRechts = True

    while True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      print(distanceGerade)
      print(distanceLinks)
      print(distanceRechts)

      test2.set_angle(1,90)
      MotorAnsteuerung.Motor_Fahren(0.5)


      if distanceGerade < 90:
        MotorAnsteuerung.Motor_Fahren(0)
        time.sleep(1)
        if distanceLinks > distanceRechts:
          FahrenLinks = True
          FahrenRechts = False
        else:
          FahrenRechts = True
          FahrenLinks = False

      break

    while FahrenLinks == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
      winkel_gerundet = round(winkel) - 10
      print(winkel_gerundet)
      test2.set_angle(1, winkel_gerundet)
      MotorAnsteuerung.Motor_Fahren(0.5)
      if distanceLinks < 20:
        test2.set_angle(1,60)
      if distanceRechts < 20:
        test2.set_angle(1,130)
      time.sleep(0.2)

    while FahrenRechts == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
      winkel_gerundet = round(winkel) - 10
      print(winkel_gerundet)
      test2.set_angle(1, winkel_gerundet)
      MotorAnsteuerung.Motor_Fahren(0.5)
      if distanceLinks < 20:
        test2.set_angle(1,60)
      if distanceRechts < 20:
        test2.set_angle(1,130)
      time.sleep(0.2)

      #DetectedColor = CameraColorDetection.ColorDetection()

#      if DetectedColor == "ORANGE":
#        time.sleep(0.25)
#        if DetectedColor == "ORANGE":
#          print("Orange erkannt")
#          OrangeLine = True

#      elif DetectedColor == "BLUE":
#        time.sleep(0.25)
#        if DetectedColor == "BLUE":
#          print("Blau erkannt")
#          BlueLine = True

#      if OrangeLine == True:
#        Line1 = True

#      elif BlueLine == True:
#        Line2 = True

#      if Line1 == True and Line2 == True:
#        CrossedSection = CrossedSection + 1
#        Line1 = False
#        Line2 = False

#      if CrossedSection == 12:
#        break

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)





def stoppen():
  MotorAnsteuerung.Motor_Fahren(0)
  test2.set_angle(1, 90)
  test2.set_angle(2, 20)
  test2.set_angle(3, 0)

if __name__ == "__main__":
  try:
      fahren()
  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
