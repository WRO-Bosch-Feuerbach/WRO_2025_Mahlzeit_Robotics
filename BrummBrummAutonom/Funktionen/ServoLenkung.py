import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA


# Initialisiere I2C
i2c = busio.I2C(SCL, SDA)

# PCA9685 Initialisieren
pca = PCA9685(i2c, address=0x5f)
pca.frequency = 50  # Frequenz auf 50 Hz setzen (Standard für Servos)

# Funktion zum Setzen des Winkels
def set_angle(ID, angle):
    """
    Setzt den Winkel des Servos auf dem angegebenen Kanal (ID).
    Der Winkel muss zwischen 0 und 180 Grad liegen.
    """
    # Stelle sicher, dass der Winkel im richtigen Bereich ist
    angle = max(0, min(angle, 180))

    # Erstelle eine Servo-Instanz und steuere den Servo auf dem angegebenen Kanal
    servo_angle = servo.Servo(pca.channels[ID], min_pulse=1500, max_pulse=2400, actuation_range=180)
    servo_angle.angle = angle  # Setze den gewuenschten Winkel

# Hier wird der Servo ganz nach rechts gelenkt (180 Grad)
#set_angle(0, 180)  # Kanal 0, 180 Grad für ganz rechts

if __name__ == "__main__":
  while True:
    set_angle(1, 90)