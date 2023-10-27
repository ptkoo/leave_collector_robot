import smbus
import time

DEVICE_ID = 0x08

# Open a connection to the I2C bus
bus = smbus.SMBus(1)  # 1 indicates the I2C bus number (Raspberry Pi 2+)

try:
    # Send data to Arduino
    data_to_send = 17
    bus.write_byte(DEVICE_ID, data_to_send)
    print("Sent data:", data_to_send)

    # Wait for Arduino to process data (adjust delay based on your application)
    time.sleep(0.1)

    # Read data from Arduino
    received_data = bus.read_byte(DEVICE_ID)
    print("Data received:", received_data)

    if received_data == data_to_send:
        print("Success!")
    else:
        print("Mismatch! Data transfer unsuccessful.")

except Exception as e:
    print("Error:", str(e))

finally:
    # Close the connection to the I2C bus
    bus.close()

