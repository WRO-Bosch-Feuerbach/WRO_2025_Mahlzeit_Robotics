import dis
from gpiozero import DistanceSensor, Servo
import time


Tr1 = 23
Ec1 = 24
sensor1 = DistanceSensor(echo=Ec1, trigger=Tr1, max_distance=2)

Tr2 = 17
Ec2 = 27
sensor2 = DistanceSensor(echo=Ec2, trigger=Tr2, max_distance=2)


Tr3 = 14
Ec3 = 15
sensor3 = DistanceSensor(echo=Ec3, trigger=Tr3, max_distance=2)

Tr4 = 22
Ec4 = 6
sensor4 = DistanceSensor(echo=Ec4, trigger=Tr4, max_distance=2)


def checkdistGerade():
  return (sensor1.distance) * 100

def checkdistRechts():
  return (sensor2.distance) * 100

def checkdistLinks():
  return (sensor3.distance) * 100

def checkdistHinten():
  return (sensor4.distance) * 100


if __name__ == "__main__":

  while True:
    time.sleep(0.1)
    #print(f'{checkdistGerade()}')
    #print(f'{checkdistRechts()}')
    #print(f'{checkdistLinks()}')
    #print(f'{checkdistHinten()}')
    print(f'hinten: {checkdistHinten()} ;         vorne: {checkdistGerade()}  ;           links: {checkdistLinks()}  ;       rechts: {checkdistRechts()}')


