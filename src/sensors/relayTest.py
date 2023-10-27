import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin number where your relay module is connected
relay_pin = 23

# Set the GPIO pin as an output pin
GPIO.setup(relay_pin, GPIO.OUT)

try:
	while True:
		# Turn on the relay (assuming the relay is active low)
		GPIO.output(relay_pin, GPIO.HIGH)
		print("Pump is OFF")
		time.sleep(5)  # Wait for 2 seconds
    

except KeyboardInterrupt:
    # If the user presses CTRL+C, cleanup and exit
    GPIO.cleanup()

finally:
    # Cleanup GPIO settings before exiting
    GPIO.cleanup()
