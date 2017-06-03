import numpy as np
import cv2 as cv
cap = cv.VideoCapture(1)

while(True):
   ret, frame = cap.read()

   hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

   hsv = cv.blur(hsv, (5, 5))

   lower = np.array([56, 91, 149])
   upper = np.array([255, 255, 255])
   thresh = cv.inRange(hsv, lower, upper)

   thresh = cv.erode(thresh, None, iterations=2)
   thresh = cv.dilate(thresh, None, iterations=6)

   contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

   for cnt in contours:
      c = sorted(contours, key=cv.contourArea, reverse=True)[0]
      rect = cv.minAreaRect(c)
      box = np.int0(cv.cv.BoxPoints(rect))
      cv.drawContours(frame, [box], -1, (0, 255, 0), 3)  # draw contours in green color

      y1 = int(box[0][1])
      x2 = int(box[1][0])
      y2 = int(box[1][1])
      x3 = int(box[2][0])

      roiImg =frame[y2:y1, x2:x3]

      if roiImg.any():
         cv.imshow('roiImg', roiImg)

         noDrive = cv.imread("noDrive.png")

         resizedRoi = cv.resize(roiImg, (100, 100))
         noDrive=cv.resize(noDrive,(100, 100))

         xresizedRoi=cv.inRange(resizedRoi, lower, upper)
         xnoDrive=cv.inRange(noDrive, lower, upper)

         identity_percent=0
         for i in range(100):
            for j in range(100):
               if (xresizedRoi[i][j]==xnoDrive[i][j]):
                  identity_percent=identity_percent+1
         print identity_percent

   cv.imshow('frame', frame)

   if cv.waitKey(1) & 0xFF == ord('q'):
       break
cap.release()
cv.destroyAllWindows()
