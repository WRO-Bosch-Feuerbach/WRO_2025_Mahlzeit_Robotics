from encodings.punycode import T
import math
import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import LenkungGPT


def fahren():
  OrangeLine = False
  BlueLine = False
  Line1 = False
  Line2 = False
  CrossedOrangeLines = 0
  CrossedSection = 0
  RoundCounter = 0

  try:
    test2.set_angle(1, 90)  # Startausrichtung Servo 1
    test2.set_angle(2, 20)  # Startausrichtung Servo 2
    test2.set_angle(3, 0)   # Servo 3 auf 0 setzen (geradeaus)
    while True:
      distanceGerade = Ultraschallsensor.checkdistGerade()  # Distanz messen
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()

      if distanceGerade > 100:  # Wenn kein Objekt innerhalb von 100 cm ist
        test2.set_angle(1, 90)  # Servo 1 in Richtung 130 drehen
        MotorAnsteuerung.Motor_Fahren(0.7)  # Motor fahren lassen
      elif distanceGerade <= 100 and distanceLinks < 50:  # Wenn ein Objekt erkannt wird
        MotorAnsteuerung.Motor_Fahren(0)  # Motor stoppen
        winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
        winkel_gerundet = round(winkel) + 10
        print(winkel_gerundet)
        test2.set_angle(1, winkel_gerundet)
        time.sleep(1)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('fertig')
      elif distanceGerade <= 100 and distanceRechts < 50:
        MotorAnsteuerung.Motor_Fahren(0)
        winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
        winkel_gerundet = round(winkel) - 10
        print(winkel_gerundet)
        test2.set_angle(1, winkel_gerundet)
        time.sleep(1)
        MotorAnsteuerung.Motor_Fahren(0.5)
        print('fertig2')

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
  while True:
    fahren()
