import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import RPIservo

MOTOR_M1_IN1 = 15
MOTOR_M1_IN2 = 14

Dir_forward = 0
Dir_backward = 1

left_forward = 1
left_backward = 0

right_forward = 0
right_backward = 1

pwn_A = 0
pwm_B = 0

sc =  RPIservo.ServoCtrl()
sc.start()


def map(x,in_min,in_max,out_min,out_max):
  return(x-in_min)/(in_max-in_min)*(out_max-out_min)+out_min


i2c = busio.I2C(SCL, SDA)
pwm_motor = PCA9685(i2c, address=0x5f)
pwm_motor.frequency = 1000

motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1], pwm_motor.channels[MOTOR_M1_IN2])
motor1.decay_mode = (motor.SLOW_DECAY)

def Motor(channel,direction,motor_speed):
  if motor_speed > 100:
    motor_speed = 100
  elif motor_speed < 0:
    motor_speed = 0
  speed = map(motor_speed, 0, 100, 0, 1.0)
  if direction == -1:
    speed = -speed

  if channel == 1:
    motor1.throttle = speed

def motorStop():
    motor1.throttle = 0

def destroy():
  motorStop()
  pwm_motor.deinit()


if __name__ == '__main__':
  try:
    chann = 1
    for i in range(10):
      speed_set = 110

      sc.singleServo(0, -1, 10)
      time.sleep(1)
      Motor(chann, 1, speed_set)
      time.sleep(2)

      sc.singleServo(0, 1, 10)
      time.sleep(1)
      Motor(chann, -1, speed_set)
      time.sleep(2)
    destroy()

  except KeyboardInterrupt:
    print("KeyBoard Interrupt desroy!")
    destroy()
