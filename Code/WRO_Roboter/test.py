import time
from board import SCL, SDA
import busio
from adafruit_pca9685  import PCA9685
from adafruit_motor import motor
import Ultraschallsensor
import lenkung_funktion
import MotorAnsteuerung

'''
distance = Ultraschallsensor.checkdist()
print(distance)
'''

if __name__ == "__main__":
  try:

    while True: 
      distance = Ultraschallsensor.checkdist()
      if distance <= 30:
        print('Distance ist ' + distance)
        lenkung_funktion.set_angle(0, 180) 
        MotorAnsteuerung.Motor_Fahren(0.35)
      
      elif distance <= 50:
        print('Distance ist ' + distance)
        lenkung_funktion.set_angle(0, 0)
        MotorAnsteuerung.Motor_Fahren(0.5)
      else:
        print('Distance ist ' + distance)
        lenkung_funktion.set_angle(0, 0)
        MotorAnsteuerung.Motor_Fahren(1)
      


  except KeyboardInterrupt:
    MotorAnsteuerung.Motor_Fahren(0)
