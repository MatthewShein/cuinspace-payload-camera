import cv2
import numpy as np
import time
import threading
import os
import RPi.GPIO as GPIO

#Setup GPIO
ledPin = 22
ledState = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

camera = cv2.videoCapture(0)
time_values = []
brightness_values = []
csv_counter = 0
csv_limit = 100
frame_counter = 0
frame_limit = 9999

def save_csv():
    global csv_counter
    if len(brightness_values) < 1:
        return
    if csv_counter < csv_limit:
        threading.Timer(60.0, save_csv).start()
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        print("Saving data to file " + timestamp)
        np.savetxt(f'./brightness_data_{timestamp}.csv', np.column_stack((time_values, brightness_values)), delimiter=',', header='Time,Average Brightness Value')
        os.fsync(open(f'./brightness_data_{timestamp}.csv', 'a'))  # Add fsync after saving
        csv_counter += 1

def save_frame():
    global frame_counter
    if frame_counter < frame_limit:
        threading.Timer(1.0, save_frame).start()
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        print("Saving frame to file " + timestamp)
        ret, frame = camera.read()
        if ret:
            try:
                # Specify the directory where the file will be saved
                directory = "/home/payload/Desktop/Matt/cuinspace-payload-camera/frames"

                # Create the directory if it doesn't exist
                os.makedirs(directory, exist_ok=True)
                temp_filename = os.path.join(directory, f'frame_{timestamp}.jpg.tmp')
                ret2, image_data = cv2.imencode('.jpg', frame)
                if ret2:
                    with open(temp_filename, 'wb') as f:
                        f.write(image_data.tobytes())
                        fd = f.fileno()
                        os.fsync(fd)
                    os.rename(temp_filename, os.path.join(directory, f'frame_{timestamp}.jpg'))
            except Exception as e:
                print(f'Error saving frame: {e}')
        frame_counter += 1

try: 
    GPIO.output(ledPin, GPIO.HIGH)
    ledState = True
    print("Light on")
    ret, frame = camera.read()
    print("Initating camera")
    time.sleep(10)
    print("Camera initiated")
    save_frame()
    save_csv()
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture image")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        brightness = hsv[:,:,2]
        average_brightness = np.mean(brightness)
        time_values.append(len(time_values)+1)
        print(f"Average brightness: {average_brightness}")
        brightness_values.append(average_brightness)
except KeyboardInterrupt:
    timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    np.savetxt(f'./brightness_data_{timestamp}.csv', np.column_stack((time_values, brightness_values)), delimiter=',', header='Time,Average Brightness Value')
    print("Data saved to file, Turning off!")
    camera.release()
    cv2.destroyAllWindows()
    GPIO.output(ledPin, GPIO.LOW)
    ledState = False
    GPIO.cleanup()
    print("Light off")