from picamera2 import Picamera2
import numpy as np
import cv2
import time

# Kamera einstellen
picam = Picamera2()
picam.start()
time.sleep(1)

# HSV bereiche einstellen
red_upper = np.array([140, 255, 255])
red_lower = np.array([125, 100, 100])

green_upper = np.array([60, 255, 255])
green_lower = np.array([30, 100, 100])

pixel_threshold = 150

def Blockfarbe():
  frame = picam.capture_array()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  # Maske erstellen
  red_mask = cv2.inRange(hsv, red_lower, red_upper)
  green_mask = cv2.inRange(hsv, green_lower, green_upper)
  # Rote und grüne Pixel zählen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  # Zum überprüfen von HSV Werten
  '''
  hsv_pixel = hsv[0,0]
  print('HSV vom Pixel:', hsv_pixel)
  '''

  # Schauen ob was rotes oder grünes im Bild ist
  if red_count > pixel_threshold:
    Farbe = 'ROT'
  elif green_count > pixel_threshold:
    Farbe = 'GRUEN'
  else:
    Farbe = 'TUNGTUNGTUNGSAHUR'
  return Farbe

