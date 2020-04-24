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
        
        pattern_size = (7, 7)
        pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
        pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)

        obj_points = []
        img_points = []
        i = -1
        j= 0
        while True:
            i += 1
            framestep = 20
            frm=self.captureLatest()
            img = frm.img
            cv2.imshow('frame',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if i % framestep != 0:
                continue
            print('Searching for chessboard in frame ' + str(i) + '...'),
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
            found, corners = cv2.findChessboardCorners(img, pattern_size, flags=cv2.CALIB_CB_FILTER_QUADS)
            if found:
                j+=1
                term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
                corners2 = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), term)
                if j == 15:
                    break
                else:
                    continue     
            if not found:
                print ('not found')
                continue
           
        

        #print('\nPerforming calibration...')

        img_points.append(corners2.reshape(1, -1, 2))
        obj_points.append(pattern_points.reshape(1, -1, 3))
        rms, mtx, dist, rvec, tvec = cv2.calibrateCamera(obj_points, img_points, img.shape[::-1],None,None)
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
        #print(self.rvec)
        self.rvec= np.ravel(self.rvec)
        #print(self.rvec)
        R,_ = cv2.Rodrigues(self.rvec)
        #print(R)
        
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
        print("world",x,y,z)
    
        #new = np.array([x,y,z])
        return [x, y, z]
    
class PointgreyCamera(Camera):
    def __init__(self):
        Camera.__init__(self, "PointgreyCamera")
        
    def startCamera(self):
        self.cap = cv2.VideoCapture(0)
        
    def captureLatest(self):
        _, img = self.cap.read()
        #gaussian smoothing
        #img = cv2.GaussianBlur(img,(5,5),0) 
        #img = cv2.medianBlur(img,7)

        return Frame(img, self)

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
         
        #frm = Frame(img, self)
        self.current = self.current + 1
        
        if (self.current > self.end):
            self.current = self.start
            
        return Frame(img, self)

class Frame():
    def __init__(self, img, cam ):
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
    
    def hsvFrame(self):
        
        return Frame(cv2.cvtColor(self.img.copy(),cv2.COLOR_BGR2HSV), self.camera)
    
    def blueFilter(self):
        #lower_blue = np.array([100,50,50])
        #upper_blue = np.array([120,255,255])
        #mask1 = cv2.inRange(self.img, lower_blue, upper_blue)

        #lower_blue = np.array([10,50,50])
        #upper_blue = np.array([140,255,255])
        #mask2 = cv2.inRange(self.img, lower_blue, upper_blue)

        #blueFiltered = mask1 + mask2
        
        return Frame(cv2.inRange(self.img,(100,50,50),(120,255,255))+cv2.inRange(self.img,(10,50,50),(140,255,255)),self.camera)
    
    def redFilter(self):
        #lower_red = np.array([0, 125, 50])
        #upper_red = np.array([10, 255,255])
        #mask1= cv2.inRange(self.img, lower_red, upper_red)

        #lower_red = np.array([170, 120, 70])
        #upper_red = np.array([180, 255, 255])
        #mask2 = cv2.inRange(self.img, lower_red, upper_red)  
         
        #redFiltered = mask1 + mask2
        
        return Frame(cv2.inRange(self.img,(0,125,50),(10,255,255))+cv2.inRange(self.img,(170,120,50),(180,255,255)),self.camera)
    
    def findEllipse(self,img):
        
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 0
        params.maxThreshold = 256
        
        params.filterByCircularity = True
        params.minCircularity = 0.5

        params.filterByArea = True
        params.minArea = 100
 
        params.filterByConvexity = False
        params.minConvexity = 0.5
        # Filter by Inert6
        params.filterByInertia = True
        params.minInertiaRatio = 0.5
        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs.
        keypoints = detector.detect(img)       
        im_with_keypoints = cv2.drawKeypoints(self.img, keypoints, np.array([]), (0,255,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        self.detected=im_with_keypoints
        

        return keypoints
       
