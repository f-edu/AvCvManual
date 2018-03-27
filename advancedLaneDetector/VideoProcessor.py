import cv2 as cv
from LaneMarkersModel import LaneMarkersModel
from LaneMarkersModel import normalize
import numpy as np
from Sensor import LaneSensor
from LineDetector import LineDetector
import time
#Initialize video input
stream = cv.VideoCapture(1) #6 7 8
# stream = cv.VideoCapture("test_videos/out7.avi") #6 7 8
if stream.isOpened() == False:
    print ("Cannot open input video")
    exit()

#some image processing parameters

cropArea = [0, 300, 640, 480] #[from left, from up, to right, to down ]
# cropArea = [0, 124, 637, 298]
sensorsNumber = 10
sensorsWidth = 40
# 640x480

#6L
line1LStart = np.array([240, 80])
line1LEnd = np.array([0, 180])
#6R
line1RStart = np.array([240, 80])
line1REnd = np.array([480, 180])
#
#VideoTest
# cropArea = [0, 350, 1280, 700] #[from left, from up, to right, to down ]
# # cropArea = [0, 124, 637, 298]
# sensorsNumber = 20
# sensorsWidth = 70
# #6L
# line1LStart = np.array([100, 80])
# line1LEnd = np.array([100, 250])
# #6R
# line1RStart = np.array([300, 80])
# line1REnd = np.array([300, 250])
#

# #RoadTest
# cropArea = [50, 250, 1230, 700] #[from left, from up, to right, to down ]
# # cropArea = [0, 124, 637, 298]
# sensorsNumber = 25
# sensorsWidth = 150
# #6L
# line1LStart = np.array([100, 80])
# line1LEnd = np.array([100, 250])
# #6R
# line1RStart = np.array([1000, 80])
# line1REnd = np.array([1000, 250])
#7L
#line1LStart = np.array([71, 163])
#line1LEnd= np.array([303, 3])

#get first frame for color model
flag, imgFull = stream.read()

img = imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]]

#Initialize left lane
leftLineColorModel = LaneMarkersModel()
#leftLineColorModel.InitializeFromImage(np.float32(img)/255.0, "Select left line")
leftLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1LStart, line1LEnd, leftLineColorModel)

#Initialize right lane
rightLineColorModel = LaneMarkersModel()
#rightLineColorModel.InitializeFromImage(np.float32(img)/255.0, "Select right line")
rightLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1RStart, line1REnd, rightLineColorModel)



frameNumber = 0
while(cv.waitKey(1) != 27):
    # cv.waitKey(0)
    frameNumber+=1
    #read and crop
    flag, imgFull = stream.read()
    # imgFull=cv.resize(imgFull, (int(1280), int(920)))
    if flag == False: break #end of video
    time.sleep(0.01)
    #do some preprocessing to share results later
    img = np.float32(imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]])/255.0
    hsv = np.float32(cv.cvtColor(img, cv.COLOR_RGB2HSV))
    canny = cv.Canny(cv.cvtColor(np.uint8(img*255), cv.COLOR_RGB2GRAY), 70, 170)
 
    #make output images
    outputImg = img.copy()
    outputFull = imgFull.copy()

    #process frame
    leftResPoints,testLeftLineY,testLeftLineYD=leftLine.ProcessFrame(img, hsv, canny, outputImg, outputFull)
    rightResPoints=rightLine.ProcessFrame(img, hsv, canny, outputImg, outputFull)
    h1=cropArea[1]+testLeftLineY
    h2=cropArea[1]+testLeftLineY+testLeftLineYD

    # 4 points for angle calculate
    w1h1=leftResPoints[0]
    w2h2=rightResPoints[0][1]
    w1h2=leftResPoints[1]
    w2h1=rightResPoints[0][0]



    #
    #show output
    cv.imshow("Output", outputImg)
    cv.imshow("Output full", outputFull)

    
cv.destroyAllWindows()