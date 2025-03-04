import dis
from gpiozero import DistanceSensor, Servo



Tr = 23
Ec = 24
sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)  


def checkdist():
    return sensor.distance * 100  



#distance = checkdist()  --> werte in distance speichern 




