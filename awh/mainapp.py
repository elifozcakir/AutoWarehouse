from awh.monitor.camera.capture import Camera, OpenCVSimCamera,PointgreyCamera
from awh.monitor.lift.detector import LiftDetector
import cv2
import numpy as np
 

#camera = OpenCVSimCamera('/home/elif/Desktop/default_camera_link_my_camera(1)-00%2d.jpg',12, 16, 4)
#camera = OpenCVSimCamera('/home/elif/Masaüstü/thesis/Detection/default_camera_link_my_camera(1)-00%2d.jpg',16, 22, 4)
#'/home/elif/Masaüstü/thesis/Detection/default_camera_link_my_camera(1)-00%2d.jpg' #16/22 detection photos
#'/home/elif/Desktop/default_camera_link_my_camera(1)-00%2d.jpg'  #12/16 calibration images 
camera= PointgreyCamera()

ldetect = LiftDetector()

lift = ldetect.getLift()
camera.startCamera()
frame = camera.captureLatest()
camera.saveCalibration("/home/elif/Desktop/calib.npy")
camera.loadCalibration("/home/elif/Desktop/calib.npy")
   
   
while True:
    
 
    frame = camera.captureLatest()
    
    ldetect.updateLiftStat(frame)
    lift = ldetect.getLift()
    camera.calculateWorld(lift)
  
    
    print (lift)
    
    frame.show()
    
    
    