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
  # Rote und gruene Pixel zaehlen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  # Zum ueberpr�fen von HSV Werten
  '''
  hsv_pixel = hsv[0,0]
  print('HSV vom Pixel:', hsv_pixel)
  '''

  # Schauen ob was rotes oder gruenes im Bild ist
  if red_count > pixel_threshold:
    Farbe = 'ROT'
  elif green_count > pixel_threshold:
    Farbe = 'GRUEN'
  else:
    Farbe = 'TUNGTUNGTUNGSAHUR'
  return Farbe

def KursanpassungFrameInnen():
  frame = picam.capture_array()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  height, width, _ = frame.shape
  AreaStartPixelX = int(width/2) -10
  AreaStartPixelY = int(height/2) - 10
  AreaEndPixelX = int(width/2) + 10
  AreaEndPixelY = int(height/2) + 10
  red_count = 0
  green_count = 0

  roi = hsv[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

  picked_values = roi[0, 0, 0]

  # Maske erstellen
  red_mask = cv2.inRange(roi, red_lower, red_upper)
  green_mask = cv2.inRange(roi, green_lower, green_upper)
  # Rote und gruene Pixel zaehlen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  #print(f'Red pixel count: {red_count}')
  #print(f'Green pixel count: {green_count}')
  pixel_count = 0
  if red_count > green_count:
    pixel_count = red_count
  if green_count > red_count:
    pixel_count = green_count

  if pixel_count is None:
      pixel_count = 0
  return pixel_count

def SplitscreenLeft():
  frame = picam.capture_array()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  height, width, _ = frame.shape
  AreaStartPixelX = int(width/2) - 128
  AreaStartPixelY = int(height/2) - 72
  AreaEndPixelX = int(width/2) + 0
  AreaEndPixelY = int(height/2) + 72
  red_count = 0
  green_count = 0

  roi = hsv[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

  picked_values = roi[0, 0, 0]

  # Maske erstellen
  red_mask = cv2.inRange(roi, red_lower, red_upper)
  green_mask = cv2.inRange(roi, green_lower, green_upper)
  # Rote und gruene Pixel zaehlen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  #print(f'Red pixel count: {red_count}')
  #print(f'Green pixel count: {green_count}')
  pixel_countLeft = 0
  if red_count > green_count:
    pixel_countLeft = red_count
  if green_count > red_count:
    pixel_countLeft = green_count

  if pixel_countLeft is None:
      pixel_countLeft = 0
  return pixel_countLeft

def SplitscreenRight():
  frame = picam.capture_array()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  height, width, _ = frame.shape
  AreaStartPixelX = int(width/2) + 128
  AreaStartPixelY = int(height/2) - 72
  AreaEndPixelX = int(width/2) + 256
  AreaEndPixelY = int(height/2) + 72
  red_count = 0
  green_count = 0

  roi = hsv[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

  picked_values = roi[0, 0, 0]

  # Maske erstellen
  red_mask = cv2.inRange(roi, red_lower, red_upper)
  green_mask = cv2.inRange(roi, green_lower, green_upper)
  # Rote und gruene Pixel zaehlen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  #print(f'Red pixel count: {red_count}')
  #print(f'Green pixel count: {green_count}')
  pixel_countRight = 0
  if red_count > green_count:
    pixel_countRight = red_count
  if green_count > red_count:
    pixel_countRight = green_count

  if pixel_countRight is None:
      pixel_countRight = 0
  return pixel_countRight

def Blockfarbe2():
  frame = picam.capture_array()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  height, width, _ = frame.shape
  AreaStartPixelX = int(width/2) -10
  AreaStartPixelY = int(height/2) - 10
  AreaEndPixelX = int(width/2) + 10
  AreaEndPixelY = int(height/2) + 10
  red_count = 0
  green_count = 0

  roi = hsv[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

  picked_values = roi[0, 0, 0]

  # Maske erstellen
  red_mask = cv2.inRange(roi, red_lower, red_upper)
  green_mask = cv2.inRange(roi, green_lower, green_upper)
  # Rote und gruene Pixel zaehlen
  red_count = cv2.countNonZero(red_mask)
  green_count = cv2.countNonZero(green_mask)

  #print(f'Red pixel count: {red_count}')
  #print(f'Green pixel count: {green_count}')
  pixel_count = 0
  if red_count > green_count:
    pixel_count = red_count
  if green_count > red_count:
    pixel_count = green_count

  if pixel_count is None:
      pixel_count = 0
  return pixel_count
