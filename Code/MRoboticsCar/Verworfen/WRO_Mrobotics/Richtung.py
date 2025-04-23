import Ultraschallsensor
import time
import math 
import Startsequenz
import ServoLenkung
import MotorAnsteuerung



def LenkRichtung(Lenkung, VelocityNormal):
    if Lenkung == 'LINKS':
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()

        winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   # Berechnet Winkel zum links fahren
        winkel_gerundet = round(winkel) + 25                      # Rundet winkel hoch
        ServoLenkung.set_angle(1, winkel_gerundet)                # setzt den Winkel von dem Servo fuer die Lenkung
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)             # faehrt bisschen langsamer weiter als davor

        if distanceLinks < 35:                                    # Wenn die Entfernung links zu klein wird lenkt er nach rechts
            ServoLenkung.set_angle(1,0)
        if distanceRechts < 25:                                   # Wenn die Entfernung rechts zu klein wird lenkt er nach links
            ServoLenkung.set_angle(1,180)

    elif Lenkung == 'RECHTS':
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()

        winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90   # Winkel zum rechts fahren wird berechnet
        winkel_gerundet = round(winkel) + 30                      # Winkel wird gerundet
        ServoLenkung.set_angle(1, winkel_gerundet)                # Winkel von dem Servo fuer die Lenkung wird gesetzt
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)             # faehrt bisschen langsamer weiter

        if distanceLinks < 25:                                    # Checkt die Enternung Links und Rechts
            ServoLenkung.set_angle(1,0)                          # Lenkt rechts wenn links die Entfernung zu klein wird
        if distanceRechts < 35:                                   
            ServoLenkung.set_angle(1,180) 