import serial
import pynmea2
import time
import io

# from gyroscope_sensor import GyroscopeSensor
class GPSSensor:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate, timeout=5.0)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    def read(self):
        try:
            line = self.sio.readline()
            msg = pynmea2.parse(line)
            return self.parse(msg)
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            return None
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            return None

    def parse(self, msg):
        lat = msg.latitude
        lon = msg.longitude
        alt = msg.altitude
        speed = msg.spd_over_grnd
        num_sats = msg.num_sats
        hdop = msg.horizontal_dil
        return (lat, lon, alt, speed, num_sats, hdop)

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    gps = GPSSensor('/dev/ttyS0', 9600)
    try:
        while True:
            data = gps.read()
            if data is not None:
                lat, lon, alt, speed, num_sats, hdop = data
                print('Latitude: {}, Longitude: {}, Altitude: {}, Speed: {}, Num Sats: {}, HDOP: {}'.format(lat, lon, alt, speed, num_sats, hdop))
            time.sleep(1)
    
    except KeyboardInterrupt:
        gps.close()
        print('Bye.')
        