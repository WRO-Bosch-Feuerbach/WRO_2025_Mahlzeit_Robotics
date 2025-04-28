from Funktionen.BrummBrummAutonom import VelocityNormal
import ServoLenkung
import MotorAnsteuerung
import Ultraschallsensor
import time

#----------------------------- Variablen -----------------------------#

#VelocityBackwards = -0.5
#distanceHinten = Ultraschallsensor.checkdistHinten()
#distanceLinks = Ultraschallsensor.checkdistLinks()
#distanceRechts = Ultraschallsensor.checkdistRechts()

#---------------------------------------------------------------------#



def Kursanp_LinksFahren():
    VelocityBackwards = -0.5
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    while distanceHinten > 30:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 30 < distanceHinten < 40 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 40 < distanceHinten < 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 60)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 30)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwaerts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
    if distanceGerade < 130:
        ServoLenkung.set_angle(1, 110)
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)
        time.sleep(0.2)


def Kursanp_RechtsFahren():
    VelocityBackwards = -0.5
    distanceHinten = Ultraschallsensor.checkdistHinten()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()
    distanceGerade = Ultraschallsensor.checkdistGerade()
    #---------- Kurs anpassen ----------#
    while distanceHinten > 30:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 30 < distanceHinten < 40 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 40 < distanceHinten < 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 120)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 150)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwaerts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
    if distanceGerade < 130:
        ServoLenkung.set_angle(1, 70)
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)
        time.sleep(0.2)