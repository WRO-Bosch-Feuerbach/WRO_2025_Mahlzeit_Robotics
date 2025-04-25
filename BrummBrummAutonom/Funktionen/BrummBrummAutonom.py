from encodings.punycode import T
import math
import time
import DebugBuzzer
from Funktionen.test_alt import fahren
import Kursanpassung
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import MotorAnsteuerung
import ServoLenkung
import CameraColorDetection
import BlockColorDetection

#--------------------------------------------------------------- Variabeln -----------------------------------------------------------------#
#---------------- Line Detection Variables ----------------#
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
CrossedSection = 0
RoundCounter = 0
#---------------- Distance from Sensor Variables ----------------#
distanceGerade = Ultraschallsensor.checkdistGerade()
distanceLinks = Ultraschallsensor.checkdistLinks()
distanceRechts = Ultraschallsensor.checkdistRechts()
distanceHinten = Ultraschallsensor.checkdistHinten()
DetectedColor = CameraColorDetection.ColorDetection2_0()
Farbe = ''
#---------------- Velocity Variables ----------------#
VelocityBegin = 0.4
VelocityNormal = 0.35
VelocityObstacle = 0.35
VelocityBackwards = -0.5

#---------------- Drive related Variables ----------------#
FahrenLinks = False
FahrenRechts = False

#making sure the servo is set straight and motor is not driving 
ServoLenkung.set_angle(1, 90)
MotorAnsteuerung.Motor_Fahren(0)

#Start-Sequence --> drive forward and check in which direction the robot has to drive, after that drive backwards, so the roboter can get the curve easily
while True: 
    MotorAnsteuerung.Motor_Fahren(VelocityBegin)
    if distanceGerade == 80:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceHinten = Ultraschallsensor.checkdistHinten()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        time.sleep(1)
        if distanceLinks > distanceRechts:
            FahrenLinks = True
            FahrenRechts = False
        if distanceRechts > distanceLinks:
            FahrenLinks = False
            FahrenRechts = True

        MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        Lenkung = True
        time.sleep(1.5)
        break #Start-Sequence is done

# <---- Driving Section
while Lenkung == True:
    MotorAnsteuerung.Motor_Fahren(VelocityNormal)
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    if distanceRechts <= 20:
        ServoLenkung.set_angle(1, 0) #
    if distanceLinks <= 20:
        ServoLenkung.set_angle(1, 180) #

    if distanceGerade <= 90:
        if FahrenLinks == True:
            angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
            angle_rounded = round(angle) + 10
        elif FahrenRechts == True:
            angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
            angle_rounded = round(angle) + 10
        print(angle_rounded)
        ServoLenkung.set_angle(1, angle_rounded)

    # Color-Line-Detection Sequence
    DetectedColor = CameraColorDetection.ColorDetection2_0()
    if DetectedColor == "ORANGE":                                                       
        LineDetected = True                                                             
        if LineDetected == True:                                    
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
        DebugBuzzer.DebugSound(0.2)
        if CrossedLinesOrange == 2:
            CrossedLinesOrange = 1
        
    if LineBeginBlue == True and BackgroundColor == True:                               
        CrossedLinesBlue = CrossedLinesBlue + 1                                         
        LineBeginBlue = False                                                           
        DebugBuzzer.DebugSound(0.2)
        if CrossedLinesBlue == 2:
            CrossedLinesBlue = 1
        
    if CrossedLinesOrange + CrossedLinesBlue == 2:                                      
        CrossedSection = CrossedSection + 1                                             
        CrossedLinesBlue = 0                                                            
        CrossedLinesOrange = 0
        DebugBuzzer.DebugSound(0.3)

    if CrossedSection == 12:                                                            
        while not(100 < distanceGerade < 150):
            distanceGerade = Ultraschallsensor.checkdistGerade()
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            if distanceLinks < 30:                                                      
                ServoLenkung.set_angle(1,20)
            if distanceRechts < 30:                                                     
                ServoLenkung.set_angle(1,170)
            if FahrenLinks == True:
                angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
                angle_rounded = round(angle) + 10
            elif FahrenRechts == True:
                angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
                angle_rounded = round(angle) + 10
            print(angle_rounded)
            ServoLenkung.set_angle(1, angle_rounded)

        break





