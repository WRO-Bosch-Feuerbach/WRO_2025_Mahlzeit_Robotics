import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)

threshold_value = 99
max_value = 255

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
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, threshold_value, max_value, cv2.THRESH_BINARY)

	cv2.imshow("Live-Stream von USB-Kamera", thresh)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
