from curses import can_change_color
import time
from turtle import width
import cv2

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

def ColorDetection():

	HueValueIsOrange = 0
	HueValueIsBlue = 0

	#while True:
	_, frame = cap.read()

	if frame is None:
		print("Das Bild konnte nicht geladen werden")
		exit()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	color = "Undefined"
	height, width, _ = frame.shape

	#cx = int(width / 2)
	#cy = int(height / 2)

	AreaStartPixelX = int(width/2) -3
	AreaStartPixelY = int(height/2) - 3
	AreaEndPixelX = int(width/2) +3
	AreaEndPixelY = int(height/2) +3

	roi = hsv_frame[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

	#pixel_Area = hsv_frame[roi]
	
	picked_hue_value = roi[:, :, 0]

#	print(picked_hue_value)
	
	for hue_value in picked_hue_value.flatten():
#		print(hue_value)
		if 8 < hue_value < 14:
			HueValueIsOrange = HueValueIsOrange + 1
#			print(HueValueIsOrange)
		elif 105 < hue_value < 115:
			HueValueIsBlue = HueValueIsBlue + 1
#			print(HueValueIsBlue)

	if HueValueIsOrange >= 28:
		color = "ORANGE"
		HueValueIsOrange = 0
		print(color)
		return color
	elif HueValueIsBlue >= 28:
		color = "BLUE"
		HueValueIsBlue = 0
		print(color)
		return color
	else:
		color = "WHITE"
		print(color)
		return color

	cv2.imshow("kamerabild", frame)
	


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

def BlackWhiteDetection():

	IsWhite = 0
	IsBlack = 0

	threshold = 127
	max_value = 255

	#while True:
	_, frame = cap.read()

	if frame is None:
		print("Das Bild konnte nicht geladen werden")
		exit()

	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	ret, BlackWhiteFrame = cv2.threshold(grayFrame, threshold, max_value, cv2.THRESH_BINARY)

	height, width = BlackWhiteFrame.shape

	white_pixel = cv2.findNonZero(BlackWhiteFrame)
	
	AreaStartPixelX = int(width/2) -3
	AreaStartPixelY = int(height/2) - 3
	AreaEndPixelX = int(width/2) +3
	AreaEndPixelY = int(height/2) +3

	roi = BlackWhiteFrame[AreaStartPixelY:AreaEndPixelY, AreaStartPixelX:AreaEndPixelX]

	#pixel_Area = hsv_frame[roi]
	
	picked_color = roi[:, :, 0]

#	print(picked_hue_value)
	
	for Color in picked_color.flatten():
		if Color == 255:
			IsWhite = IsWhite + 1
		elif Color == 0:
			IsBlack = IsBlack + 1

	if IsWhite >= 28:
		color = "WHITE"
		return color
	else:
		color = "BLACK"
		return color
	
