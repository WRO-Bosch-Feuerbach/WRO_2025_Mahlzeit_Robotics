import cv2
import numpy as np
import time

#Kamere einrichten
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 854)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

time.sleep(0.1)

#Farbwerte definieren
red_lower = np.array([0,150,100])
red_upper = np.array([10,255,255])

green_lower = np.array([55,50,50])
green_upper = np.array([70,255,255])

print('Start Farberkennung')

while True:
  ret, frame = cap.read()
  if not ret:
    print('Fehler beim Kamerazugriff')
    break
  
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
  # Farbmaske erstellen
  red_mask = cv2.inRange(hsv, red_lower, red_upper)
  green_mask = cv2.inRange(hsv, green_lower, green_upper)
  
  
  # Farbe hervorheben = alles was nicht die Farbe ist wird Schwarz
  red_result = cv2.bitwise_and(frame, frame, mask=red_mask)
  green_result = cv2.bitwise_and(frame, frame, mask=green_mask)
  
  # Pixel zählen
  red_pixels = cv2.countNonZero(red_mask)
  green_pixels = cv2.countNonZero(green_mask)
  
  # wenn genug pixel im bild sind dann ausgeben
  if red_pixels > 500:
    print('Rot erkannt')
  elif green_pixels > 500:
    print('Grün erkannt')
  else:
    print(' nix ')
  

  # Bild in GUI ausgeben lassen
  combined = cv2.addWeighted(red_result, 1, green_result, 1, 0)
  cv2.imshow("Kamera", frame)
  cv2.imshow("Erkannte Farben", combined)
  
  
  # beenden mit q
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  


cap.release()
cv2.destroyAllWindows()
