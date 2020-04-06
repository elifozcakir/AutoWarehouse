import numpy as np
import cv2


class Camera():
    
    def __init__(self, name):
        self.name = name
        self.setCalibration(None, None,None,None)
    
    def startCamera(self):
        pass
    
    def captureLatest(self):
        pass
    
    def setCalibration(self, mtx, dist, rvec, tvec):
        self.mtx = mtx
        self.dist = dist
        self.rvec = rvec
        self.tvec = tvec
            
    def saveCalibration(self,fname):
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((7*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.  
        frm=self.captureLatest()
        img = frm.img
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
        
        ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        
        np.save(fname, {"M":mtx, "D":dist,"R":rvec, "T":tvec})
        
    def loadCalibration(self, fname):
        L = np.load(fname)
        self.setCalibration(L.item().get("M"), L.item().get("D"), L.item().get("R"), L.item().get("T"))
        
    def projectPoint(self, worldp):
        pass

    def calculateWorld(self, pixp):
        x = pixp.x
        y = pixp.y
        ### convert pıxel to (u,v,1) !!!! Warning distortion 
        u = (x-self.mtx[0][2])/self.mtx[0][0]
        v = (y-self.mtx[1][2])/self.mtx[1][1]
        wp = np.array([u,v,1])
        ### converto to unit vector
        wp = wp/np.linalg.norm(wp)
        self.rvec= np.ravel(self.rvec)
        
        R,_ = cv2.Rodrigues(self.rvec)
        print(R)
        
        ### Rotate to world coordinate system using R transpose
        wp = np.dot(R.T, wp)
        ### rotate camera position -T using R transpose
        self.tvec= np.ravel(self.tvec)
        camera_origin = -self.tvec
        camera_origin = np.dot(R.T, camera_origin)
        t = (0-camera_origin[2])/wp[2]
        x = camera_origin[0] + wp[0]*t
        y = camera_origin[1] + wp[1]*t
        z = camera_origin[2] + wp[2]*t
        print(x)
        print(y)
        print(z)
    
        #new = np.array([x,y,z])
        return [x, y, z]
    
class PointgreyCamera(Camera):
    def __init__(self):
        Camera.__init__(self, "PointgreyCamera")
        
    def startCamera(self):
        self.cap = cv2.VideoCapture(0)
        
    def captureLatest(self):
        img = self.cap.read()
        ret, img = cv2.convertScaleAbs(img)

        frm = Frame(img, self)
        return frm

class OpenCVSimCamera(Camera):
    def __init__(self, fname_template, start, end,noise_std):
        Camera.__init__(self, "OpenCV Camera")
        self.template = fname_template
        self.start = start
        self.end = end
        self.current = start
        self.noise_std = noise_std
    
    
    def startCamera(self):
        pass
    
    def captureLatest(self):
        fname = self.template % (self.current)
        img = cv2.imread(fname)
        #add gaussian noise
        #gauss=np.random.normal(0,1,img.size)
        #gauss=gauss.reshape(img.shape[0],img.shape[1],img.shape[2]).astype('uint8')
        #img=cv2.add(img,gauss) 
        #gaussian smoothing
        #img = cv2.GaussianBlur(img,(5,5),0) 
        #img = cv2.medianBlur(img,7)
         
        frm = Frame(img, self)
        self.current = self.current + 1
        
        if (self.current > self.end):
            self.current = self.start
            
        return frm

class Frame():
    def __init__(self, img, cam):
        self.camera = cam
        self.img = img
        self.detected=None

    def show(self):
        cv2.imshow("Framewin",self.img)
        cv2.imshow("Detected",self.detected)
       
        cv2.waitKey(0)
        
        cv2.destroyAllWindows()

    def clone(self):
        return Frame(self.img.copy(), self.camera)

    def findEllipse(self):
        
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 10
        params.maxThreshold = 200
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 15
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.8
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.6
        # Filter by Inert6
        params.filterByInertia = False
        params.minInertiaRatio = 0.01
        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs.
        keypoints = detector.detect(self.img)       
        im_with_keypoints = cv2.drawKeypoints(self.img, keypoints, np.array([]), (0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.detected=im_with_keypoints
        

        return keypoints
       
