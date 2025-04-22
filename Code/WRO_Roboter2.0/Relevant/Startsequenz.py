import Ultraschallsensor
import MotorAnsteuerung
import test2
import time

#----------------------------- Variablen -----------------------------#

VelocityBegin = 0.4
VelocityBackwards = -0.5
Lenkung = ''

#---------------------------------------------------------------------#

def Startsequenz():

    #----------Startsequenz um zu schauen in welche Richtung der Roboter fahren muss----------#

    while True:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        test2.set_angle(1,100)                                    # Servo gerade stellen
        MotorAnsteuerung.Motor_Fahren(VelocityBegin)              # losfahren

        if distanceGerade < 40:                                   # Hält an um zu prüfen ob links oder rechts mehr platz ist
          MotorAnsteuerung.Motor_Fahren(0)
          time.sleep(2)
        if distanceLinks > distanceRechts:                        # Wenn links mehr platz ist wird das Programm in die FahrenLinks-Schleife springen
          Lenkung = "LINKS"
          return Lenkung
        else:                                                     # Wenn rechts mehr platz ist wird das Programm in die FahrenRechts-Schleife springen
          Lenkung = "RECHTS"
          return Lenkung        
        
        MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        time.sleep(2)
        break                                                     # Bricht aus erster Schleife aus