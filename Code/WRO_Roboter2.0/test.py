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
import CameraColorDetection2


def fahren():
  OrangeLine = False
  BlueLine = False
  Line1 = False
  Line2 = False
  CrossedOrangeLines = 0
  CrossedLines = 0
  LineDetected = False
  LineBegin = False
  BackgroundColor = False

  #------------------------------------

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
      MotorAnsteuerung.Motor_Fahren(0.35)
      if distanceLinks < 30:
        test2.set_angle(1,30)
      if distanceRechts < 30:
        test2.set_angle(1,180)
      time.sleep(0.2)

      #DetectedColor = CameraColorDetection2.ColorDetection()
      DetectedColor = CameraColorDetection2.BlackWhiteDetection()

      if DetectedColor == "BLACK":
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
      elif DetectedColor == "WHITE":
        BackgroundColor = True

      if LineBegin == True and BackgroundColor == True: 
        CrossedLines = CrossedLines + 1
        LineBegin = False

      if CrossedLines == 2:
        CrossedSection = CrossedSection + 1
        CrossedLines = 0

      if CrossedSection == 12:
        break

      #if DetectedColor == "ORANGE":
        #print("Orange erkannt")
        #OrangeLine = True
      #elif DetectedColor == "BLUE":
        #print("Blau erkannt")
        #BlueLine = True

      #if BlueLine == True and OrangeLine == True:
        #CrossedSection = CrossedSection + 1
        #print(f"Section crossed: {CrossedSection}")
        #OrangeLine = False
        #BlueLine = False

      #if Line1 == True and Line2 == True:
        #CrossedSection = CrossedSection + 1
        #Line1 = False
        #Line2 = False

      #if CrossedSection == 12:
        #break


    while FahrenRechts == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
      winkel_gerundet = round(winkel) - 10
      print(winkel_gerundet)
      test2.set_angle(1, winkel_gerundet)
      MotorAnsteuerung.Motor_Fahren(0.3)
      if distanceLinks < 30:
        test2.set_angle(1,30)
      if distanceRechts < 30:
        test2.set_angle(1,180)
      time.sleep(0.2)

      #DetectedColor = CameraColorDetection2.ColorDetection()
      DetectedColor = CameraColorDetection2.BlackWhiteDetection()

      if DetectedColor == "BLACK":
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
      elif DetectedColor == "WHITE":
        BackgroundColor = True

      if LineBegin == True and BackgroundColor == True: 
        CrossedLines = CrossedLines + 1
        LineBegin = False

      if CrossedLines == 2:
        CrossedSection = CrossedSection + 1
        CrossedLines = 0

      if CrossedSection == 12:
        break

      #if DetectedColor == "ORANGE":
        #print("Orange erkannt")
        #OrangeLine = True
      #elif DetectedColor == "BLUE":
        #print("Blau erkannt")
        #BlueLine = True

      #if OrangeLine == True:
        #Line1 = True
      #elif BlueLine == True:
        #Line2 = True

      #if Line1 == True and Line2 == True:
        #CrossedSection = CrossedSection + 1
        #Line1 = False
        #Line2 = False

      #if CrossedSection == 12:
        #break

    MotorAnsteuerung.Motor_Fahren(0)


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
