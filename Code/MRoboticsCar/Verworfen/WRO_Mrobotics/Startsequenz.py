import Ultraschallsensor
import MotorAnsteuerung
import ServoLenkung
import time

#----------------------------- Variablen -----------------------------#



#---------------------------------------------------------------------#

def Losfahren(VelocityBegin, VelocityBackwards): 
    
    Lenkung = ''

    #----------Startsequenz um zu schauen in welche Richtung der Roboter fahren muss----------#

    while Lenkung != 'LINKS' and Lenkung != 'RECHTS':
      distanceGerade = Ultraschallsensor.checkdistGerade()      # checkt Distanz nach vorne
      distanceLinks = Ultraschallsensor.checkdistLinks()        # checkt Distanz nach links
      distanceRechts = Ultraschallsensor.checkdistRechts()      # checkt Distanz nach rechts

      ServoLenkung.set_angle(1,100)                             # Servo gerade stellen
      MotorAnsteuerung.Motor_Fahren(VelocityBegin)              # losfahren

      if distanceGerade < 40:                                   # Haelt an um zu pruefen ob links oder rechts mehr platz ist
        MotorAnsteuerung.Motor_Fahren(0)
        time.sleep(2)
      if distanceLinks > distanceRechts:                        # Wenn links mehr platz ist wird das Programm in die FahrenLinks-Schleife springen
        Lenkung = "LINKS"
      else:                                                     # Wenn rechts mehr platz ist wird das Programm in die FahrenRechts-Schleife springen
        Lenkung = "RECHTS"
                 
      MotorAnsteuerung.Motor_Fahren(VelocityBackwards)          # faehrt 2 Sekunden zurück um richtig loszufahren
      time.sleep(2)                                                     

      return Lenkung                                            # gibt zurück ob es Links oder Rechts runden sind