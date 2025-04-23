from curses import can_change_color
import time
from turtle import width
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)


def ColorDetection2_0():

	#-----------------------Varialbles-------------------------
 
	Orange_Max = np.array([15, 150, 255])
	Orange_Min = np.array([0, 25, 100])

	Blue_Max = np.array([115, 255, 255])
	Blue_Min = np.array([100, 100, 100])
 
	pixel_threshold = 75

	#while True:
	_, frame = cap.read()

	if frame is None:
		print("Das Bild konnte nicht geladen werden")
		exit()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	color = "Undefined"
	height, width, _ = frame.shape

	#------------------HSV Value testing---------------------

	#hsv_frame_pixel = hsv_frame[0,0]
	#print('HSV vom Pixel:', hsv_frame_pixel)

	#------------------------Masks---------------------------

	Orange_Mask = cv2.inRange(hsv_frame, Orange_Min, Orange_Max)
	Blue_Mask = cv2.inRange(hsv_frame, Blue_Min, Blue_Max)

	#---------------Counting colored Pixel-------------------
	
	OrangePixel_Count = cv2.countNonZero(Orange_Mask)
	BluePixel_Count = cv2.countNonZero(Blue_Mask)

	#-----------------Color Detection------------------------

	if OrangePixel_Count > pixel_threshold:
		color = "ORANGE"
		return color
	elif BluePixel_Count > pixel_threshold:
		color = "BLUE"
		return color
	else:
		color = "WHITE"
		return color