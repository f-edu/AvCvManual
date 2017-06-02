import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
while(True):
   ret, frame = cap.read()
   cv.imshow('frame',frame)

   hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
   cv.imshow('hsv', hsv)

   hsv = cv.blur(hsv, (5, 5))
   cv.imshow('hsv2', hsv)

   lower = np.array([56, 91, 149])
   upper = np.array([255, 255, 255])
   thresh = cv.inRange(hsv, lower, upper)
   cv.imshow('thresh', thresh)

   thresh = cv.erode(thresh, None, iterations=2)
   thresh = cv.dilate(thresh, None, iterations=6)

   if cv.waitKey(1) & 0xFF == ord('q'):
       break
cap.release()
cv.destroyAllWindows()
