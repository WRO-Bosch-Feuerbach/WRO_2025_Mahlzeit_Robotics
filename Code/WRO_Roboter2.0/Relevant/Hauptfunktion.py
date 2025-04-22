from encodings.punycode import T
import math
import time
import Buzzer
import Kursanpassung
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import ServoLenkung
import CameraColorDetection2
import BlockColorDetection
import Startsequenz
import Fahren_Richtung

#--------------------------------------- Variablen ---------------------------------------#
OrangeLine = False
BlueLine = False
Line1 = False
Line2 = False
CrossedOrangeLines = 0
CrossedLinesOrange = 0
CrossedLinesBlue = 0
LineDetected = False
LineBeginOrange = False
LineBeginBlue = False
BackgroundColor = False
distanceGerade = Ultraschallsensor.checkdistGerade()
distanceLinks = Ultraschallsensor.checkdistLinks()
distanceRechts = Ultraschallsensor.checkdistRechts()
distanceHinten = Ultraschallsensor.checkdistHinten()
DetectedColor = CameraColorDetection2.ColorDetection2_0()
Farbe = ''
CrossedSection = 0
RoundCounter = 0
VelocityBegin = 0.4
VelocityNormal = 0.35
VelocityObstacle = 0.35
VelocityBackwards = -0.5
RouteCorrection = False
#-----------------------------------------------------------------------------------------#

#--------------------------------------- Startsequenz ausf�hren und Richtungsvorgabe ---------------------------------------#

Lenkung = Startsequenz.Startsequenz()

#------------------------------------------------------ Fahren Links -------------------------------------------------------#
while Lenkung == "LINKS":
    Fahren_Richtung.Links()

    #---------------------- Farberkennung Bodenlinien ----------------------#

    DetectedColor = CameraColorDetection2.ColorDetection2_0()

    if DetectedColor == "ORANGE":                                                       # Checkt ob Farbe orange ist
        LineDetected = True                                                             # Erste Linie wird erkannt
    if LineDetected == True:                                    
        LineDetected = False                                                            # Wird direkt wieder auf False gesetzt um die Zweite Linie wieder zu erkennen
        LineBeginOrange = True                                                          # Wird auf True gesetzt damit Linie erst wieder erkannt werden kann nach dem man dar�ber gefahren ist
        BackgroundColor = False                                                         # Background ist die wei�e Bahn fl�che
    elif DetectedColor == "BLUE":                                                       # Das gleiche wie bei orange f�r Farbe Blau
        LineDetected = True 
    if LineDetected == True:                                  
        LineDetected = False                                  
        LineBeginBlue = True                                  
        BackgroundColor = False                               
    else:                                                                               # Default ist das der Boden wei� ist und keine Linie erkannt wurde
        BackgroundColor = True                                
        LineDetected = False                                  

    if LineBeginOrange == True and BackgroundColor == True:                             # Wenn vorher eine Linie erkannt wurde und der Boden wieder wei� ist -> Linie komplett �berfahren
        CrossedLinesOrange = CrossedLinesOrange + 1                                     # Liniencounter wirdhochgez�hlt
        LineBeginOrange = False                                                         # LineBegin wieder auf False f�r die n�chste Linie
        Buzzer.DebugSound(0.2)
    if CrossedLinesOrange == 2:
        CrossedLinesOrange = 1
        
    if LineBeginBlue == True and BackgroundColor == True:                               # Wenn vorher eine Linie erkannt wurde und der Boden wieder wei� ist -> Linie komplett �berfahren
        CrossedLinesBlue = CrossedLinesBlue + 1                                         # Liniencounter wirdhochgez�hlt
        LineBeginBlue = False                                                           # LineBegin wieder auf False f�r die n�chste Linie
        Buzzer.DebugSound(0.2)
   
        #---------- Kurs anpassen ----------#
        Kursanpassung.Kursanp_LinksFahren()
        
    if CrossedLinesOrange + CrossedLinesBlue == 2:                                      # 2 Linien sind eine Ecke bzw. 1/4
        CrossedSection = CrossedSection + 1                                             # 1/4 ist 1 Sektion
        CrossedLinesBlue = 0                                                            # �berquerte Linien wieder auf 0 um die n�chste Sektion zu pr�fen
        CrossedLinesOrange = 0
        Buzzer.DebugSound(0.3)

    if CrossedSection == 12:                                                            # Bei 12 �berquerten Sektionen sind 3 Runden durchfahren
        while distanceGerade < 100 and distanceGerade > 150:
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            if distanceLinks < 30:                                                      # Wenn die Entfernung links zu klein wird lenkt er nach rechts
                ServoLenkung.set_angle(1,20)
            if distanceRechts < 30:                                                     # Wenn die Entfernung rechts zu klein wird lenkt er nach links
                ServoLenkung.set_angle(1,170)
                winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90                 # Berechnet Winkel zum links fahen
                winkel_gerundet = round(winkel) + 25                                    # Rundet winkel hoch
                ServoLenkung.set_angle(1, winkel_gerundet)                                     # setzt den Winkel von dem Servo f�r die Lenkung
                MotorAnsteuerung.Motor_Fahren(VelocityNormal)                           # f�hrt bisschen langsamer weiter als davor

          
            break                                                                       # Aus der Schleife springen bzw. Programm ist danach Ende 

    #---------------------- Farberkennung Hindernisse ----------------------#

    while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Rot'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
        ServoLenkung.set_angle(1,10)
        if distanceLinks < 18:
            ServoLenkung.set_angle(1,0)
        if distanceRechts < 18:
            ServoLenkung.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien �berquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')



    while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe ='Gr�n'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
        ServoLenkung.set_angle(1,170)
        if distanceLinks < 18:
            ServoLenkung.set_angle(1,0)
        if distanceRechts < 18:
            ServoLenkung.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien �berquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

