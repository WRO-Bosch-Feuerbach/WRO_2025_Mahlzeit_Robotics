import dis
from gpiozero import DistanceSensor, Servo
import time


Tr1 = 23
Ec1 = 24
sensor1 = DistanceSensor(echo=Ec1, trigger=Tr1, max_distance=2)

Tr2 = 27
Ec2 = 17
sensor2 = DistanceSensor(echo=Ec2, trigger=Tr2, max_distance=2)


Tr3 = 14
Ec3 = 15
sensor3 = DistanceSensor(echo=Ec3, trigger=Tr3, max_distance=2)


def checkdistGerade():
  return (sensor1.distance) * 100

def checkdistLinks():
  return (sensor2.distance) * 100

def checkdistRechts():
  return (sensor3.distance) * 100


if __name__ == "__main__":

  while True:
    time.sleep(0.1)
    print(f'{checkdistLinks()}    {checkdistGerade()}    {checkdistRechts()}')

#distance = checkdist()  #-> werte in distance speichern 




