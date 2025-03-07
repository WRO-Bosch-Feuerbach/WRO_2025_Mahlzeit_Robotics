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

	print (hsv_frame.shape)

	height, width, _ = frame.shape

	#cx = int(width / 2)
	#cy = int(height / 2)

	AreaStartPixelX = int(width/2) -5
	AreaStartPixelY = int(height/2) - 5

	roi = hsv_frame[AreaStartPixelY, AreaStartPixelX]

	#pixel_Area = hsv_frame[roi]
	
	hue_value = roi[:, :, 0]

	print(hue_value)


	'''
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
#cv2.destroyAllWindows()

'''