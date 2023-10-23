import smbus
from time import sleep
import math
import RPi.GPIO as GPIO
import sys

class GyroscopeSensor:
    def __init__(self):
        self.PWR_MGMT_1 = 0x6B
        self.SMPLRT_DIV = 0x19
        self.CONFIG = 0x1A
        self.GYRO_CONFIG = 0x1B
        self.INT_ENABLE = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47

        self.Device_Address = 0x68
        self.bus = smbus.SMBus(1)

        self.gyro_scale = 65.5  # Sensitivity scale factor for ±500 dps (deg/s) range
        self.dt = 0.3  # Time interval in seconds (sampling rate of 2 Hz)
        self.x_calibrated_value = -3.9352595419847227
        self.y_calibrated_value = -1.2961908396946593
        self.z_calibrated_value = -1.6157633587786213

        self.x_angular = 0.0
        self.y_angular = 0.0
        self.z_angular = 0.0

        self.MPU_Init()

    def MPU_Init(self):
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 5)  # low pass filter
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 8)  # scale factor of 65.5 LSB/deg/s
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)
        value = ((high << 8) | low)
        if value > 32768:
            value = value - 65536
        return value

    def runGyro(self):
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H)
        gyro_y = self.read_raw_data(self.GYRO_YOUT_H)
        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)

        gyro_x_scaled = (gyro_x / self.gyro_scale) - self.x_calibrated_value
        gyro_y_scaled = (gyro_y / self.gyro_scale) - self.y_calibrated_value
        gyro_z_scaled = (gyro_z / self.gyro_scale) - self.z_calibrated_value

        self.x_angular += gyro_x_scaled 
        self.y_angular += gyro_y_scaled 
        self.z_angular += gyro_z_scaled 

        x_angle1 = (self.x_angular *  self.dt) % 360
        y_angle1 = (self.y_angular *  self.dt) % 360
        z_angle1 = (self.z_angular *  self.dt) % 360

        print("X Angle: {:.2f} degrees from gyro".format(x_angle1))
        #print("Y Angle: {:.2f} degrees".format(gyro_x_scaled))
        #print("Z Angle: {:.2f} degrees".format(z_angle1))
        #print("\n")

        return self.x_angular, x_angle1, z_angle1, 


if __name__ == "__main__":
    gyro_sensor = GyroscopeSensor()
    print("Reading MPU6050...")
    while True:
        gyro_sensor.runGyro()
        sleep(gyro_sensor.dt)
        

