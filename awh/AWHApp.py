import threading

from awh.comm.mqtt.mqtt import Mqtt_Connection
from awh.monitor.camera.capture import OpenCVSimCamera
from awh.monitor.lift.detector import LiftDetector


class AWHApp():
    
    def __init__(self):
        camera = OpenCVSimCamera('/home/elif/Masaüstü/thesis/Detection/default_camera_link_my_camera(1)-00%2d.jpg', 16, 22,4)
        self.liftdetect = LiftDetector()
    
    def startFeedbackLoop(self):
        self.stopped = False
        self.mqtt = Mqtt_Connection("192.168.43.120","AWH")
        self.feedbackThread = threading.Thread(target=self.feedbackLoop)
        self.feedbackThread.start()
    
    def feedbackLoop(self):
        while not self.stopped:
            self.mqtt.SendFeedback(self.liftdetect.getLift())
 