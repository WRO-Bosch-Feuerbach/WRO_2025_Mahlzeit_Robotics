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
  distanceGerade = Ultraschallsensor.checkdistGerade()
  distanceLinks = Ultraschallsensor.checkdistLinks()
  distanceRechts = Ultraschallsensor.checkdistRechts()
  DetectedColor = CameraColorDetection2.ColorDetection2_0()

  #------------------------------------

  CrossedSection = 0
  RoundCounter = 0

  try:
    #----------Startsequenz um zu schauen in welche Richtung der Roboter fahren muss----------#

    while True:

      test2.set_angle(1,100)                                    # Servo gerade stellen
      MotorAnsteuerung.Motor_Fahren(0.4)                        # losfahren


      if distanceGerade < 80:                                   # Hält an um zu prüfen ob links oder rechts mehr platz ist
        MotorAnsteuerung.Motor_Fahren(0)
        time.sleep(2)
        if distanceLinks > distanceRechts:                      # Wenn links mehr platz ist wird das Programm in die FahrenLinks-Schleife springen
          FahrenLinks = True
          FahrenRechts = False
        else:                                                   # Wenn rechts mehr platz ist wird das Programm in die FahrenRechts-Schleife springen
          FahrenRechts = True
          FahrenLinks = False

        break                                                   # Bricht aus erster Schleife aus




    #---------- FahrenLinks-Schleife ----------#

    while FahrenLinks == True:

      winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   # Berechnet Winkel zum links fahen
      winkel_gerundet = round(winkel) + 25                      # Rundet winkel hoch
      test2.set_angle(1, winkel_gerundet)                       # setzt den Winkel von dem Servo für die Lenkung
      MotorAnsteuerung.Motor_Fahren(0.35)                       # fährt bisschen langsamer weiter als davor

      if distanceLinks < 30:                                    # Wenn die Entfernung links zu klein wird lenkt er nach rechts
        test2.set_angle(1,20)
      if distanceRechts < 30:                                   # Wenn die Entfernung rechts zu klein wird lenkt er nach links
        test2.set_angle(1,170)

      #-------- Farberkennung für Hindernisse ----------#

      while BlockColorDetection.Blockfarbe() == 'ROT':          # Checkt ob die Farbe rot ist
        print('Rot')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.3)                      # Wird langsamer
        test2.set_angle(1,20)                                   # lenkt nach rechts
        print('gelenkt')
        if distanceLinks < 20:                                  # Checkt noch die Entfernung an den Seiten
          test2.set_angle(1,20)                                 # lenkt nach rechts
        if distanceRechts < 20:                                 #
          test2.set_angle(1,170)                                # lenkt nach links

        BlockColorDetection.Blockfarbe()                        # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben

      while BlockColorDetection.Blockfarbe() == 'GRUEN':        # Checkt ob Farbe grün ist
        print('Grün')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.3)                      # Wird langsamer
        test2.set_angle(1,170)                                  # lenkt nach links
        print('gelenkt')
        if distanceLinks < 20:                                  # Checkt noch die Entfernung an den Seiten
          test2.set_angle(1,20)                                 # lenkt nach rechts
        if distanceRechts < 20:                                 #
          test2.set_angle(1,170)                                # lenkt nach links

        BlockColorDetection.Blockfarbe()                        # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben

      #---------- Farberkennung Bodenlinien ----------#

      if DetectedColor == "ORANGE":                             # Checkt ob Farbe orange ist
        LineDetected = True                                     # Erste Linie wird erkannt
        if LineDetected == True:                                #
          LineDetected = False                                  # Wird direkt wieder auf False gesetzt um die Zweite Linie wieder zu erkennen
          LineBegin = True                                      # Wird auf True gesetzt damit Linie erst wieder erkannt werden kann nach dem man darüber gefahren ist
          BackgroundColor = False                               # Background ist die weiße Bahn fläche
          print("Line crossed")
      elif DetectedColor == "BLUE":                             # Das gleiche wie bei orange für Farbe Blau
        LineDetected = True                                     #
        if LineDetected == True:                                #
          LineDetected = False                                  #
          LineBegin = True                                      #
          BackgroundColor = False                               #
          print("Line crossed")
      else:                                                     # Default ist das der Boden weiß ist und keine Linie erkannt wurde
        BackgroundColor = True                                  #
        LineDetected = False                                    #

      if LineBegin == True and BackgroundColor == True:         # Wenn vorher eine Linie erkannt wurde und der Boden wieder weiß ist -> Linie komplett überfahren
        CrossedLines = CrossedLines + 1                         # Liniencounter wirdhochgezählt
        LineBegin = False                                       # LineBegin wieder auf False für die nächste Linie
        Buzzer.DebugSound(0.5)

      if CrossedLines == 2:                                     # 2 Linien sind eine Ecke bzw. 1/4
        CrossedSection = CrossedSection + 1                     # 1/4 ist 1 Sektion
        CrossedLines = 0                                        # Überquerte Linien wieder auf 0 um die nächste Sektion zu prüfen
        print("Section crossed")
        print(CrossedSection)
        Buzzer.DebugSound(1)

      if CrossedSection == 12:                                  # Bei 12 überquerten Sektionen sind 3 Runden durchfahren
        break                                                   # Aus der Schleife springen bzw. Programm ist danach Ende





    #---------- FahrenRechts-Schleife ----------#

    while FahrenRechts == True:
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90  # Winkel zum rechts fahren wird berechnet
      winkel_gerundet = round(winkel) + 30                     # Winkel wird gerundet
      test2.set_angle(1, winkel_gerundet)                      # Winkel von dem Servo für die Lenkung wird gesetzt
      MotorAnsteuerung.Motor_Fahren(0.35)                      # fährt bisschen langsamer weiter

      if distanceLinks < 30:                                   # Checkt die Enternung Links und Rechts
        test2.set_angle(1,20)                                  # Lenkt rechts wenn links die Entfernung zu klein wird
      if distanceRechts < 30:                                  #
        test2.set_angle(1,170)                                 # Lenkt links wenn rechts die Entfernung zu klein wird


      #----------- Farberkennung Hindernisse ----------#       Siehe Erklärung FahrenLinks-Schleife

      while BlockColorDetection.Blockfarbe() == 'ROT':
        print('Rot')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.3)
        test2.set_angle(1,20)
        print('gelenkt')
        if distanceLinks < 20:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)

        BlockColorDetection.Blockfarbe()

      while BlockColorDetection.Blockfarbe() == 'GRUEN':
        print('Grün')
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(0.3)
        test2.set_angle(1,170)
        print('gelenkt')
        if distanceLinks < 20:
          test2.set_angle(1,20)
        if distanceRechts < 15:
          test2.set_angle(1,170)

        BlockColorDetection.Blockfarbe()


      #---------- Farberkennung Bodenlinien ----------#   Siehe Erklärung FahrenLinks-Schleife
      if DetectedColor == "ORANGE":
        LineDetected = True
        if LineDetected == True:
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
          print("Line crossed")
      elif DetectedColor == "BLUE":
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




if __name__ == "__main__"

try:
  fahren()
except KeyboardInterrupt:
  MotorAnsteuerung.Motor_Fahren(0)
  test2.set_angle(1,90)
