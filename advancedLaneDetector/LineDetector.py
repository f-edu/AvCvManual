'''
Created on Nov 29, 2011

@author: Dima
'''
import cv2 as cv
import numpy as np
from Sensor import LaneSensor

class LineDetector():
    def __init__(self, cropArea, sensorsNumber, sensorsWidth, lineStart, lineEnd, rightLineColorModel):
        self.lineSensors = []
        self.lineModel = None
        self.cropArea = None
        self.Initialize(cropArea, sensorsNumber, sensorsWidth, lineStart, lineEnd, rightLineColorModel)

    def Initialize(self, cropArea, sensorsNumber, sensorsWidth, lineStart, lineEnd, rightLineColorModel):
        self.cropArea = cropArea
        for iSensor in range(0, sensorsNumber):
            sensor = LaneSensor()
            pos = lineStart + iSensor*(lineEnd-lineStart)/(sensorsNumber+1)
            sensor.SetGeometry(pos, sensorsWidth)
            sensor.InitializeModel(rightLineColorModel.avgRGB, rightLineColorModel.avgHSV, (0.8318770212301404, 0.784796499543384, 0.6864621111668014), (41.02017792349725, 0.17449159984689502, 0.832041028240797))
            self.lineSensors.append(sensor) 
        self.lineModel = np.poly1d(np.polyfit([lineStart[1], lineEnd[1]], [lineStart[0], lineEnd[0]], 1)) 
    
    def ProcessFrame(self, img, hsv, canny, outputImg, outputFull):
        #sensors
        laneCoordinatesX = []
        laneCoordinatesY = []
        for sensor in self.lineSensors:
            linesNumber, lineSegments, allSegments = sensor.FindSegments(img, hsv, canny, outputImg, self.lineModel(sensor.yPos))
            if linesNumber == 1:
                sensor.UpdatePositionAndModelFromRegion(img, hsv, lineSegments[0])
                laneCoordinatesY.append((lineSegments[0][0]+lineSegments[0][1])/2)
                laneCoordinatesX.append(sensor.yPos)
    #        if linesNumber == 0:
    #            sensor.UpdatePositionBasedOnCanny(canny)
                
            sensor.UpdatePositionIfItIsFarAway(self.lineModel(sensor.yPos))
        
        if len(laneCoordinatesX)>0:
            rank = 'ok'
            try:
                z = np.polyfit(laneCoordinatesX, laneCoordinatesY, 1)
                #print np.polyfit(laneCoordinatesX, laneCoordinatesY, 1, None, True)
            except np.RankWarning:
                rank = 'bad'
                print ("Line fiting problem")
            except:
                print ('URA!!!')
            if rank == 'ok':
                tmpLineModel = np.poly1d(z) 
                self.lineModel = tmpLineModel
            
            #self.lineModel = np.poly1d(np.polyfit(laneCoordinatesX, laneCoordinatesY, 1))
            for sensor in self.lineSensors:
                #cv.circle(outputImg, (laneCoordinatesX[i], laneCoordinatesY[i]), 2, [200, 0, 100], 2)
                cv.circle(outputImg, (int(self.lineModel(sensor.yPos)), sensor.yPos), 2, [100, 0, 200], 1)

        resPoints,testLeftLineY,testLeftLineYD=self.CheckLinePositionAndDrawOutput(outputFull, img)
        return resPoints,testLeftLineY,testLeftLineYD

    def CheckLinePositionAndDrawOutput(self, outputFull, img):

        testLeftLineY = 50
        testLeftLineYD = 130
        
        #find intersection of a lane edge and test line
        testLeftLineIntersection = int(self.lineModel(testLeftLineY))
        testLeftLineIntersectionD = int(self.lineModel(testLeftLineYD))
        lanePositionColor = [0, 255, 0]

        #line model
        cv.line(outputFull, (self.cropArea[0]+int(self.lineModel(0)), self.cropArea[1]+0), (self.cropArea[0]+int(self.lineModel(img.shape[0])), self.cropArea[1]+img.shape[0]), [255, 0, 0], 2)
        cv.line(outputFull, (self.cropArea[0]+0,self.cropArea[1]+testLeftLineY) , (self.cropArea[0]+img.shape[1],self.cropArea[1]+testLeftLineY), [0.2,0.2,0.2])
        cv.line(outputFull, (self.cropArea[0] + 0, self.cropArea[1] + testLeftLineYD),(self.cropArea[0] + img.shape[1], self.cropArea[1] + testLeftLineYD), [0.2, 0.2, 0.2])

        # #intersection circle !!
        cv.circle(outputFull, (self.cropArea[0]+testLeftLineIntersection, self.cropArea[1]+testLeftLineY), 2, lanePositionColor, 3)
        cv.circle(outputFull, (self.cropArea[0] + testLeftLineIntersectionD, self.cropArea[1] + testLeftLineYD), 2,lanePositionColor, 3)
        resPoints=[self.cropArea[0]+testLeftLineIntersection,self.cropArea[0] + testLeftLineIntersectionD]
        return resPoints,testLeftLineY,testLeftLineYD