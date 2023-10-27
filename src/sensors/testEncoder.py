import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the motor pins
IN1 = 28
IN2 = 30
ENA = 3

# Define the pulse counter variable
pulse_count = 0

# Set the motor pins as output
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Set up the GPIO input pin for the motor encoder
MOTOR_ENCODER_PIN = 2  # Replace with your actual GPIO pin number for the motor encoder
GPIO.setup(MOTOR_ENCODER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create a PWM object for controlling the motor speed
pwm = GPIO.PWM(ENA, 20000)  # Frequency 20 kHz

# Interrupt callback function to count pulses
def motor_encoder_callback(channel):
    global pulse_count
    pulse_count += 1

# Add event detection to the motor encoder pin
GPIO.add_event_detect(MOTOR_ENCODER_PIN, GPIO.FALLING, callback=motor_encoder_callback)

try:
    # Start the PWM with a duty cycle of 50%
    pwm.start(50)

    while True:
        # Set the motor direction (clockwise)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        
        # Print the pulse count
        print("Pulse Count:", pulse_count)
        
    

    # Stop the motor
    pwm.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

finally:
    # Stop PWM
    pwm.stop()

    # Cleanup the GPIO pins
    GPIO.cleanup()
