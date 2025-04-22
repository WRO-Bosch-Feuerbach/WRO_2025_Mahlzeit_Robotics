import Ultraschallsensor
import time 
import MotorAnsteuerung
import ServoLenkung
import Startsequenz

#----------------------------- Variablen -----------------------------#

VelocityNormal = 0.35

#---------------------------------------------------------------------#

def Links(Lenkung):

    #---------- FahrenLinks-Schleife ----------#

    if Lenkung == "LINKS":
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      if distanceLinks < 35:                                    # Wenn die Entfernung links zu klein wird lenkt er nach rechts
        test2.set_angle(1,20)
      if distanceRechts < 25:                                   # Wenn die Entfernung rechts zu klein wird lenkt er nach links
        test2.set_angle(1,170)
      winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   # Berechnet Winkel zum links fahen
      winkel_gerundet = round(winkel) + 25                      # Rundet winkel hoch
      test2.set_angle(1, winkel_gerundet)                       # setzt den Winkel von dem Servo für die Lenkung
      MotorAnsteuerung.Motor_Fahren(VelocityNormal)             # fährt bisschen langsamer weiter als davor

def Rechts(Lenkung):

    #---------- FahrenRechts-Schleife ----------#

    if Lenkung == "RECHTS":
      distanceGerade = Ultraschallsensor.checkdistGerade()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceRechts = Ultraschallsensor.checkdistRechts()
      if distanceLinks < 25:                                   # Checkt die Enternung Links und Rechts
        test2.set_angle(1,20)                                  # Lenkt rechts wenn links die Entfernung zu klein wird
      if distanceRechts < 35:                                  #
        test2.set_angle(1,170) 
      winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90  # Winkel zum rechts fahren wird berechnet
      winkel_gerundet = round(winkel) + 30                     # Winkel wird gerundet
      test2.set_angle(1, winkel_gerundet)                      # Winkel von dem Servo für die Lenkung wird gesetzt
      MotorAnsteuerung.Motor_Fahren(VelocityNormal)            # fährt bisschen langsamer weiter

