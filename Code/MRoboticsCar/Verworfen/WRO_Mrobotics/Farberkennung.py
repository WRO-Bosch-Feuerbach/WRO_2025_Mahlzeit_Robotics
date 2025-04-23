import CameraColorDetection2
import BlockColorDetection
import Buzzer
import MotorAnsteuerung
import ServoLenkung
import Ultraschallsensor


#-------------------- Bodenlinienerkennung --------------------#
def Bodenlinie():

    DetectedColor = CameraColorDetection2.ColorDetection2_0()
    LineDetected = False
    LineBeginOrange = False
    LineBeginBlue = False
    BackgroundColor = True
    fertig = False
    CrossedLinesOrange = 0
    CrossedLinesBlue = 0
    CrossedSection = 0

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
        Buzzer.DebugSound(0.2)
    if CrossedLinesOrange == 2:
        CrossedLinesOrange = 1

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
    
    if CrossedSection == 12:
        fertig = True
    
    return fertig 





#-------------------- Hindernisblockerkennung --------------------#
def HindernisBlock(VelocityObstacle):
    distanceGerade = Ultraschallsensor.checkdistGerade()
    distanceLinks = Ultraschallsensor.checkdistLinks()
    distanceRechts = Ultraschallsensor.checkdistRechts()

    if BlockColorDetection.Blockfarbe() == 'ROT' and distanceGerade < 80:
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

    if BlockColorDetection.Blockfarbe() == 'GRUEN' and distanceGerade < 80:      
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        Farbe = 'Gruen'
        Buzzer.DebugSound(0.1)
        MotorAnsteuerung.Motor_Fahren(VelocityObstacle)        
        ServoLenkung.set_angle(1,170)                                  
        if distanceLinks < 25:                                  
            ServoLenkung.set_angle(1,0)                                  
        if distanceRechts < 25:                                 
            ServoLenkung.set_angle(1,180)                               

        BlockColorDetection.Blockfarbe()                        
        






