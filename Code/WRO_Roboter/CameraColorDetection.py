import time
from turtle import width
import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

#def ColorDetection():

while True:
	_, frame = cap.read()
<<<<<<< HEAD
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	print(hsv_frame.shape)
	height, width, _ = frame.shape

	#cx = int(width / 2)
	#cy = int(height / 2)

	AreaStartPixelX = int(width/2)
	AreaStartPixelY = int(height/2)

	if 55 <= hsv_frame.shape[1] and 55 <= hsv_frame.shape[0]:
		roi_hsv = hsv_frame[55, 55]
		print("Dimensionen der extrahierten Region (ROI):", roi_hsv.shape)

		#pixel_Area = hsv_frame[roi]
		if len(roi_hsv.shape) == 3 and roi_hsv.shape[2] == 3:
			hue_values = roi_hsv[:, :, 0]
			print("Dimensionen des Hue-Arrays:", hue_values.shape)
			print(hue_values)
		else:
			print("Fehler")
			print(roi_hsv.shape)
	else:
		print("Die Region überschreitet die Bildgrenzen")
		print(hsv_frame.shape[1])
		print(hsv_frame.shape[0])
=======

	if frame is None:
		print("Das Bild konnte nicht geladne werden")
		exit()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	height, width, _ = frame.shape

	cx = int(width/2) -5
	cy = int(height/2) - 5
>>>>>>> ba263b278a5b49c59cac4c639faa6c16e29b1262

	pixel_center = hsv_frame[cy, cx]
	hue_value = pixel_center[0]

	color = "Undefined"

	if 9 < hue_value < 13:
		color = "ORANGE"
		#return color
	elif 95 < hue_value < 120:
		color = "BLUE"
		#return color
	else:
		color = "WHITE"
		#return color

#print(pixel_center)
#cv2.putText(frame, color, (10, 50), 0, 1, (255, 0, 0), 2)
#cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)

#cv2.imshow("Frame", frame)
#time.sleep(0.5)
#key = cv2.waitKey(1)
#if key == 27:
	#break

#cap.release()
<<<<<<< HEAD
#cv2.destroyAllWindows()

'''
=======
#cv2.destroyAllWindows()
>>>>>>> ba263b278a5b49c59cac4c639faa6c16e29b1262
