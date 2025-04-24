import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import RPi.GPIO as GPIO
import time

#--------------------------------- erste Methode zur Ansteuerung ---------------------------------
# Initialisiere I2C
i2c = busio.I2C(SCL, SDA)

# PCA9685 Initialisieren
pca = PCA9685(i2c, address=0x5f)
pca.frequency = 50  # Standartwert fuer Servos

# Funktion zum Setzen des Winkels
def set_angle(ID, angle):
    # min und max Winkel definieren
    angle = max(0, min(angle, 180))
    
    duty_cycle = (angle/180) * 5 + 5

    pulse_value = int((duty_cycle/100) * 65535)

    pca.channels[ID].duty_cycle = pulse_value
    # Servoinstanz wird erstellt
    #servo_angle = servo.Servo(pca.channels[ID], min_pulse=1000, max_pulse=2000, actuation_range=180)
    #servo_angle.angle = angle  # Winkel wird gesetzt

#--------------------------------- zweite Methode zur Ansteuerung ---------------------------------#

# GPIO-Pin definieren
servo_pin = 17

# GPIO-Modus einstellen
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50) # PWM mit einer Frequenz von 50 Hz
pwm.start(0)  # Initialisiere PWM mit 0% Duty Cycle (Servo wird nicht bewegt)

def set_servo_angle(angle):
    # Berechne die Pulsbreite fuer den gewuenschten Winkel
    pulse_width = (angle / 18) + 2  # Dies entspricht der Pulsbreite in ms
    duty_cycle = (pulse_width / 20) * 100  # Berechne den Duty Cycle in %
    pwm.ChangeDutyCycle(duty_cycle)  # Setze den Duty Cycle fuer den Servo

if __name__ == "__main__":
  while True:
    set_angle(1, 90)
