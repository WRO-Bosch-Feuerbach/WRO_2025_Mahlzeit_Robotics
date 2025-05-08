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
WallRight = 45
WallLeft = 45
#---------------- Velocity Variables ----------------#
VelocityBegin = 0.4
VelocityNormal = 0.3
VelocityObstacle = 0.25
VelocityBackwards = -0.5
VelocitySlow = 0.2
#---------------- Drive related Variables ----------------#
FahrenLinks = False
FahrenRechts = False
#---------------- Obstacle Variables ----------------#
pixel_count = 0



try:

    #making sure the servo is set straight and motor is not driving
    ServoLenkung.set_angle(1, 100)
    MotorAnsteuerung.Motor_Fahren(0)
    #Start-Sequence --> drive forward and check in which direction the robot has to drive, after that drive backwards, so the roboter can get the curve easily
    while True:
        print('Start-Sequenz eingeleitet')
        MotorAnsteuerung.Motor_Fahren(VelocityBegin)
        distanceGerade = Ultraschallsensor.checkdistGerade()
        distanceHinten = Ultraschallsensor.checkdistHinten()
        distanceLinks = Ultraschallsensor.checkdistLinks()
        distanceRechts = Ultraschallsensor.checkdistRechts()
        if distanceGerade <= 60:
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
            time.sleep(1)
            break #Start-Sequence is done

    # <---- Driving Section
    while Lenkung == True:
        
      MotorAnsteuerung.Motor_Fahren(VelocityNormal)
      distanceRechts = Ultraschallsensor.checkdistRechts()
      distanceLinks = Ultraschallsensor.checkdistLinks()
      distanceGerade = Ultraschallsensor.checkdistGerade()
      BlockColor = BlockColorDetection.Blockfarbe()
      pixel_count = BlockColorDetection.PixelCount()

      if BlockColor != "GRUEN" and BlockColor != "ROT":
          if FahrenLinks == True and distanceGerade <= 100:
              angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
              angle_rounded = round(angle) + 20
              print(angle_rounded)
              ServoLenkung.set_angle(1,angle_rounded)

          elif FahrenRechts == True and distanceGerade <= 100:
              angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
              angle_rounded = round(angle) + 20
              print(angle_rounded)
              ServoLenkung.set_angle(1, angle_rounded)
      else:
        ServoLenkung.set_angle(1, 90)

      if distanceRechts <= 40:
          MotorAnsteuerung.Motor_Fahren(VelocityNormal - 0.05)
          ServoLenkung.set_angle(1, 160)
          time.sleep(0.1)
      if distanceLinks <= 40:
          MotorAnsteuerung.Motor_Fahren(VelocityNormal - 0.05)
          ServoLenkung.set_angle(1, 20)
          time.sleep(0.1)

      if distanceGerade < 30 and BlockColor != "GRUEN" and BlockColor != "ROT" and distanceHinten >= 15:
        MotorAnsteuerung.Motor_Fahren(0)
        ServoLenkung.set_angle(1, 100)
        time.sleep(0.5)
        MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
        time.sleep(0.7)

      if BlockColor == "ROT" and pixel_count > 1000:
        while distanceRechts > 20 and distanceGerade > 20:
          pixel_count = BlockColorDetection.PixelCount()
          distanceGerade = Ultraschallsensor.checkdistGerade()
          distanceRechts = Ultraschallsensor.checkdistRechts()
          distanceHinten = Ultraschallsensor.checkdistHinten()
          ServoLenkung.set_angle(1, 30)
          if pixel_count > 9000 and distanceHinten > 20:
              print("Bin drin in der Schleife")
              MotorAnsteuerung.Motor_Fahren(0)
              ServoLenkung.set_angle(1, 100)
              time.sleep(0.5)
              MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
              time.sleep(0.7)
              break

      if BlockColor == "GRUEN" and pixel_count > 1000:
        while distanceLinks > 20 and distanceGerade > 20:
          pixel_count = BlockColorDetection.PixelCount()
          distanceGerade = Ultraschallsensor.checkdistGerade()
          distanceLinks = Ultraschallsensor.checkdistLinks()
          distanceHinten = Ultraschallsensor.checkdistHinten()
          ServoLenkung.set_angle(1, 150)
          if pixel_count > 9000 and distanceHinten > 20:
              print("Bin drin in das Schleife")
              MotorAnsteuerung.Motor_Fahren(0)
              ServoLenkung.set_angle(1, 100)
              time.sleep(0.5)
              MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
              time.sleep(0.7)
              break

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
          CrossedLinesOrange = CrossedLinesOrange +1
          DebugBuzzer.DebugSound(0.2)
          if FahrenRechts == True and CrossedLinesOrange == 1:
              #MotorAnsteuerung.Motor_Fahren(0)
              #ServoLenkung.set_angle(1, 130)
              #time.sleep(0.5)
              #MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
              #time.sleep(1)
              #Kursanpassung.Kursanp_Fahren2_0(VelocitySlow)
              print("Kursanpassung rechts")
          print("Orange Line wurde erhoeht")
          LineBeginOrange = False
      if CrossedLinesOrange == 2:
          CrossedLinesOrange = 1

      if LineBeginBlue == True and BackgroundColor == True:
          CrossedLinesBlue = CrossedLinesBlue + 1
          DebugBuzzer.DebugSound(0.2)
          if FahrenLinks == True and CrossedLinesBlue == 1:
              #MotorAnsteuerung.Motor_Fahren(0)
              #ServoLenkung.set_angle(1, 50)
              #time.sleep(0.5)
              #MotorAnsteuerung.Motor_Fahren(VelocityBackwards)
              #time.sleep(1)
              #Kursanpassung.Kursanp_Fahren2_0(VelocitySlow)
              print("Kursanpassung links")
          print("Blue Line wurde erhoeht")
          LineBeginBlue = False
      if CrossedLinesBlue == 2:
          CrossedLinesBlue = 1

      if CrossedLinesOrange + CrossedLinesBlue == 2:
          CrossedSection = CrossedSection + 1
          CrossedLinesBlue = 0
          CrossedLinesOrange = 0
          print(f'Ueberfahrene Sektionen bzw. Viertel: {CrossedSection}')
          DebugBuzzer.DebugSound(0.3)

      if CrossedSection == 12:
          while not (100 < distanceGerade < 150):
              print('Debug 9')
              distanceGerade = Ultraschallsensor.checkdistGerade()
              distanceLinks = Ultraschallsensor.checkdistLinks()
              distanceRechts = Ultraschallsensor.checkdistRechts()
              if FahrenLinks == True:
                  angle = 90 + ((200 - distanceGerade) / (200 - 5)) * 90
                  angle_rounded = round(angle) + 10
              elif FahrenRechts == True:
                  angle = 90 - ((200 - distanceGerade) / (200 - 5)) * 90
                  angle_rounded = round(angle) + 10
              print(angle_rounded)
              ServoLenkung.set_angle(1, angle_rounded)
              if distanceLinks <= 35:
                  ServoLenkung.set_angle(1,25)
              if distanceRechts <= 35:
                  ServoLenkung.set_angle(1,155)

          break

    MotorAnsteuerung.Motor_Fahren(0)

except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
