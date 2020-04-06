import paho.mqtt.publish as publish  # MQTT Library For Connection.


class Mqtt_Connection: # MQTT Connection Class.
    def __init__(self, server, path):
        self.MQTT_SERVER = server
        self.MQTT_PATH = path
        publish.single(self.MQTT_PATH, "Connected!", hostname=self.MQTT_SERVER) # Send Connected Message.
        print("Check your pi to make sure connection. You should see 'Connected!' message.") # İnformation
    
    def Send_Message(self,message): # Send Coordinates Function.
        publish.single(self.MQTT_PATH,message,hostname=self.MQTT_SERVER)
        
    def SendFeedback(self,lift): # Send Attitudes Function.
        
        message = self.constructFeedbackMessage(lift)
        self.Send_Message(message)
        
    def Send_TakeItem(self, fromPos, toPos): # Send Lines Function.
        
        message = self.constructTakeMessage(fromPos, toPos)
        self.Send_Message(message)
    
    def constructFeedbackMessage(self, lift):
        message = "FB:%3.3f,%3.3f,%3.3f:BF" % (lift.x, lift.y, lift.az)
        return message
        
    def constructTakeMessage(self, fromPos, toPos):
        message = "TK:%3.3f,%3.3f:%3.3f,%3.3f:KT" % (fromPos[0],fromPos[1],toPos[0],toPos[1])
        return message
        