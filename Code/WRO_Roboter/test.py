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
      distance = Ultraschallsensor.checkdist()  # Distanz messen
      print(distance)
      
      if distance > 100:  # Wenn kein Objekt innerhalb von 100 cm ist
        test2.set_angle(1, 90)  # Servo 1 in Richtung 130 drehen
        MotorAnsteuerung.Motor_Fahren(0.7)  # Motor fahren lassen
        
      elif distance <= 100:  # Wenn ein Objekt erkannt wird
        MotorAnsteuerung.Motor_Fahren(0)  # Motor stoppen
        test2.set_angle(3, 180)  # Servo 3 nach links drehen (180 Grad)
        time.sleep(1)  # Kurze Pause, um sicherzustellen, dass der Servo Zeit hat, die Bewegung zu vollziehen

        prüfen = Ultraschallsensor.checkdist()
        # Nach dem Zurückkehren zur Ausgangsposition weiter mit der Logik:
        if prüfen > 100:  # Wenn nach 3 Sekunden die Distanz wieder über 100 ist
          MotorAnsteuerung.Motor_Fahren(0)
          winkel = 90 + ((200 - distance) / (200 - 5)) * 90
          winkel_gerundet = round(winkel) + 10
          print(winkel_gerundet)
          test2.set_angle(1, winkel_gerundet)
          time.sleep(1)
          MotorAnsteuerung.Motor_Fahren(0.5)
          time.sleep(0.2)
          print('fertig')
        else:
          MotorAnsteuerung.Motor_Fahren(0)
          winkel = 90 - ((200 - distance) / (200 - 5)) * 90
          winkel_gerundet = round(winkel) + 10
          print(winkel_gerundet)
          test2.set_angle(1, winkel_gerundet)
          time.sleep(1)
          MotorAnsteuerung.Motor_Fahren(0.5)
          time.sleep(0.2)
          print('fertig2')
        time.sleep(1)
        test2.set_angle(3,0)
        time.sleep(1)


      #DetectedColor = CameraColorDetection.ColorDetection()

      if DetectedColor == "ORANGE":
        time.sleep(0.25)
        if DetectedColor == "ORANGE":
          print("Orange erkannt")
          OrangeLine = True

      elif DetectedColor == "BLUE":
        time.sleep(0.25)
        if DetectedColor == "BLUE":
          print("Blau erkannt")
          BlueLine = True

      if OrangeLine == True:
        Line1 = True

      elif BlueLine == True:
        Line2 = True

      if Line1 == True and Line2 == True:
        CrossedSection = CrossedSection + 1
        Line1 = False
        Line2 = False

      if CrossedSection == 12:
        break

  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)



if __name__ == "__main__":
 fahren()
