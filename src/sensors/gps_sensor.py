import serial
import pynmea2
import time

from gyroscope_sensor import GyroscopeSensor

class GPSSensor:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=5)


    def read(self):
        data = self.ser.readline().decode("utf-8")
        if data[0:6] == "$GPGGA":
            msg = pynmea2.parse(data)
            return self.parse(msg)
        else:
            return None
        
    def parse(self, msg):
        lat = msg.latitude
        lon = msg.longitude
        alt = msg.altitude
        speed = msg.spd_over_grnd
        return data(lat, lon, alt, speed)
    
    def close(self):
        self.ser.close()



class data:
    def __init__(self, lat, lon, alt, speed):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.speed = speed

    def __str__(self):
        return "lat: " + str(self.lat) + " lon: " + str(self.lon) + " alt: " + str(self.alt) + " speed: " + str(self.speed)
    
    



if __name__ == "__main__":

    sensor = GPSSensor("/dev/ttyAMAO", 9600)
    while True:
        data = sensor.read()
        print(data)
        time.sleep(1)
        #if data corrupt break
        if data == None:
            break
    sensor.close()
