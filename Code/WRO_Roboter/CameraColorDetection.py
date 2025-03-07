import time
from turtle import width
import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

def ColorDetection():

	while True:
		_, frame = cap.read()
		hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		height, width, _ = frame.shape

		cx = int(width / 2)
		cy = int(height / 2)

		pixel_center = hsv_frame[cy, cx]
		hue_value = pixel_center[0]

		color = "Undefined"

		if 9 < hue_value < 13:
			color = "ORANGE"
			return color
		elif 95 < hue_value < 120:
			color = "BLUE"
			return color
		else:
			color = "WHITE"
			return color

#print(pixel_center)
#cv2.putText(frame, color, (10, 50), 0, 1, (255, 0, 0), 2)
#cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)

#cv2.imshow("Frame", frame)
#time.sleep(0.5)
#key = cv2.waitKey(1)
#if key == 27:
	#break

#cap.release()
cv2.destroyAllWindows()

