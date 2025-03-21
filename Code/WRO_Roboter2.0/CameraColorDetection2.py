import time
from turtle import width
import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

#def ColorDetection():

while True:
	_, frame = cap.read()

	if frame is None:
		print("Das Bild konnte nicht geladne werden")
		exit()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	HueValueIsOrange = 0
	HueValueIsBlue = 0
	color = "Undefined"
	height, width, _ = frame.shape

	#cx = int(width / 2)
	#cy = int(height / 2)

	AreaStartPixelX = int(width/2) -5
	AreaStartPixelY = int(height/2) - 5
	AreaEndPixelX = int(width/2) +5
	AreaEndPixelY = int(height/2) +5

	roi = hsv_frame[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

	#pixel_Area = hsv_frame[roi]
	
	hue_value = roi[:, :, 0]

	for hue_value in roi:
		if 9 < hue_value < 13:
			HueValueIsOrange = HueValueIsOrange + 1
		elif 105 < hue_value < 115:
			HueValueIsBlue = HueValueIsBlue + 1

	if HueValueIsOrange >= 20:
		color = "ORANGE"
		print(color)
	elif HueValueIsBlue >= 20:
		color = "BLUE"
		print(color)
	else:
		color = "WHITE"
		print(color)

	#highlightedArea = frame.copy()

	#highlightedArea[hue_mask] = [0, 0, 255]
#print(pixel_center)
#cv2.putText(frame, color, (10, 50), 0, 1, (255, 0, 0), 2)
#cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 3)

#cv2.imshow("Frame", frame)
#time.sleep(0.5)
#key = cv2.waitKey(1)
#if key == 27:
	#break

#cap.release()
#cv2.destroyAllWindows()