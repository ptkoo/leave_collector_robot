import serial

import time

import io

import math



# from gyroscope_sensor import GyroscopeSensor

class GPSSensor:

    def __init__(self, port, baudrate):

        self.port = port

        self.baudrate = baudrate

        self.ser = serial.Serial(port, baudrate, timeout=0.5)

        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

        self.text_stream = []  # Initialize a variable to accumulate the text stream

        self.GPSdata = {

            'latitude' : 0,

            'longitude' : 0

            }

        self.distanceTravelled = 0





    def read(self):

        try:

            for _ in range(9):

                line = self.ser.readline().strip()

                self.text_stream.append(line)

            self.decodeData(self.text_stream)

        except serial.SerialException as e:

            print('Device error: {}'.format(e))

            return None

    

        

        if len(self.text_stream) == 9: 

            self.text_stream = []

    

    def decodeData(self, data):

        for data in data:

            data = data.decode('latin-1') 

            

            if data.startswith('$GPGGA'):

                GGAdata = data.split(',')

               # print(GGAdata)

                continue

            elif data.startswith('$GPRMC'):

                RMCdata = data.split(',')

                # Extract latitude and longitude values and their signs

                

                latitudeData = float(RMCdata[3]) # Convert minutes to degrees

                longitudeData = float(RMCdata[5]) # Convert minutes to degrees

                

                # Convert latitude and longitude from the format provided to degrees

                latitude_minutes = float(latitudeData) / 100

                longitude_minutes = float(longitudeData) / 100

                

                # Separate the degrees and minutes

                latitude_degrees = int(latitude_minutes)

                longitude_degrees = int(longitude_minutes)

                

                # Calculate the remaining minutes (decimal part)

                latitude_minutes = (latitude_minutes - latitude_degrees) * 100

                longitude_minutes = (longitude_minutes - longitude_degrees) * 100

                

                latitude = latitude_degrees + latitude_minutes/60

                longitude = longitude_degrees + longitude_minutes/60

                

                lat_sign = RMCdata[4]  # 'N' for North, 'S' for South

                lon_sign = RMCdata[6]  # 'E' for East, 'W' for West

                

                # Check the sign and adjust latitude and longitude accordingly

                if lat_sign == 'S':

                    latitude = -latitude

                if lon_sign == 'W':

                    longitude = -longitude

                    

                currentGPSdata = {

                    'latitude' : latitude,

                    'longitude' : longitude

                    }

                self.calculateDistance(self.GPSdata,currentGPSdata)

                #Record data

                self.GPSdata = {

                'latitude': latitude,

                'longitude': longitude

                }

                print(RMCdata)

                 

                continue

            elif data.startswith('$GPVTG'):

                VTGdata = data.split(',')

                continue

            elif data.startswith('$GPGSA'):

                GSAdata = data.split(',')

                continue

            elif data.startswith('$GPGLL'):

                GLLdata = data.split(',')

            

        

                    

    def calculateDistance(self,oldGPSdata, currentGPSdata):

        

        latitudeOld = math.radians(oldGPSdata['latitude']) if oldGPSdata.get('latitude', 0) != 0 else None

        longitudeOld = math.radians(oldGPSdata['longitude']) if oldGPSdata.get('longitude', 1) != 0 else None

        latitudeCurrent = math.radians(currentGPSdata['latitude'])

        longitudeCurrent = math.radians(currentGPSdata['longitude'])

        R = 6371 # earth radius in km

        

        if latitudeOld is not None and longitudeOld is not None:

            # Calculate Cartesian coordinates

            '''x1 = R * math.cos(latitudeOld) * math.cos(longitudeOld)

            y1 = R * math.cos(latitudeOld) * math.sin(longitudeOld)

            z1 = R * math.sin(latitudeOld)



            x2 = R * math.cos(latitudeCurrent) * math.cos(longitudeCurrent)

            y2 = R * math.cos(latitudeCurrent) * math.sin(longitudeCurrent)

            z2 = R * math.sin(latitudeCurrent)

            

            self.distanceTravelled = (math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2))*1000 '''

            lat = (latitudeOld+latitudeCurrent)/2

            lon = (longitudeOld+longitudeOld) /2

            dlat = latitudeCurrent - latitudeOld

            dlon = longitudeCurrent - longitudeOld

            

            self.distanceTravelled = (R * math.sqrt(dlat**2 + (math.cos(lat)**2 * dlon**2)))*1000

            

        print(self.distanceTravelled)

      

        

    def close(self):

        self.ser.close()





if __name__ == '__main__':

    gps = GPSSensor('/dev/ttyAMA0', 9600)

    try:

        while True:

            data = gps.read()

            print('\n')

            #if data is not None:

                #lat, lon, alt, speed, num_sats, hdop = data

              #  print('Latitude: {}, Longitude: {}, Altitude: {}, Speed: {}, Num Sats: {}, HDOP: {}'.format(lat, lon, alt, speed, num_sats, hdop))

          

            time.sleep(1)

            

    

    except KeyboardInterrupt:

        gps.close()

        print('Bye.')

        

