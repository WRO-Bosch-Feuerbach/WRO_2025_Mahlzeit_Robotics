import cv2
import numpy as np

lower_red = np.array([0, 120, 150])
upper_red = np.array([10, 255, 255])

lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

cap = cv2.VideoCapture(0)

if not cap.isOpened():
  print("FEHLER: Kamera konnte nicht geöffnet werden!!!")
  exit()

while True:
  ret, frame = cap.read()
  if not ret:
    break

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  mask_red = cv2.inRange(hsv, lower_red, upper_red)
  mask_green = cv2.inRange(hsv, lower_green, upper_green)

  result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
  result_green = cv2.bitwise_and(frame, frame, mask=mask_green)

  combined = np.hstack((result_red, result_green))

  cv2.imshow('Kamera Bild', frame)
  cv2.imshow('Rot und Grün erkannt', combined)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  raw_capture.truncate(0)

cap.release()
cv2.destroyAllWindows()
