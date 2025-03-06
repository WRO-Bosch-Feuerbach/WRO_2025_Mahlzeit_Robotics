import dis
from gpiozero import DistanceSensor, Servo
from time import sleep

Tr = 2
Ec = 3

sensor = DistanceSensor(echo=Ec, trigger=Tr,max_distance=2) # Maximum detection distance 2m.

# Get the distance of ultrasonic detection.
def checkdist():
    return (sensor.distance) *100 # Unit: cm

if __name__ == "__main__":
    while True:
        distance = checkdist()
        print("%.2f cm" %distance)
        sleep(0.05)
