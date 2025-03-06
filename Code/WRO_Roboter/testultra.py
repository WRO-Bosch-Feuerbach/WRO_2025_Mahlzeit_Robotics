import smbus2
import RPi.GPIO as GPIO
import time

# I2C-Adresse des PCA9685
PCA9685_ADDRESS = 0x5f

# Definiere den I2C-Bus (I2C-1 auf dem Raspberry Pi)
bus = smbus2.SMBus(1)

# Echo-Pin und Trigger-Pin auf dem Raspberry Pi (GPIO)
ECHO_PIN = 14  # Beispiel: Pin 14 des PCA9685
TRIGGER_PIN = 15  # Beispiel: Pin 15 des PCA9685

# Setup für GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)

# Funktion zum Senden eines Impulses an den Trigger-Pin über den PCA9685
def send_trigger_pulse():
    bus.write_byte_data(PCA9685_ADDRESS, TRIGGER_PIN, 0xFF)  # Trigger-Pin auf HIGH setzen
    time.sleep(0.00001)  # 10 Mikrosekunden warten
    bus.write_byte_data(PCA9685_ADDRESS, TRIGGER_PIN, 0x00)  # Trigger-Pin auf LOW setzen

# Funktion zum Messen der Entfernung mit dem Echo-Pin
def measure_distance():
    send_trigger_pulse()

    # Warte, bis Echo-Pin auf HIGH geht (Start der Messung)
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Warte, bis Echo-Pin wieder auf LOW geht (Ende der Messung)
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Berechne die Zeitdifferenz zwischen Start und Ende
    time_elapsed = stop_time - start_time

    # Schallgeschwindigkeit ist ca. 343 m/s => Entfernung = Zeit * Schallgeschwindigkeit / 2
    distance = (time_elapsed * 34300) / 2

    return distance

if __name__ == "__main__":
    try:
        while True:
            print('Anfang')
            dist = measure_distance()
            print(f"Entfernung: {dist:.2f} cm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Messung gestoppt")

    finally:
        GPIO.cleanup()
