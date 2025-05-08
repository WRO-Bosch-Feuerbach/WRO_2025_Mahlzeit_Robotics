import ServoLenkung
import MotorAnsteuerung
import Ultraschallsensor
import time
import BlockColorDetection

#----------------------------- Variablen -----------------------------#

#VelocityBackwards = -0.5
#distanceHinten = Ultraschallsensor.checkdistHinten()
#distanceLinks = Ultraschallsensor.checkdistLinks()
#distanceRechts = Ultraschallsensor.checkdistRechts()

#---------------------------------------------------------------------#



def Kursanp_LinksFahren(VelocitySlow):
    VelocityBackwards = -0.5
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    while distanceHinten > 30:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 30 < distanceHinten < 50 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 50 < distanceHinten < 90 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 50)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 90 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 20)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwaerts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
    if distanceGerade < 110:
        print("Wand vor mir")
        ServoLenkung.set_angle(1, 30)
        MotorAnsteuerung.Motor_Fahren(VelocitySlow)
        time.sleep(1.5)


def Kursanp_RechtsFahren(VelocitySlow):
    VelocityBackwards = -0.5
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    while distanceHinten > 30:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 30 < distanceHinten < 50 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 50 < distanceHinten < 90 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 130)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 90 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 160)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwaerts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
    if distanceGerade < 110:
        print("Wand vor mir")
        ServoLenkung.set_angle(1, 150)
        MotorAnsteuerung.Motor_Fahren(VelocitySlow)
        time.sleep(1.5)

def Kursanp_Fahren2_0(VelocitySlow):
    VelocityBackwards = -0.4
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    pixel_count = BlockColorDetection.KursanpassungFrameInnen()
    while pixel_count < 275:
        pixel_count = BlockColorDetection.KursanpassungFrameInnen()
        pixel_countLeft = BlockColorDetection.SplitscreenLeft()
        pixel_countRight = BlockColorDetection.SplitscreenRight()
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if pixel_countLeft > pixel_countRight:
            ServoLenkung.set_angle(1, 35)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        elif pixel_countRight > pixel_countLeft:
            ServoLenkung.set_angle(1, 145)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        elif pixel_countLeft or pixel_countRight == 0:
            break
        if distanceHinten < 15:
            break


def Kursanp_LinksFahren2_0(VelocitySlow):
    VelocityBackwards = -0.4
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    while pixel_count < 275:
        pixel_count = BlockColorDetection.KursanpassungFrameInnen()
        pixel_countLeft = BlockColorDetection.SplitscreenLeft()
        pixel_countRight = BlockColorDetection.SplitscreenRight()
        if pixel_countLeft > pixel_countRight:
            ServoLenkung.set_angle(1, 35)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        elif pixel_countRight > pixel_countLeft:
            ServoLenkung.set_angle(1, 145)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        elif pixel_countLeft or pixel_countRight == 0:
            break
