from awh.comm.mqtt.mqtt import Mqtt_Connection
from awh.monitor.lift.detector import Lift
import numpy as np


def main():
    
    mqtt = Mqtt_Connection("192.168.43.120", "AWH")
    
    lift = Lift(10,10,10)
    
    while True:
        lift.x = np.random.rand()
        lift.y = np.random.rand()
        lift.az = np.random.rand()
        mqtt.SendFeedback(lift)

if __name__ == '__main__':
    main()