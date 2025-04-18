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
  Farbe = ''
  CrossedSection = 0
  RoundCounter = 0
  VelocityBegin = 0.4
  VelocityNormal = 0.35
  VelocityObstacle = 0.35

  #-------------------------------------------------------------------- Start Sequenz + Linienerkennung --------------------------------------------------------------------#

  try:
    #----------Startsequenz um zu schauen in welche Richtung der Roboter fahren muss----------#

    while True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      test2.set_angle(1,100)                                    # Servo gerade stellen
      MotorAnsteuerung.Motor_Fahren(VelocityBegin)                        # losfahren


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

      #---------- Farberkennung Bodenlinien ----------#

      DetectedColor = CameraColorDetection2.ColorDetection2_0()

      if DetectedColor == "ORANGE":                             # Checkt ob Farbe orange ist
        LineDetected = True                                     # Erste Linie wird erkannt
        if LineDetected == True:                                #
          LineDetected = False                                  # Wird direkt wieder auf False gesetzt um die Zweite Linie wieder zu erkennen
          LineBegin = True                                      # Wird auf True gesetzt damit Linie erst wieder erkannt werden kann nach dem man darüber gefahren ist
          BackgroundColor = False                               # Background ist die weiße Bahn fläche
      elif DetectedColor == "BLUE":                             # Das gleiche wie bei orange für Farbe Blau
        LineDetected = True                                     #
        if LineDetected == True:                                #
          LineDetected = False                                  #
          LineBegin = True                                      #
          BackgroundColor = False                               #

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
        Buzzer.DebugSound(1)

      print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')
      if CrossedSection == 12:                                  # Bei 12 überquerten Sektionen sind 3 Runden durchfahren
        break                                                   # Aus der Schleife springen bzw. Programm ist danach Ende

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------- Fahren Links + Linienerkennung + Hindernisserkennung ------------------------------------------------------#

    #---------- FahrenLinks-Schleife ----------#

    while FahrenLinks == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   # Berechnet Winkel zum links fahen
      winkel_gerundet = round(winkel) + 25                      # Rundet winkel hoch
      test2.set_angle(1, winkel_gerundet)                       # setzt den Winkel von dem Servo für die Lenkung
      MotorAnsteuerung.Motor_Fahren(VelocityNormal)                       # fährt bisschen langsamer weiter als davor

      if distanceLinks < 30:                                    # Wenn die Entfernung links zu klein wird lenkt er nach rechts
        test2.set_angle(1,20)
      if distanceRechts < 30:                                   # Wenn die Entfernung rechts zu klein wird lenkt er nach links
        test2.set_angle(1,170)

      #-------- Farberkennung für Hindernisse ----------#

      while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:          # Checkt ob die Farbe rot ist
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Rot'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)         # Wird langsamer
        test2.set_angle(1,10)                                   # lenkt nach rechts

        if distanceLinks < 18:                                  # Checkt noch die Entfernung an den Seiten
          test2.set_angle(1,0)                                  # lenkt nach rechts
        if distanceRechts < 18:                                 #
          test2.set_angle(1,180)                                # lenkt nach links

        BlockColorDetection.Blockfarbe()                        # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

      while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:        # Checkt ob Farbe grün ist
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Grün'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)                      # Wird langsamer
        test2.set_angle(1,170)                                  # lenkt nach links

        if distanceLinks < 18:                                  # Checkt noch die Entfernung an den Seiten
          test2.set_angle(1,0)                                  # lenkt nach rechts
        if distanceRechts < 18:                                 #
          test2.set_angle(1,180)                                # lenkt nach links

        BlockColorDetection.Blockfarbe()                        # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben

        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

     #---------- Farberkennung Bodenlinien ----------#

      DetectedColor = CameraColorDetection2.ColorDetection2_0()

      if DetectedColor == "ORANGE":                             # Checkt ob Farbe orange ist
        LineDetected = True                                     # Erste Linie wird erkannt
        if LineDetected == True:                                #
          LineDetected = False                                  # Wird direkt wieder auf False gesetzt um die Zweite Linie wieder zu erkennen
          LineBegin = True                                      # Wird auf True gesetzt damit Linie erst wieder erkannt werden kann nach dem man darüber gefahren ist
          BackgroundColor = False                               # Background ist die weiße Bahn fläche
      elif DetectedColor == "BLUE":                             # Das gleiche wie bei orange für Farbe Blau
        LineDetected = True                                     #
        if LineDetected == True:                                #
          LineDetected = False                                  #
          LineBegin = True                                      #
          BackgroundColor = False                               #

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
        Buzzer.DebugSound(1)

      print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

      if CrossedSection == 12:                                  # Bei 12 überquerten Sektionen sind 3 Runden durchfahren
        break                                                   # Aus der Schleife springen bzw. Programm ist danach Ende

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #---------------------------------------------------------- Fahren Rechts + Linienerkennung + Hindernisserkennung ------------------------------------------------------#

    #---------- FahrenRechts-Schleife ----------#

    while FahrenRechts == True:
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90  # Winkel zum rechts fahren wird berechnet
      winkel_gerundet = round(winkel) + 30                     # Winkel wird gerundet
      test2.set_angle(1, winkel_gerundet)                      # Winkel von dem Servo für die Lenkung wird gesetzt
      MotorAnsteuerung.Motor_Fahren(VelocityNormal)                      # fährt bisschen langsamer weiter

      if distanceLinks < 30:                                   # Checkt die Enternung Links und Rechts
        test2.set_angle(1,20)                                  # Lenkt rechts wenn links die Entfernung zu klein wird
      if distanceRechts < 30:                                  #
        test2.set_angle(1,170)                                 # Lenkt links wenn rechts die Entfernung zu klein wird


      #----------- Farberkennung Hindernisse ----------#       Siehe Erklärung FahrenLinks-Schleife

      while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Rot'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
        test2.set_angle(1,10)
        if distanceLinks < 18:
          test2.set_angle(1,0)
        if distanceRechts < 18:
          test2.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

      while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe ='Grün'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
        test2.set_angle(1,170)
        if distanceLinks < 18:
          test2.set_angle(1,0)
        if distanceRechts < 18:
          test2.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

      #---------- Farberkennung Bodenlinien ----------#   Siehe Erklärung FahrenLinks-Schleife

      DetectedColor = CameraColorDetection2.ColorDetection2_0()

      if DetectedColor == "ORANGE":
        LineDetected = True
        if LineDetected == True:
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
      elif DetectedColor == "BLUE":
        LineDetected = True
        if LineDetected == True:
          LineDetected = False
          LineBegin = True
          BackgroundColor = False
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
        Buzzer.DebugSound(1)
      print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLines};     Sektionen durchfahren: {CrossedSection}', end='')

      if CrossedSection == 12:
        break

    MotorAnsteuerung.Motor_Fahren(0)


  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)

  #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":

  try:
    fahren()
  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    test2.set_angle(1,90)
