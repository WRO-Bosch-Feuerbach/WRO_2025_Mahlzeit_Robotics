import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

#brightness = 1
#cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)


if not cap.isOpened():
	print("Bild kann nicht geladen werden")
	exit()

while True:
	ret, frame = cap.read()
	if not ret: 
		print("Fehler beim lesen des Kamerabildes")
		break
	
	#-----------------------Varialbles-------------------------
 
	Blue_Max = np.array([60, 255, 255])
	Blue_Min = np.array([30, 100, 100])

	Orange_Max = np.array([60, 255, 255])
	Orange_Min = np.array([30, 100, 100])
 
	pixel_threshold = 100

	#while True:
	_, frame = cap.read()

	if frame is None:
		print("Das Bild konnte nicht geladen werden")
		exit()

	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	color = "Undefined"
	height, width, _ = frame.shape

	#------------------HSV Value testing---------------------

	hsv_frame_pixel = hsv_frame[0,0]
	print('HSV vom Pixel:', hsv_frame_pixel)

	#------------------------Masks---------------------------

	Orange_Mask = cv2.inRange(hsv_frame, Orange_Min, Orange_Max)
	Blue_Mask = cv2.inRange(hsv_frame, Blue_Min, Blue_Max)

	#---------------Counting colored Pixel-------------------
	
	OrangePixel_Count = cv2.countNonZero(Orange_Mask)
	BluePixel_Count = cv2.countNonZero(Blue_Mask)

	#-----------------Color Detection------------------------

	if OrangePixel_Count > pixel_threshold:
		color = "ORANGE"
		print("ORANGE LINE")
	elif BluePixel_Count > pixel_threshold:
		color = "BLUE"
		print("BLUE LINE")
	else:
		color = "WHITE"
		print("WHITE/NOTHING")

	cv2.imshow("Live-Stream von USB-Kamera", hsv_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()



