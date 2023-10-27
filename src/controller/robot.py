import smbus2 as smbus
from adafruit_servokit import ServoKit

def StrTobytes(src: str):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

import math
import time

from controller.pid import pid_forward

class Robot:
    def __init__(self, sDriverType=16, arduinoAdd=0x08):
        self.L_speed = 80
        self.R_speed = 80
        
        self.ser_kit = ServoKit(channels=sDriverType)
        self.servo = [0, 0, 0, 0]
        self.for_angle = [100, 100, 100, 90]

        self.I2Cadd = arduinoAdd
        self.I2Cbus = smbus.SMBus(1)

        self.mx_speed = 255

        self.prev_error = 0
        self.sum_error = 0
        self.prev_time = -1

    def set_mxSpeed(self, mx_speed: int):
        # Set new max speed according to the system PWM
        self.mx_speed = mx_speed

    def set_servo_pins(self, font_l: int, font_r: int, back_l: int, back_r: int):
        # Set each servo pin from Servo Driver
        self.servo[0] = font_l
        self.servo[1] = font_r
        self.servo[2] = back_l
        self.servo[3] = back_r

    def SendData(self):
        try:
                package = "-".join([str(int(self.L_speed)), str(int(self.R_speed))])
                #print(package)
                package = StrTobytes(package)
                #print(package)
                package = smbus.i2c_msg.write(self.I2Cadd, package)
                # Sending the data via I2C to arduino Mega
                self.I2Cbus.i2c_rdwr(package)
        except:
                pass

    def set_servos_angle(self, angles: list, degree = True):
            
        setpoint = False
        if angles is self.for_angle:
                setpoint = True
            
        for i, angle in enumerate(angles):
            if not degree:
                angle = angle*(180/math.pi)
            self.ser_kit.servo[self.servo[i]].angle = self.for_angle[i] + angle if not setpoint else angle

    def set_speeds(self, L: int, R: int):
        self.L_speed = L
        self.R_speed = R
        
        self.SendData()

    
    def forward(self, pos: int, tar: int, k: list = [1, 0, 0]):

        # The robot use positive and negative of 180 degree system
        # RHS is the positive angle and LHS is the negative angle
        if tar > 180:
            tar = tar - 360
    
        if pos > 180:
            pos = pos - 360

        # Get time for each iteration
        delta_time = 1
        if self.prev_time != -1:
            delta_time = time.time() - self.prev_time
        self.prev_time = time.time()

        # PID calculation
        P = tar - pos # (+) need more left speed, (-) need to more right speed
        I = (self.sum_error + P) * delta_time if self.prev_time != -1 else 0
        D = (P - self.prev_error) / delta_time if self.prev_time != -1 else 0

        # Sum error and mem prev error
        self.sum_error += P
        self.prev_error = P

        # Call the pid function to get new speed and direction
        # k[0] = Kp | k[1] = Ki | k[2] = Kd
        ML, MR = pid_forward(
            self.L_speed,
            self.R_speed,
            self.mx_speed,
            P*k[0],
            I*k[1],
            D*k[2]
        )

        self.L_speed = ML
        self.R_speed = MR

        self.SendData()
