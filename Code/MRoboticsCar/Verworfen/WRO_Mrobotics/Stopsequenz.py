import MotorAnsteuerung
import Ultraschallsensor
import Richtung

def Anhalten(VelocityNormal):

    while distanceGerade < 100 and distanceGerade > 150:            # Roboter soll am ende noch solange fahren bis er mittig ist
        distanceGerade = Ultraschallsensor.checkdistGerade()        # checkt die Distanz nach vorne 
        MotorAnsteuerung.Motor_Fahren(VelocityNormal)               # fährt mit normaler Geschwindigkeit
        Richtung.LenkRichtung                                       # guckt trotzdem noch nach den Seiten
 

    MotorAnsteuerung.Motor_Fahren(0)                                # bleibt stehen wenn der Roboter mittig steht