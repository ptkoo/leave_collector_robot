import serial
import pynmea2
import time
import io

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


while 1:
    try:
        line = sio.readline()
        if line:
            msg = pynmea2.parse(line)
            print(repr(msg))
            print (msg.latitude)
            print (msg.longitude)
    except KeyboardInterrupt:
        print('Bye.')
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
    except ValueError:
        print('Invalid checksum in the sentence.')
        continue
    time.sleep(0.1)