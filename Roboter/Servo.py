import RPIservo
import time

sc = RPIservo.ServoCtrl()
sc.start()

while 1:
    sc.singleServo(1, -1, 15)
    time.sleep(1)
    sc.stopWiggle()

    sc.singleServo(1, 1, 15)
    time.sleep(1)
    sc.stopWiggle()
