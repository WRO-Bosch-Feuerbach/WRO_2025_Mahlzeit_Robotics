import RPIservo
import time

sc = RPIservo.ServoCtrl()
sc.start()

while 1:
    sc.singleServo(3, -1, 2)
    time.sleep(1)
    sc.stopWiggle()

    sc.singleServo(3, 1, 2)
    time.sleep(1)
    sc.stopWiggle()