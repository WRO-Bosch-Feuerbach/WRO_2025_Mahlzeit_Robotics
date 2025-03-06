from turtle import width
import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
	_, frame = cap.read()
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	height, width, _ = frame.shape

	cx = int(width / 2)
	cy = int(height / 2)

	pixel_center = hsv_frame[cy, cx]
	hue_value = pixel_center[0]

	color = "Undefined"
	if hue_value < 5:
		color = "RED"
	elif hue_value < 22:
		color = "ORANGE"
	elif hue_value < 33: 
		color = "YELLOW"
	elif hue_value < 78:
		color = "GREEN"
	elif hue_value < 131:
		color = "BLUE"
	elif hue_value < 170:
		color = "VIOLET"
	else:
		color = "RED"

	print(pixel_center)
	print(frame, color, (10, 50), 0, 1, (255, 0, 0), 2)
	cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)
