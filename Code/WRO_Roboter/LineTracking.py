import argparse
from gpiozero import InputDevice

line_pin_left = 22
line_pin_middle = 27
line_pin_right = 17

left = InputDevice(pin=line_pin_right)
middle = InputDevice(pin=line_pin_middle)
right = InputDevice(pin=line_pin_left)

def CheckLines():
    status_right = right.value
    status_middle = middle.value
    status_left = left.value


'''
if __name__ == '__main__':
    try:
      while 1:
        run()
        time.sleep(0.3)
    except KeyboardInterrupt:
        pass
'''