import time
import subprocess
import RPi.GPIO as GPIO
import MotorAnsteuerung

BUTTON_PIN = 5  # GPIO2 (SDA)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

running_process = None  # Speichert den Prozess

def button_callback(channel):
    global running_process
    if running_process is None:
        print("Programm gestartet")
        running_process = subprocess.Popen(["python3", "test.py"])
    else:
        print("Programm gestoppt")
        MotorAnsteuerung.Motor_Fahren(0)  # Motor anhalten
        GPIO.cleanup()  # GPIO-Pins freigeben
        running_process.terminate()
        running_process = None

# Interrupt für den Button setzen
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    print("Starten")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Beendet")
    GPIO.cleanup()
    if running_process:
        running_process.terminate()