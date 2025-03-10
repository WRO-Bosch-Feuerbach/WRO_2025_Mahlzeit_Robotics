import RPi.GPIO as GPIO
import time

BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
previous_button_state = GPIO.input(BUTTON_PIN)

try:
    while True:
        time.sleep(0.02)
        button_state = GPIO.input(BUTTON_PIN)
        if button_state != previous_button_state:
            previous_button_state = button_state
            if button_state == GPIO.HIGH:
                print("Button has been released")
except KeyboardInterrupt:
    GPIO.cleanup()
