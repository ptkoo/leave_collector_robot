import time
import sys
sys.path.append('..')

from sensors.gyroscope_sensor import GyroscopeSensor
from sensors.magnetometer import runMag


 
# this is the initial uncertaintyPrevious , kalmanUncertainty = uncertaintyPrevious + deltaTime **2 4*4, deltaTime **2 4*4 is process noise covariance
kalmanUncertaintyAngle = 2*2  # uncertainty of the initial , so this is uncertaintyPrevious
kalmanState = 0  # set the initial angle to zero


def angleDifference(kalmanMeasurement, kalmanState):
	diff = kalmanMeasurement - kalmanState 
	if ((kalmanMeasurement >= 0 and kalmanMeasurement <= 90 ) and (kalmanState >= 270 and kalmanState <= 360 )) or ((kalmanState >= 0 and kalmanState <= 90 ) and (kalmanMeasurement >= 270 and kalmanMeasurement <= 360 )):
		if ( diff > 0 ): 
			return 360 - diff
		elif ( diff < 0 ) :
			return 360 + diff
	else: 
		return abs(diff) 

# kalman Input is gyroscope yaw angle, kalmanMeasurement is magnetometer yaw angle. 
# kalman Input is the predicted state based on previous state and and physical model in our case, we alrdy did that with gyro.


def kalmanfilter(kalmanState, predictUncertainty , kalmanPredict, kalmanMeasurement):
    # Predict the current State
    kalmanState = (0.5 * kalmanPredict ) % 360 
    #print(kalmanInput)
    
    # Calculate the uncertainty
    predictUncertainty = predictUncertainty + 0.5 * 0.5 * 2.5 * 2.5  # kalmanUncertainty = uncertaintyPrevious + deltaTime ** 2 * 4 * 4, deltaTime ** 2 * 4 * 4 is process noise covariance
    
    # Calculate Kalman Gain
    kalmanGain = predictUncertainty / (predictUncertainty + 2 * 2)  # 3 * 3 is the variance angle of magnetometer
    
    # Angle wrapping 
    error = angleDifference(kalmanMeasurement, kalmanState)
    
    #print("Error", error)
    # Update the predicted state and wrap it to [0, 360) range
    kalmanState = (kalmanState + kalmanGain * error) % 360 
    
    # Update uncertainty
    predictUncertainty = (1 - kalmanGain) * predictUncertainty
    
    return kalmanState, predictUncertainty



gyro = GyroscopeSensor()
offset = runMag()



while True:
	print("Offset",offset)
	x_anglularRate, y_angle, z_angle = gyro.runGyro()
	
	
	#print("X Angle: {:.2f} degrees".format(x_anglularRate))
	#print("Y Angle: {:.2f} degrees".format(y_angle))
	#print("Z Angle: {:.2f} degrees".format(z_angle))
	#print("\n")
	
	magAngle = runMag() - offset
	
	if magAngle<0:
		yawAngleMag = 360 + magAngle
		
	else:
		 yawAngleMag = magAngle
	
	
	print("X Angle from Mag", yawAngleMag)
	
	optimalYawAngle, uncertainty = kalmanfilter(kalmanState, kalmanUncertaintyAngle, x_anglularRate, yawAngleMag)  
	
	print("Yaw Angle", optimalYawAngle)
	
	#print("Uncertainty", uncertainty)
	
	print("\n")
	
	time.sleep(0.5)

