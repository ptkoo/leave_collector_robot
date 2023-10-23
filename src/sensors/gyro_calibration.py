import smbus
from time import sleep

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

bus = smbus.SMBus(1)
Device_Address = 0x68

def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 8)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

gyro_cali_x = 0.0
gyro_cali_y = 0.0
gyro_cali_z = 0.0


if __name__ == "__main__":
    MPU_Init()
    gyro_scale = 65.5  # Sensitivity scale factor for ±500 dps range

    print("Reading MPU6050...")

    for _ in range(2000):
        gyro_cali_x += read_raw_data(GYRO_XOUT_H) / gyro_scale
        gyro_cali_y += read_raw_data(GYRO_YOUT_H) / gyro_scale
        gyro_cali_z += read_raw_data(GYRO_ZOUT_H) / gyro_scale

        sleep(0.01)  # Sampling rate of 1 Hz

    gyro_cali_x /= 2000
    gyro_cali_y /= 2000
    gyro_cali_z /= 2000

    print("x calibrated values:", gyro_cali_x)
    print("y calibrated values:", gyro_cali_y)
    print("z calibrated values:", gyro_cali_z)
