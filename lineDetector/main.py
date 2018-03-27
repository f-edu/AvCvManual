import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture("test_videos/road.avi")
if cap.isOpened() == False:
    print ("Cannot open input video")
    exit()



frameNumber = 0
while (cv.waitKey(1) != 27):
    frameNumber += 1
    # read and crop
    flag, frame = cap.read()
    if flag == False: break # end of video
    time.sleep(0.03)
    frame=cv.resize(frame, (int(640), int(480)))
    hsv_image = cv.cvtColor(frame, cv.COLOR_RGB2HSV)

    lower = np.array([0, 0, 150])
    upper = np.array([255, 255, 255])

    thresh = cv.inRange(hsv_image, lower, upper)
    thresh = cv.erode(thresh, None, iterations=1)  # delete other white pixels
    thresh = cv.dilate(thresh, None, iterations=3)  # not change ROI blob size in prev function (erode)

    canny = cv.Canny(thresh, 280, 360,apertureSize = 3)

    lines = cv.HoughLinesP(canny, 1, np.pi / 4, 2, None, 10, 1)

    if lines is not None:
        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])

            cv.line(frame, pt1, pt2, (0, 0, 255), 3)

    cv.imshow("Output full", thresh)
    cv.imshow("Output thresh1", canny)
    cv.imshow("Output frame", frame)


cv.destroyAllWindows()