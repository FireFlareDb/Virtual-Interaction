import cv2
import numpy as np
import HandTrackingModule as htm
import MouseControler as mc
import time

WIDTH, HEIGHT = 3, 4
WCAM, HCAM = 640, 480
FRAME_REDUCTION = 100

smoothValue = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

pTime = 0
detector = htm.handDetector(maxHands=1)

# cap = cv2.VideoCapture("http://192.168.1.33:8080/video")
cap = cv2.VideoCapture(0)
cap.set(HEIGHT, HCAM)
cap.set(WIDTH, WCAM)

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList, bbox = detector.findPosition(img)
    cv2.rectangle(img, (FRAME_REDUCTION, FRAME_REDUCTION),
                  (WCAM - FRAME_REDUCTION, HCAM - FRAME_REDUCTION), (255, 0, 255), 2)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        if fingers[1] == 1 and fingers[2] == 0:
            wSCR, hSCR = mc.getScreenSize()
            x3 = np.interp(x1, (FRAME_REDUCTION, WCAM-FRAME_REDUCTION), (0, wSCR))
            y3 = np.interp(y1, (FRAME_REDUCTION, HCAM-FRAME_REDUCTION), (0, hSCR))
            clocX = plocX + (x3 - plocX) / smoothValue
            clocY = plocY + (y3 - plocY) / smoothValue
            mc.moveCursor(wSCR - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, i = detector.findDistance(8, 12, img, draw=False)
            if length <= 40:
                cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED)
                mc.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # def putText(img, text, org, fontFace, fontScale, color, thickness=None, lineType=None, bottomLeftOrigin=None,
    # /) -> img
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
