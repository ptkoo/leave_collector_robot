import pynmea2
import time
import io

class GPSSensor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    sentence = line[line.find('$')+1:line.find('*')]  # Extract the characters between '$' and '*'
                    calculated_checksum = self.calculate_checksum(sentence)
                    provided_checksum = int(line[line.find('*')+1:line.find('*')+3], 16)

                    if calculated_checksum != provided_checksum:
                        line = line.replace('*' + line[line.find('*')+1:line.find('*')+3], '*' + calculated_checksum)

                    msg = pynmea2.parse(line)
                    yield self.parse(msg)
                except pynmea2.ParseError as e:
                    print('Parse error: {}'.format(e))
                except ValueError:
                    print('Invalid checksum in the sentence.')
                continue

    def calculate_checksum(self, sentence):
        checksum = 0
        for char in sentence:
            checksum ^= ord(char)
        return '{:02X}'.format(checksum)

    def parse(self, msg):
        lat = msg.latitude
        lon = msg.longitude
        alt = msg.altitude
        speed = msg.spd_over_grnd
        num_sats = msg.num_sats
        hdop = msg.horizontal_dil
        return (lat, lon, alt, speed, num_sats, hdop)

if __name__ == '__main':
    gps = GPSSensor('src/sensors/mock.log')  # Change to the path of your mockup GPS data file
    try:
        for data in gps.read():
            if data is not None:
                lat, lon, alt, speed, num_sats, hdop = data
                print('Latitude: {}, Longitude: {}, Altitude: {}, Speed: {}, Num Sats: {}, HDOP: {}'.format(lat, lon, alt, speed, num_sats, hdop))
            time.sleep(1)

    except KeyboardInterrupt:
        print('Bye.')
