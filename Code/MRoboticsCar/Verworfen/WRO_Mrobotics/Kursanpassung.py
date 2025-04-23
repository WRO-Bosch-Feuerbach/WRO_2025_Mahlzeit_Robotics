import ServoLenkung
import MotorAnsteuerung
import Ultraschallsensor
import time

#----------------------------- Variablen -----------------------------#

VelocityBackwards = -0.5
distanceHinten = Ultraschallsensor.checkdistHinten()
distanceLinks = Ultraschallsensor.checkdistLinks()
distanceRechts = Ultraschallsensor.checkdistRechts()

#---------------------------------------------------------------------#



def Kursanp_LinksFahren():

    #---------- Kurs anpassen ----------#
    while distanceHinten > 15:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 15 < distanceHinten < 40 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 40 < distanceHinten < 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 60)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 30)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwärts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)

def Kursanp_RechtsFahren():

    #---------- Kurs anpassen ----------#
    while distanceHinten > 15:
        MotorAnsteuerung.Motor_Fahren(0)
        distanceHinten = Ultraschallsensor.checkdistHinten()
        if 15 < distanceHinten < 40 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if 40 < distanceHinten < 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 120)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        if distanceHinten > 75 and distanceRechts > 5:
            ServoLenkung.set_angle(1, 150)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        #--------- Rückwärts wenn links nicht genug Platz ist ---------#
        while distanceHinten > 75 and distanceRechts < 5:
            ServoLenkung.set_angle(1, 90)
            MotorAnsteuerung.Motor_Fahren(VelocityBackwards)