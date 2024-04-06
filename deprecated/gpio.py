import RPi.GPIO as GPIO
import time
import keyboard

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Function to turn on the light
def turn_on_light():
    GPIO.output(18, GPIO.HIGH)
    print("Light on")

# Function to turn off the light
def turn_off_light():
    GPIO.output(18, GPIO.LOW)
    print("Light off")

# Main program
try:
    while True:
        print("Waiting for spacebar press...")
        keyboard.wait('space')
        turn_on_light()

        print("Waiting for spacebar release...")
        keyboard.wait('space')
        turn_off_light()
    
except KeyboardInterrupt:
    # Clean up GPIO on program exit
    print("Exiting program")
    GPIO.cleanup()