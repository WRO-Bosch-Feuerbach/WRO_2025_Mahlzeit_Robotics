import time 
from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL,SDA)
pca = PCA9685(i2c, address=0x5f)
pca.frequency = 50



def set_angle(ID, angle):
    duty_cycle = max(0, min(duty_cycle, 65535))
    servo_angle = servo.Servo(pca.channels[ID], min_pulse=500, max_pulse=2400, actuation_range=180)
    servo_angle.angle = angle

