import time
import sys
sys.path.append('..')

from sensors.gyroscope_sensor import GyroscopeSensor
from sensors import gyro_calibration
from sensors.magnetometer import runMag


 
# this is the initial uncertaintyPrevious , kalmanUncertainty = uncertaintyPrevious + deltaTime **2 4*4, deltaTime **2 4*4 is process noise covariance
kalmanUncertaintyAngle = 2*2  # uncertainty of the initial , so this is uncertaintyPrevious
kalmanState = 0  # set the initial angle to zero


def angleDifference(kalmanMeasurement, kalmanState):
	diff = kalmanMeasurement - kalmanState 
	if ((kalmanMeasurement >= 0 and kalmanMeasurement <= 90 ) and (kalmanState >= 270 and kalmanState <= 360 )):
	    return (360 + diff)
	    
	elif ((kalmanState >= 0 and kalmanState <= 90 ) and (kalmanMeasurement >= 270 and kalmanMeasurement <= 360 )):
	    return (360 - diff)
		
	else:
	    return abs(diff) 

# kalman Input is gyroscope yaw angle, kalmanMeasurement is magnetometer yaw angle. 
# kalman Input is the predicted state based on previous state and and physical model in our case, we alrdy did that with gyro.


def kalmanfilter(predictUncertainty , kalmanPredict, kalmanMeasurement):
    # Predict the current State
    #kalmanState = (0.5 * kalmanPredict ) % 360 
    #print(kalmanInput)
    
    # Calculate the uncertainty
    # predictUncertainty = predictUncertainty + 0.5 * 0.5 * 2 * 2  # kalmanUncertainty = uncertaintyPrevious + deltaTime ** 2 * 4 * 4, deltaTime ** 2 * 4 * 4 is process noise covariance
    
    # Calculate Kalman Gain
    kalmanGain = predictUncertainty / (predictUncertainty + 6 * 6)  # is the variance angle of magnetometer
    
    # Angle wrapping 
    error = angleDifference(kalmanMeasurement, kalmanPredict)
    
    # print("Error", error)
    # Update the predicted state and wrap it to [0, 360) range
    kalmanPredict = (kalmanPredict + (kalmanGain * error)) % 360 
    
    # Update uncertainty
    predictUncertainty = ((1 - kalmanGain) * predictUncertainty) +(0.0001) 
    
    return kalmanPredict, predictUncertainty
    
    
x, y, z = gyro_calibration.get_cali()


class Kalman_Yaw:
    def __init__(self):
        self.gyro = GyroscopeSensor(x, y, z)
        self.offset = runMag()
        self.reset = False
	
    def get_yaw(self):
        x_anglularRate, y_angle, z_angle = self.gyro.runGyro()
        initialKalmanPredict = (0.2 * x_anglularRate) % 360
        magAngle = runMag() - self.offset
        if magAngle < 0:
            yawAngleMag = 360 + magAngle
        else:
            yawAngleMag = magAngle
	    
        optimalYawAngle, uncertainty = kalmanfilter(kalmanUncertaintyAngle, initialKalmanPredict, yawAngleMag)
	
        print("YAW: ", optimalYawAngle)
        return optimalYawAngle
    
    def re_initialize(self):
        del self.gyro
        del self.offset
	
        self.gyro = GyroscopeSensor(x, y, z)
        self.offset = runMag()
    
    

'''
gyro = GyroscopeSensor()
offset = runMag()

while True:
    
    print("Offset", offset)
    
    x_anglularRate, y_angle, z_angle = gyro.runGyro()
    
    # Predict the current State
    initialKalmanPredict = (0.2 * x_anglularRate) % 360 
    
    magAngle = runMag() - offset
    
    if magAngle < 0:
        yawAngleMag = 360 + magAngle
    else:
        yawAngleMag = magAngle
    
    print("X Angle from Mag", yawAngleMag)
    
    optimalYawAngle, uncertainty = kalmanfilter(kalmanUncertaintyAngle, initialKalmanPredict, yawAngleMag)  
    
    print("Yaw Angle", optimalYawAngle)
    
    print("\n")
    
    time.sleep(0.2)
'''
