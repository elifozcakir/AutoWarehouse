import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from awh.AWHApp import AWHApp


Window.size = (1366, 768)
Window.fullscreen = False

Window.clearcolor = (0.9, 0.9, 0.9, 1)


class TestForCalibration(FloatLayout):
    pass

class StartCalibration(FloatLayout):
    pass

class CalibrationReport(FloatLayout):
    pass

class ManageItems(FloatLayout):
    pass

class ManageRoutes(FloatLayout):
    pass

class Monitor(FloatLayout):
    pass

def testcali_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Test For Calibration", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png',auto_dismiss = False)
    popupWindow.open()

def startcali_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Start Calibration", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png')
    popupWindow.open()

def calireport_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Calibration Report", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png')
    popupWindow.open()

def manageitem_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Manage Items", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png')
    popupWindow.open()

def manageroute_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Manage Routes", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png')
    popupWindow.open()

def monitor_popup():
    show = TestForCalibration()
    popupWindow = Popup(title="Monitor", content=show, size_hint=(None,None),size=(500,200), background = 'awh_systems_popup_background.png')
    popupWindow.open()


class SecondWindow(Screen):


    def __init__(self,*args,**argsv):
        Screen.__init__(self,*args,**argsv)
        self.awh = AWHApp()

    def testforcali(self):
        testcali_popup()

    def start_calibration(self):
        startcali_popup()

    def calibration_report(self):
        calireport_popup()

    def manage_item(self):
        manageitem_popup()

    def manage_routes(self):
        manageroute_popup()

    def monitor_page(self):
        self.awh.startFeedbackLoop()

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

class MyApp(App):
    def build(self):
        return kv

    
if __name__ =="__main__":
    MyApp().run()
