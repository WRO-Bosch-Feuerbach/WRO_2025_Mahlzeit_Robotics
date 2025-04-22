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

#-------------------------------------------------------------------- Start Sequenz + Linienerkennung --------------------------------------------------------------------#

try:

    #----------Startsequenz um zu schauen in welche Richtung der Roboter fahren muss----------#

    while True:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        ServoLenkung.set_angle(1,100)                            
        MotorAnsteuerung.Motor_Fahren(VelocityBegin)              

        if distanceGerade < 40:                                   
            MotorAnsteuerung.Motor_Fahren(0)
            time.sleep(2)
        if distanceLinks > distanceRechts:                      
            FahrenLinks = True
            FahrenRechts = False
        else:                                                   
            FahrenRechts = True
            FahrenLinks = False
        
        MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        time.sleep(2)
        break                                                   
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #----------------------------------------------------- Fahren Links + Linienerkennung + Hindernisserkennung + Kursanpassung -------------------------------------------------#

    #---------------------------------------- FahrenLinks-Schleife --------------------------------------------#

    while FahrenLinks == True:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   
        winkel_gerundet = round(winkel) + 25                      
        ServoLenkung.set_angle(1, winkel_gerundet)                
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)             
        if distanceLinks < 35:                                    
            ServoLenkung.set_angle(1,0)
        if distanceRechts < 25:                                   
            ServoLenkung.set_angle(1,180)

      

        #-------- Farberkennung für Hindernisse ----------#

        while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:         
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            Farbe = 'Rot'
            Buzzer.DebugSound(0.1)
            MotorAnsteuerung.Motor_Fahren(VelocityObstacle)                      
            ServoLenkung.set_angle(1,10)                                 
        if distanceLinks < 25:                                          
            ServoLenkung.set_angle(1,0)                                  
        if distanceRechts < 25:                                          
            ServoLenkung.set_angle(1,180)                                

        BlockColorDetection.Blockfarbe()                        
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

        while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:      
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            Farbe = 'Grün'
            Buzzer.DebugSound(0.1)
            MotorAnsteuerung.Motor_Fahren(VelocityObstacle)        
            ServoLenkung.set_angle(1,170)                                  

        if distanceLinks < 25:                                  
            ServoLenkung.set_angle(1,0)                                  
        if distanceRechts < 25:                                 
            ServoLenkung.set_angle(1,180)                               

        BlockColorDetection.Blockfarbe()                        
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

        #---------- Farberkennung Bodenlinien ----------#

        DetectedColor = CameraColorDetection2.ColorDetection2_0()

        if DetectedColor == "ORANGE":                             
            LineDetected = True                                    
        if LineDetected == True:                                
            LineDetected = False                                  
            LineBeginOrange = True                               
            BackgroundColor = False                              
        elif DetectedColor == "BLUE":                             
            LineDetected = True                                     
        if LineDetected == True:                                
            #RouteCorrection = True
            LineDetected = False                                  
            LineBeginBlue = True                                  
            BackgroundColor = False                               
        else:                                                    
            BackgroundColor = True                                  
            LineDetected = False                                    

        if LineBeginOrange == True and BackgroundColor == True:   
            CrossedLinesOrange = CrossedLinesOrange + 1            
            LineBeginOrange = False                                 
            Buzzer.DebugSound(0.2)
        if CrossedLinesOrange == 2:
            CrossedLinesOrange = 1
        

        if LineBeginBlue == True and BackgroundColor == True:
            CrossedLinesBlue = CrossedLinesBlue + 1               
            LineBeginBlue = False                                   
        #RouteCorrection = True
        Buzzer.DebugSound(0.2)

        #-------------- Kursanpassen ---------------#
        #Kursanpassung.Kursanp_LinksFahren()

        if CrossedLinesOrange + CrossedLinesBlue == 2:            
            CrossedSection = CrossedSection + 1                    
            CrossedLinesBlue = 0                                   
            CrossedLinesOrange = 0
            Buzzer.DebugSound(0.3)

        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')
        if CrossedSection == 12:                                  
            while distanceGerade < 100 and distanceGerade > 150:
                distanceGerade = Ultraschallsensor.checkdistGerade()
                distanceLinks = Ultraschallsensor.checkdistLinks()
                distanceRechts = Ultraschallsensor.checkdistRechts()
            winkel = 90 + ((200 - distanceGerade) / (200 - 5)) * 90   
            winkel_gerundet = round(winkel) + 25                     
            ServoLenkung.set_angle(1, winkel_gerundet)                      
            MotorAnsteuerung.Motor_Fahren(VelocityNormal)            
            if distanceLinks < 30:                                    
                ServoLenkung.set_angle(1,20)
            if distanceRechts < 30:                                 
                ServoLenkung.set_angle(1,170)
          
        break                                                       

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #----------------------------------------------------- Fahren Rechts + Linienerkennung + Hindernisserkennung + Kursanpassung -------------------------------------------------#

    #---------- FahrenRechts-Schleife ----------#

    while FahrenRechts == True:
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90  
        winkel_gerundet = round(winkel) + 30                     
        ServoLenkung.set_angle(1, winkel_gerundet)                      
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)            
        if distanceLinks < 25:                                   
           ServoLenkung.set_angle(1,0)                                  
        if distanceRechts < 35:                                  
            ServoLenkung.set_angle(1,180)

        #----------- Farberkennung Hindernisse ----------#      

        while BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 100:
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            Farbe = 'Rot'
            Buzzer.DebugSound(0.1)
            MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
            ServoLenkung.set_angle(1,10)
            if distanceLinks < 25:
                ServoLenkung.set_angle(1,0)
            if distanceRechts < 25:
                ServoLenkung.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')



        while BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 100:
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            Farbe ='Grün'
            Buzzer.DebugSound(0.1)
            MotorAnsteuerung.Motor_Fahren(VelocityObstacle)
            ServoLenkung.set_angle(1,170)
            if distanceLinks < 25:
                ServoLenkung.set_angle(1,0)
            if distanceRechts < 25:
                ServoLenkung.set_angle(1,180)

        BlockColorDetection.Blockfarbe()
        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')

        #---------- Farberkennung Bodenlinien ----------#   Siehe Erklarrung FahrenLinks-Schleife

        DetectedColor = CameraColorDetection2.ColorDetection2_0()

        if DetectedColor == "ORANGE":                            
            LineDetected = True                                     
        if LineDetected == True:                                
            RouteCorrection = True
            LineDetected = False                                  
            LineBeginOrange = True                                
            BackgroundColor = False                               
        elif DetectedColor == "BLUE":                             
            LineDetected = True                                     
        if LineDetected == True:                               
            LineDetected = False                                  
            LineBeginBlue = True                                  
            BackgroundColor = False                               
        else:                                                     
            BackgroundColor = True                                  
            LineDetected = False                                    

        if LineBeginOrange == True and BackgroundColor == True:   
            CrossedLinesOrange = CrossedLinesOrange + 1             
            LineBeginOrange = False                                 
            #RouteCorrection = True
            Buzzer.DebugSound(0.2)
        
        #-------------- Kursanpassen ---------------#
        #Kursanpassung.Kursanp_RechtsFahren()

        if LineBeginBlue == True and BackgroundColor == True:     
            CrossedLinesBlue = CrossedLinesBlue + 1                 
            LineBeginBlue = False                                  
            Buzzer.DebugSound(0.2)
        if CrossedLinesBlue == 2:
            CrossedLinesBlue = 1

        if CrossedLinesOrange + CrossedLinesBlue == 2:            
            CrossedSection = CrossedSection + 1                     
            CrossedLinesBlue = 0                                    
            CrossedLinesOrange = 0
            Buzzer.DebugSound(0.3)

        print(f'\rHindernis Farbe: {Farbe};     Linien überquert: {CrossedLinesOrange + CrossedLinesBlue};     Sektionen durchfahren: {CrossedSection}', end='')
        if CrossedSection == 12:                                  
            while distanceGerade < 100 and distanceGerade > 150:
                distanceGerade = Ultraschallsensor.checkdistGerade()
                distanceLinks = Ultraschallsensor.checkdistLinks()
                distanceRechts = Ultraschallsensor.checkdistRechts()
            winkel = 90 - ((200 - distanceGerade) / (200 - 5)) * 90  
            winkel_gerundet = round(winkel) + 30                     
            ServoLenkung.set_angle(1, winkel_gerundet)                      
            MotorAnsteuerung.Motor_Fahren(VelocityNormal)                      
            if distanceLinks < 30:                                   
                ServoLenkung.set_angle(1,20)                                  
            if distanceRechts < 30:                                  
                ServoLenkung.set_angle(1,170) 

        break

    MotorAnsteuerung.Motor_Fahren(0)

except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    ServoLenkung.set_angle(1,90)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
