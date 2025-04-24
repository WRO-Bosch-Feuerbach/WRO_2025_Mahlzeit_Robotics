import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA


# Initialisiere I2C
i2c = busio.I2C(SCL, SDA)

# PCA9685 Initialisieren
pca = PCA9685(i2c, address=0x5f)
pca.frequency = 50  # Standartwert für Servos

# Funktion zum Setzen des Winkels
def set_angle(ID, angle):
    # min und max Winkel definieren
    angle = max(0, min(angle, 180))

    # Servoinstanz wird erstellt
    servo_angle = servo.Servo(pca.channels[ID], min_pulse=1000, max_pulse=2000, actuation_range=180)
    servo_angle.angle = angle  # Winkel wird gesetzt

# Hier wird der Servo ganz nach rechts gelenkt (180 Grad)
#set_angle(0, 180)  # Kanal 0, 180 Grad für ganz rechts

if __name__ == "__main__":
  while True:
    set_angle(1, 90)