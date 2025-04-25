#from encodings.punycode import T
import math
import time
import DebugBuzzer
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
VelocityObstacle = 0.25
VelocityBackwards = -0.5
#---------------- Drive related Variables ----------------#
FahrenLinks = False
FahrenRechts = False

try:

    #making sure the servo is set straight and motor is not driving
    ServoLenkung.set_angle(1, 100)
    MotorAnsteuerung.Motor_Fahren(VelocityBegin)
    #Start-Sequence --> drive forward and check in which direction the robot has to drive, after that drive backwards, so the roboter can get the curve easily
    while True:
        print('Start-Sequenz eingeleitet')
        MotorAnsteuerung.Motor_Fahren(VelocityBegin)
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceHinten = Ultraschallsensor.checkdistHinten()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        if distanceGerade <= 40:
            MotorAnsteuerung.Motor_Fahren(0)
            distanceLinks = Ultraschallsensor.checkdistLinks()
            distanceRechts = Ultraschallsensor.checkdistRechts()
            if distanceLinks > distanceRechts:
                FahrenLinks = True
                FahrenRechts = False
                print('Ich fahre Links')
            if distanceRechts > distanceLinks:
                FahrenLinks = False
                FahrenRechts = True
                print('Ich fahre rechts')

            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
            Lenkung = True
            time.sleep(2)
            break #Start-Sequence is done

    # <---- Driving Section
    while Lenkung == True:
        ServoLenkung.set_angle(1, 90)
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)
        distanceRechts = Ultraschallsensor.checkdistRechts()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceGerade = Ultraschallsensor.checkdistGerade()

        if distanceGerade <= 100:
            if FahrenLinks == True:
                angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
                angle_rounded = round(angle) + 20
                #print(angle_rounded)
                ServoLenkung.set_angle(1,angle_rounded)
            elif FahrenRechts == True:
                angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
                angle_rounded = round(angle) + 20
                #print(angle_rounded)
                ServoLenkung.set_angle(1, angle_rounded)

        if distanceRechts <= 30 and distanceLinks > distanceRechts:
            MotorAnsteuerung.Motor_Fahren(VelocityNormal - 0.05)
            ServoLenkung.set_angle(1, 155)
        if distanceLinks <= 30 and distanceLinks < distanceRechts:
            MotorAnsteuerung.Motor_Fahren(VelocityNormal - 0.05)
            ServoLenkung.set_angle(1, 25)

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
            print(CrossedSection)
            DebugBuzzer.DebugSound(0.3)

        if CrossedSection == 12:
            while not (100 < distanceGerade < 150):
                print('Debug 9')
                distanceGerade = Ultraschallsensor.checkdistGerade()
                distanceLinks = Ultraschallsensor.checkdistLinks()
                distanceRechts = Ultraschallsensor.checkdistRechts()
                if distanceLinks <= 35:
                    ServoLenkung.set_angle(1,25)
                if distanceRechts <= 35:
                    ServoLenkung.set_angle(1,155)
                if FahrenLinks == True:
                    angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
                    angle_rounded = round(angle) + 10
                elif FahrenRechts == True:
                    angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
                    angle_rounded = round(angle) + 10
                print(angle_rounded)
                ServoLenkung.set_angle(1, angle_rounded)

            break
    MotorAnsteuerung.Motor_Fahren(0)	

except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)





