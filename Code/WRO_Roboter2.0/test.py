from encodings.punycode import T
import math
import time
import Buzzer
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import test2
import CameraColorDetection2
import BlockColorDetection

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

    while True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      print(distanceGerade)
      print(distanceLinks)
      print(distanceRechts)

      test2.set_angle(1,90)
      MotorAnsteuerung.Motor_Fahren(0.5)


      if distanceGerade < 80:
        MotorAnsteuerung.Motor_Fahren(0)
        time.sleep(2)
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
      winkel_gerundet = round(winkel) + 25
      print(winkel_gerundet)
      test2.set_angle(1, winkel_gerundet)
      MotorAnsteuerung.Motor_Fahren(0.4)
      

      DetectedColor = CameraColorDetection2.ColorDetection2_0()
      #DetectedColor = CameraColorDetection2.BlackWhiteDetection()
      
      '''
      if DetectedColor == "ORANGE":
        print("Orange erkannt")
        OrangeLine = True
      elif DetectedColor == "BLUE":
        print("Blau erkannt")
        BlueLine = True

      if BlueLine == True and OrangeLine == True:
        CrossedSection = CrossedSection + 1
        print(f"Section crossed: {CrossedSection}")
        OrangeLine = False
        BlueLine = False

      if CrossedSection == 12:
        break
      '''

      

      if BlockColorDetection.Blockfarbe() == 'ROT':
        print('Rot')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.2)
        test2.set_angle(1,20)
        print('gelenkt')
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)

      elif BlockColorDetection.Blockfarbe() == 'GRUEN':
        print('Grün')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.2)
        test2.set_angle(1,170)
        print('gelenkt')
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)

      else:
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)



      if DetectedColor == "ORANGE":
        print("Orange erkannt")
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
          print("Line crossed")
      elif DetectedColor == "BLUE":
        print("Blau erkannt")
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
          print("Line crossed")
      else:
        BackgroundColor = True
        LineDetected = False

      if LineBegin == True and BackgroundColor == True: 
        CrossedLines = CrossedLines + 1
        LineBegin = False
        Buzzer.DebugSound(0.5)

      if CrossedLines == 2:
        CrossedSection = CrossedSection + 1
        CrossedLines = 0
        print("Section crossed")
        print(CrossedSection)
        Buzzer.DebugSound(1)

      if CrossedSection == 12:
        break


    while FahrenRechts == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
      winkel_gerundet = round(winkel) + 30
      print(winkel_gerundet)
      test2.set_angle(1, winkel_gerundet)
      MotorAnsteuerung.Motor_Fahren(0.4)

      DetectedColor = CameraColorDetection2.ColorDetection2_0()
      #DetectedColor = CameraColorDetection2.BlackWhiteDetection()

      if BlockColorDetection.Blockfarbe() == 'ROT':
        print('Rot')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.2)
        test2.set_angle(1,20)
        print('gelenkt')
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)

      elif BlockColorDetection.Blockfarbe() == 'GRUEN':
        print('Grün')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.2)
        test2.set_angle(1,170)
        print('gelenkt')
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)

      else:
        if distanceLinks < 15:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)
        time.sleep(0.5)





      if DetectedColor == "ORANGE":
        print("Orange erkannt")
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
          print("Line crossed")
      elif DetectedColor == "BLUE":
        print("Blau erkannt")
        LineDetected = True
        if LineDetected == True: 
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
          print("Line crossed")
      else:
        BackgroundColor = True
        LineDetected = False

      if LineBegin == True and BackgroundColor == True: 
        CrossedLines = CrossedLines + 1
        LineBegin = False
        Buzzer.DebugSound(0.5)

      if CrossedLines == 2:
        CrossedSection = CrossedSection + 1
        CrossedLines = 0
        print("Section crossed")
        print(CrossedSection)
        Buzzer.DebugSound(1)

      if CrossedSection == 12:
        break

    MotorAnsteuerung.Motor_Fahren(0)


  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)



def stoppen():
  MotorAnsteuerung.Motor_Fahren(0)
  test2.set_angle(1, 90)


if __name__ == "__main__":
  try:
      fahren()
  except KeyboardInterrupt:
      stoppen()
