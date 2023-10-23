import smbus		#import SMBus module of I2C
from time import sleep  #import sleep
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse
import numpy as np

#some MPU6050 Registers and their Address
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register
declination = -0.0151261874        #define declination angle of location where measurement going to be done
pi          = 3.14159265359     #define pi value

# Initialize a list to store raw data samples
x_raw_samples = []
y_raw_samples = []
z_raw_samples = []

# Calibrate sample

x_calibrated_samples = []
y_calibrated_samples = []
z_calibrated_samples = []

# This is the calibration data for transformation matrix 
x_calibrated_samples1 = []
y_calibrated_samples1 = []
# bias
x_raw_bias = 0
y_raw_bias = 0
z_raw_bias = 0

def Magnetometer_Init():
        #write to Configuration Register A
        bus.write_byte_data(Device_Address, Register_A, 0x70)

        #Write to Configuration Register B for gain
        bus.write_byte_data(Device_Address, Register_B, 0xa0)

        #Write to mode Register for selecting mode
        bus.write_byte_data(Device_Address, Register_mode, 0)
	
	

def read_raw_data(addr):
    
        #Read raw 16-bit value
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from module
        if(value > 32768):
            value = value - 65536
        return value

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
   

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson) #small radius (major)
    ell_radius_y = np.sqrt(1 - pearson) #large radius (minor)
    
    ellipse = Ellipse((0, 0), width = ell_radius_x *2, height = ell_radius_y *2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    
    transf = transforms.Affine2D() \
       .rotate_deg(0) \
       .scale(scale_x, scale_y)

    ellipse.set_transform(transf + ax.transData)
   
    # Calculate width and height of transformed ellipse

    width_transformed = ell_radius_x*2* scale_x
    height_transformed = ell_radius_y*2* scale_y

    # Get the transformation matrix
    TandT_matrix = transf.get_matrix()
    
    #print(TandT_matrix)
    transformationMatrix = TandT_matrix[:2, :2]  # Extract 2x2 transformation matrix
    
    # Extract translation matrix
    translationMatrix = TandT_matrix[:2, 2:]
    #print("Transformation Matrix\n", transformationMatrix)
    #print("Translation Matrix\n", translationMatrix)
    
    # Calculate the major and minor axes endpoints in data coordinates
    major_axis_endpoints_data = np.array([[ell_radius_x , 0], [-ell_radius_x, 0]])
    minor_axis_endpoints_data = np.array([[0, ell_radius_y], [0, -ell_radius_y]])

    
    # Apply the transformation matrix to the endpoints
    major_axis_endpoints_transformed = np.dot(major_axis_endpoints_data, transformationMatrix)  + translationMatrix.T
    minor_axis_endpoints_transformed = np.dot(minor_axis_endpoints_data, transformationMatrix) + translationMatrix.T
        
    
    #print("Major Axis\n", major_axis_endpoints_transformed)
    #print("Minor Axis\n", minor_axis_endpoints_transformed)
    
    # Extract the transformed endpoints
    major_axis_endpoint1, major_axis_endpoint2 = major_axis_endpoints_transformed
    minor_axis_endpoint1, minor_axis_endpoint2 = minor_axis_endpoints_transformed


    
    return ax.add_patch(ellipse), width_transformed, height_transformed , major_axis_endpoint1, major_axis_endpoint2, minor_axis_endpoint1, minor_axis_endpoint2
    
def calibrate():
        print( " Calcuting bias... " )
        # Read 1000 samples of raw data
        for _ in range(500):
            x_raw = read_raw_data(X_axis_H)
            y_raw = read_raw_data(Y_axis_H)
            z_raw = read_raw_data(Z_axis_H)

            # Append raw data to the sample lists
            x_raw_samples.append(x_raw)
            y_raw_samples.append(y_raw)
            z_raw_samples.append(z_raw)

            # Calculate mean of raw data samples
            x_raw_bias = sum(x_raw_samples) / len(x_raw_samples)
            y_raw_bias = sum(y_raw_samples) / len(y_raw_samples)
            z_raw_bias = sum(z_raw_samples) / len(z_raw_samples)

                
            # Append Calibrated data to the calibrated lists
            x_calibrated_samples.append(x_raw - x_raw_bias )
            y_calibrated_samples.append(y_raw - y_raw_bias )
            z_calibrated_samples.append(z_raw - z_raw_bias )
            
            
            sleep(0.1)
            
        print("Calibrated")   
        
        # X sensitivity scale factor
        
        x_sen_fact = max(1, abs((max(x_calibrated_samples)- 0 ) / (min(x_calibrated_samples) - 0)))
        y_sen_fact = max(1, abs((max(y_calibrated_samples)- 0 ) / (min(y_calibrated_samples) - 0)))
     

        
        sens_vec = np.array([[x_sen_fact, 0], [0, y_sen_fact]])
        
        # Plot the confidence ellipse with 3 standard deviations
        ax = plt.gca()
        ellipse, width, height, major_axis_endpoint1, major_axis_endpoint2, minor_axis_endpoint1, minor_axis_endpoint2= confidence_ellipse(x_calibrated_samples, y_calibrated_samples, ax, n_std=2.5, edgecolor='red', linewidth=2)
     
        # Get the center point and orientation angle of the ellipse
        ellipse_center = ellipse.center
        # orientation_rad = np.arctan2(height, width)

        
        
        
       # Plot rotated major axis (in blue) and minor axis (in green)
        ax.plot([major_axis_endpoint1[0], major_axis_endpoint2[0]],
                [major_axis_endpoint1[1], major_axis_endpoint2[1]], color='blue', linestyle='--', label='Major Axis')

        ax.plot([minor_axis_endpoint1[0], minor_axis_endpoint2[0]],
                [minor_axis_endpoint1[1], minor_axis_endpoint2[1]], color='green', linestyle='--', label='Minor Axis')


        # Plot the center point
        plt.plot(ellipse_center[0], ellipse_center[1], marker='o', markersize=8, color='yellow', label='Ellipse Center')

        ax.scatter(x_raw_samples, y_raw_samples, c='b', marker='o')
        ax.scatter(x_calibrated_samples, y_calibrated_samples , c='r', marker='o', label='Calibrated Data')
        
        # So, we are morphing into circle from the ellipse.
       
        # Scale factor
        #scale_factor = width / height
        major_axis_length = major_axis_endpoint1[0] - major_axis_endpoint2[0]
        minor_axis_length = minor_axis_endpoint1[1] - minor_axis_endpoint2[1]
        scale_factor = abs(major_axis_length / minor_axis_length)
        if (major_axis_length > minor_axis_length):
                
                scaleMatrix = np.array([[1/scale_factor, 0], [0, 1]])
        else: 
                
                scaleMatrix = np.array([[1, 0], [0, scale_factor]])
                
                
       # print(major_axis_length)
        #print(minor_axis_length)
        #print(scaleMatrix)
        #print(major_axis_endpoint1)
        #print(major_axis_endpoint2)
       # print(minor_axis_endpoint1)
        #print(minor_axis_endpoint2)
        
        
        
       
       # for x in x_calibrated_samples:
                #x_calibrated_samples1.append(x / scale_factor)
        
        # Transfoming ellipse into circle
        
        # Create Rotational Matrix
        c, s = np.cos(0), np.sin(0)
        rotationalMatrix = np.array([[c, s], [-s, c]])

        # Create Reverse Rotational Matrix
        inverse_rotation_matrix = rotationalMatrix.T
        
        soft_factor = rotationalMatrix @ scaleMatrix @ inverse_rotation_matrix  @ sens_vec
        
        for x_calibrated, y_calibrated in zip(x_calibrated_samples, y_calibrated_samples):
                
                # Create a 2 x 1 matrix with x and y as elements
                vectorMatrix = np.array([[x_calibrated,0], [0,y_calibrated]])
                
                # Perform matrix multiplication: Reverse Rotation Matrix * Scale Matrix * Rotation Matrix * Vector Matrix
               
                resultMatrix = vectorMatrix @ soft_factor
                
                # Extract individual elements from the result matrix
                x_calibrated_samples1.append(resultMatrix[0, 0] ) # First element (x value)
                y_calibrated_samples1.append(resultMatrix[1, 1] ) # Second element (y value)
                
        
        ellipse1 = confidence_ellipse(x_calibrated_samples1, y_calibrated_samples1, ax, n_std=2.5, edgecolor='green', linewidth=2)
        ellipse_center1 = ellipse.center
        # Plot the center point
        plt.plot(ellipse_center1[0], ellipse_center[1], marker='o', markersize=8, color='yellow', label='Ellipse Center')
        ax.scatter(x_calibrated_samples1, y_calibrated_samples1 , c='c', marker='o', label='Calibrated Data')
        plt.xlim(-1000, 1000)  
        plt.ylim(-1000, 1000)  

        ax.set_xlabel('X Raw')
        ax.set_ylabel('Y Raw')
        # Show legend
        plt.legend()
        plt.show()
        

        # We return this so that we can calibrate the raw data. These results came from the transformation and bias calculation
        return x_raw_bias, y_raw_bias, soft_factor
        
        

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e   # HMC5883L magnetometer device address

Magnetometer_Init()     # initialize HMC5883L magnetometer 

# Assigning to global variables 

#x_raw_bias, y_raw_bias, soft_factor = calibrate()


soft_factor = np.array([[1, 0], [0, 0.84465789]])
x_raw_bias = 53.148
y_raw_bias = -48.19

#print(soft_factor)
#print(x_raw_bias, y_raw_bias)

#while True:

def runMag():
	
        #Read magnetometer raw value
        
        x_raw = read_raw_data(X_axis_H) 
        y_raw = read_raw_data(Y_axis_H) 
        z_raw = read_raw_data(Z_axis_H) 
        
        
        # Read Calibrated Accelerometer value

        x_calibrated = x_raw - x_raw_bias
        y_calibrated = y_raw - y_raw_bias
        z_calibrated = z_raw - z_raw_bias
        
       
        # Create a 2 x 1 matrix with x and y as elements
        vectorMatrix = np.array([[x_calibrated,0], [0,y_calibrated]])
        
       

        # Perform matrix multiplication: Reverse Rotation Matrix * Scale Matrix * Rotation Matrix * Vector Matrix
        resultMatrix = vectorMatrix @ soft_factor
        
      

        # Extract individual elements from the result matrix
        x = resultMatrix[0, 0]  # First element (x value)
        y = resultMatrix[1, 1]  # Second element (y value)

        

        heading =  math.atan2(x,y) 
        
        #Due to declination check for >360 degree
        if(heading > 2*pi):
                heading = heading - 2*pi

        #check for sign
        if(heading < 0):
                heading = heading + 2*pi

        #convert into angle
        heading_angle = int(heading * 180/pi) 
        
        #print ("Heading Angle = %d°" %heading_angle)
        return heading_angle
        
 #       sleep(0.5)
 
if __name__ == "__main__":
         while True:
                runMag()
                sleep(0.5)
