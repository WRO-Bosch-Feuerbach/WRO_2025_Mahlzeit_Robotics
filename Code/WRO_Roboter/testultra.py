import RPi.GPIO as GPIO
import time

# Echo-Pin und Trigger-Pin auf dem Raspberry Pi (GPIO)
ECHO_PIN = 15  # Beispiel: physischer Pin für Echo (GPIO 22)
TRIGGER_PIN = 14  # Beispiel: physischer Pin für Trigger (GPIO 17)

# Setup für GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)

# Funktion zum Senden eines Impulses an den Trigger-Pin (direkt über GPIO)
def send_trigger_pulse():
    # Trigger-Pin auf LOW setzen und kurz warten
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    time.sleep(0.000002)  # 2 Mikrosekunden
    
    # Trigger-Pin auf HIGH setzen für 10 Mikrosekunden
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 Mikrosekunden
    
    # Trigger-Pin wieder auf LOW setzen
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

# Funktion zum Messen der Entfernung mit dem Echo-Pin
def measure_distance():
    send_trigger_pulse()

    # Warte, bis Echo-Pin auf HIGH geht (Start der Messung)
    start_time = time.time()
    timeout = start_time + 1.0  # Timeout von 1 Sekunde für den Start

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
        if time.time() > timeout:
            print("Fehler: Start Timeout")
            return None

    # Warte, bis Echo-Pin wieder auf LOW geht (Ende der Messung)
    stop_time = time.time()
    timeout = stop_time + 1.0  # Timeout von 1 Sekunde für das Ende
    
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
        if time.time() > timeout:
            print("Fehler: Stop Timeout")
            return None

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
            if dist is not None:
                print(f"Entfernung: {dist:.2f} cm")
            else:
                print("Messfehler")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Messung gestoppt")

    finally:
        GPIO.cleanup()
