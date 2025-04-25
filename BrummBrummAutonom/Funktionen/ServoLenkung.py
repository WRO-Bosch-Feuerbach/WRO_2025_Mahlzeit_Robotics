import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import RPi.GPIO as GPIO
import time

#--------------------------------- erste Methode zur Ansteuerung ---------------------------------
pca = None

def init():
    global pca
    
    if pca is None:

      # Initialisiere I2C
      i2c = busio.I2C(SCL, SDA)

      # PCA9685 Initialisieren
      pca = PCA9685(i2c, address=0x5f)
      pca.frequency = 50  # Standartwert fuer Servos

# Funktion zum Setzen des Winkels
def set_angle(ID, angle):

    if pca is None:
      init()

    # min und max Winkel definieren
    angle = max(0, min(angle, 180))

    duty_cycle = (angle/180) * 5 + 5
    pulse_value = int((duty_cycle/100) * 65535)
    pca.channels[ID].duty_cycle = pulse_value
    # Servoinstanz wird erstellt
    #servo_angle = servo.Servo(pca.channels[ID], min_pulse=1000, max_pulse=2000, actuation_range=180)
    #servo_angle.angle = angle  # Winkel wird gesetzt



if __name__ == "__main__":
  while True:
    #set_angle(1, 0)
    #time.sleep(1)
    set_angle(1, 180)
    #time.sleep(1)
    #set_angle(1, 180)
    #time.sleep(1)
    #set_angle(1, 90)
    #time.sleep(1)

