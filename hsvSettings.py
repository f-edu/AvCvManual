import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100
mh,ms,mv = 100,100,100
# Creating track bar
cv.createTrackbar('h', 'result',0,255,nothing)
cv.createTrackbar('s', 'result',0,255,nothing)
cv.createTrackbar('v', 'result',0,255,nothing)

cv.createTrackbar('mh', 'result',0,255,nothing)
cv.createTrackbar('ms', 'result',0,255,nothing)
cv.createTrackbar('mv', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv.getTrackbarPos('h','result')
    s = cv.getTrackbarPos('s','result')
    v = cv.getTrackbarPos('v','result')

    mh = cv.getTrackbarPos('mh','result')
    ms = cv.getTrackbarPos('ms','result')
    mv = cv.getTrackbarPos('mv','result')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([mh,ms,mv])

    mask = cv.inRange(hsv,lower_blue, upper_blue)

    result = cv.bitwise_and(frame,frame,mask = mask)

    cv.imshow('result',result)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv.destroyAllWindows()