import Startsequenz
import Richtung
import Farberkennung
import Stopsequenz
from encodings.punycode import T
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import MotorAnsteuerung

#-------------------- Variablen --------------------#

Lenkung = ''
VelocityBegin = 0.4
VelocityNormal = 0.35
VelocityObstacle = 0.3
VelocityBackwards = -0.4

#---------------------------------------------------#

#-------------------- Losfahren --------------------#

Lenkung = Startsequenz.Losfahren(VelocityBegin, VelocityBackwards)

#---------------------------------------------------#
#-------------------- Rundenfahren, Farberkennung Bodenlinie & Hindernis --------------------#
while True:
    MotorAnsteuerung.Motor_Fahren(VelocityNormal)                                                      
    Farberkennung.HindernisBlock(VelocityObstacle)
    Farberkennung.Bodenlinie()
    if Farberkennung.Bodenlinie == True:
        break
    Richtung.LenkRichtung(Lenkung, VelocityNormal)
#--------------------------------------------------------------------------------------------#

#-------------------- Anhalten --------------------# 
Stopsequenz.Anhalten(VelocityNormal)