#----------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------ Fahren Rechts -------------------------------------------------------#
while Lenkung == "RECHTS":
    Fahren_Richtung.Rechts(Lenkung)

    #---------------------- Farberkennung Bodenlinien ----------------------#

    DetectedColor = CameraColorDetection2.ColorDetection2_0()

    if DetectedColor == "ORANGE":                                                       # Checkt ob Farbe orange ist
        LineDetected = True                                                             # Erste Linie wird erkannt
    if LineDetected == True:                                
        RouteCorrection = True
        LineDetected = False                                                            # Wird direkt wieder auf False gesetzt um die Zweite Linie wieder zu erkennen
        LineBeginOrange = True                                                          # Wird auf True gesetzt damit Linie erst wieder erkannt werden kann nach dem man dar�ber gefahren ist
        BackgroundColor = False                                                         # Background ist die wei�e Bahn fl�che
    elif DetectedColor == "BLUE":                                                       # Das gleiche wie bei orange f�r Farbe Blau
        LineDetected = True                                     
    if LineDetected == True:                                
        LineDetected = False                                  
        LineBeginBlue = True                                  
        BackgroundColor = False                               
    else:                                                                               # Default ist das der Boden wei� ist und keine Linie erkannt wurde
        BackgroundColor = True                                  
        LineDetected = False                                    

    if LineBeginOrange == True and BackgroundColor == True:                             # Wenn vorher eine Linie erkannt wurde und der Boden wieder wei� ist -> Linie komplett �berfahren
        CrossedLinesOrange = CrossedLinesOrange + 1                                     # Liniencounter wirdhochgez�hlt
        LineBeginOrange = False                                                         # LineBegin wieder auf False f�r die n�chste Linie
        Buzzer.DebugSound(0.2)
        
        #---------- Kurs anpassen ----------#
        Kursanpassung.Kursanp_RechtsFahren()
        

    if LineBeginBlue == True and BackgroundColor == True:                               # Wenn vorher eine Linie erkannt wurde und der Boden wieder wei� ist -> Linie komplett �berfahren
        CrossedLinesBlue = CrossedLinesBlue + 1                                         # Liniencounter wirdhochgez�hlt
        LineBeginBlue = False                                                           # LineBegin wieder auf False f�r die n�chste Linie
        Buzzer.DebugSound(0.2)
    if CrossedLinesBlue == 2:
        CrossedLinesBlue = 1

    if CrossedLinesOrange + CrossedLinesBlue == 2:                                      # 2 Linien sind eine Ecke bzw. 1/4
        CrossedSection = CrossedSection + 1                                             # 1/4 ist 1 Sektion
        CrossedLinesBlue = 0                                                            # �berquerte Linien wieder auf 0 um die n�chste Sektion zu pr�fen
        CrossedLinesOrange = 0
        Buzzer.DebugSound(0.3)

    print(f'\rHindernis Farbe: {Farbe};     Linien �berquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

    if CrossedSection == 12:                                                            # Bei 12 �berquerten Sektionen sind 3 Runden durchfahren
        while distanceGerade < 100 and distanceGerade > 150:
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            if distanceLinks < 30:                                                      # Checkt die Enternung Links und Rechts
                ServoLenkung.set_angle(1,20)                                                   # Lenkt rechts wenn links die Entfernung zu klein wird
            if distanceRechts < 30:                                 
                ServoLenkung.set_angle(1,170) 
                winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90                 # Winkel zum rechts fahren wird berechnet
                winkel_gerundet = round(winkel) + 30                                    # Winkel wird gerundet
                ServoLenkung.set_angle(1, winkel_gerundet)                                     # Winkel von dem Servo f�r die Lenkung wird gesetzt
                MotorAnsteuerung.Motor_Fahren(VelocityNormal)                           # f�hrt bisschen langsamer weiter

            break

    #---------------------- Farberkennung Hindernisse ----------------------#

    while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:           # Checkt ob die Farbe rot ist
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Rot'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)                                 # Wird langsamer
        ServoLenkung.set_angle(1,10)                                                           # lenkt nach rechts

        if distanceLinks < 18:                                                          # Checkt noch die Entfernung an den Seiten
            ServoLenkung.set_angle(1,0)                                                        # lenkt nach rechts
        if distanceRechts < 18:                                 
            ServoLenkung.set_angle(1,180)                                                      # lenkt nach links

        BlockColorDetection.Blockfarbe()                                                # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben
        print(f'\rHindernis Farbe: {Farbe};     Linien �berquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

    while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:         # Checkt ob Farbe gr�n ist
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Gr�n'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)                                 # Wird langsamer
        test2.set_angle(1,170)                                                          # lenkt nach links

        if distanceLinks < 18:                                                          # Checkt noch die Entfernung an den Seiten
            ServoLenkung.set_angle(1,0)                                                        # lenkt nach rechts
        if distanceRechts < 18:                                 
            ServoLenkung.set_angle(1,180)                                                      # lenkt nach links

        BlockColorDetection.Blockfarbe()                                                # Checkt nochmal nach der Farbe um nicht in der Schleife gefangen zu bleiben
        print(f'\rHindernis Farbe: {Farbe};     Linien �berquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

    #----------------------------------------------------------------------------------------------------------------------------#