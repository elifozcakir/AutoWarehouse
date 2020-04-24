'''
Created on 14 Şub 2020

@author: elif
'''
import math

class Lift():
    
    def __init__(self, x, y, az):
        self.x = x
        self.y = y
        self.az = az
    
    
    
    def updateLiftState(self, p1, p2):
        p1x=p1[0]
        p1y=p1[1]
        p2x=p2[0]
        p2y=p2[1]
        # Calculate azimuth
        self.az= math.atan2((p1y-p2y), (p1x-p2x))*(180/math.pi) #in degree
        # calculate center
        self.x=(p1x+p2x)/2
        self.y=(p1y+p2y)/2
        
        return self.x, self.y, self.az
        
        
    
    
    def __str__(self):
        return "L(%f,%f,%f)" % (self.x, self.y, self.az)


class LiftDetector():
    def __init__(self):
        self.lift = Lift(0,0,0)
    
    
    def getLift(self):
        return self.lift
    
    def updateLiftStat(self, frame):
        
        hsv= frame.hsvFrame()
        red = hsv.clone().redFilter()
        red = red.img
        blue = hsv.clone().blueFilter()
        blue= blue.img
        img= red + blue
        img= 255-img
        keypoints=frame.findEllipse(img)
        
        if len(keypoints)<2:
            print("Not detected")
            return
        
        for i in range(len(keypoints)): 
            if i==0:
                p1x = keypoints[i].pt[0]
                p1y = keypoints[i].pt[1]
                #print("p1x",p1x)
                #print("p1y",p1y)
            elif i==1:
                p2x = keypoints[i].pt[0]
                p2y = keypoints[i].pt[1]
                #print("p2x",p2x)
                #print("p2y",p2y)
                
        
        p1 = [p1x, p1y]
        p2 = [p2x, p2y]
        
        #p1 = frame.camera.calculateWorld(p1)
        #p2 = frame.camera.calculateWorld(p2)
        self.lift.updateLiftState(p1, p2)
        