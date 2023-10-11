import imusensor.MPU9250 as mpu9250
import time

class GyroscopeSensor:
    def __init__(self):
        self.sensor = mpu9250.MPU9250()

    def read(self):
        return self.sensor.readGyro()
    
    def close(self):
        self.sensor.close()

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " z: " + str(self.z)
    
if __name__ == "__main__":
    sensor = GyroscopeSensor()
    while True:
        data = sensor.read()
        print(data)
        time.sleep(1)
        #if data corrupt break
        if data == None:
            break
    sensor.close()

        
        