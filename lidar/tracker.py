from util import movingAverage 

class Tracker:
    def __init__(self):
        self.heading = 0

    def findXAngle(self):
        xAngle = self.heading + 180
        if xAngle >= 360:
            xAngle -= 360
        return xAngle
    
    def findYAngle(self):
        yAngle = self.heading + 90
        if yAngle >= 360:
            yAngle -= 360
        return yAngle

    def updateHeading(self,xAngle,yAngle):
        heading = yAngle - 90
        if heading < 0:
            heading = 360 - abs(heading)
        self.heading = heading
    
    def findCoordinates(self, data):
        minPoints = movingAverage(data)
        yTarget = self.findYAngle()
        xTarget = self.findXAngle()
        miny = 1000
        minx = 1000
        xAngle = 0
        yAngle = 0
        for i in range(len(minPoints)):
            if abs(yTarget - minPoints[i][0]) < miny:
                miny =  abs(yTarget - minPoints[i][0])
                yAngle = minPoints[i][0]
            if abs(xTarget - minPoints[i][0]) < minx:
                minx =  abs(xTarget - minPoints[i][0])
                xAngle = minPoints[i][0]
        return [xAngle,yAngle]


    



    