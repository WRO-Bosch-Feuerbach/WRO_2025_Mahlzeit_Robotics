import math
import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import lenkung_funktion
import MotorAnsteuerung
import test2
'''
distance = Ultraschallsensor.checkdist()
print(distance)
'''

if __name__ == "__main__":

  try:
    while True:
      distance = Ultraschallsensor.checkdist()
      winkel = math.degrees(math.atan((distance/2)/distance)) + 90
      if distance <= 80:
        time.sleep(0.1)
        print(distance)
        print(winkel)
        lenkung_funktion.set_angle(0,winkel)
        MotorAnsteuerung.Motor_Fahren(0.3)
        print('fertig')
      else:
        lenkung_funktion.set_angle(0,80)
        MotorAnsteuerung.Motor_Fahren(0.5)
      time.sleep(0.5)
  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    lenkung_funktion.set_angle(0,80)


'''
if __name__ == "__main__":
  try:

    while True:
      distance = Ultraschallsensor.checkdist()

      if distance <= 20:
        print(f'Distance ist {distance}')
        time.sleep(0.1)
        lenkung_funktion.set_angle(0, 180)
        time.sleep(0.1)
        MotorAnsteuerung.Motor_Fahren(0)
        time.sleep(0.1)

      elif distance <= 100:
        lenkung_funktion.set_angle(0,180)
        time.sleep(0.1)
        MotorAnsteuerung.Motor_Fahren(0.3)

      elif distance <= 120:
        print(f'Distance ist {distance}')
        time.sleep(0.1)
        lenkung_funktion.set_angle(0, 140)
        time.sleep(0.1)
        MotorAnsteuerung.Motor_Fahren(0.6)
        time.sleep(0.1)

      elif distance <= 140:
        lenkung_funktion.set_angle(0, 100)
        time.sleep(0.1)
        MotorAnsteuerung.Motor_Fahren(0.5)

      else:
        print(f'Distance ist {distance}')
        time.sleep(0.1)
        lenkung_funktion.set_angle(0, 80)
        time.sleep(0.1)
        MotorAnsteuerung.Motor_Fahren(0.7)
        time.sleep(0.1)


  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
    lenkung_funktion.set_angle(0,90)

'''
