import cv2
import numpy as np
import time
import threading

#Raspberry Pi Camera Command
# raspivid -t 0

cam = cv2.VideoCapture(1)

time_values = []
v_values = []

counter = 0
limit = 60

def save_file():
    global counter
    if counter < limit:
        threading.Timer(60.0, save_file).start()
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        print("Saving data to file " + timestamp)
        np.savetxt(f'./brightness_data_{timestamp}.csv', np.column_stack((time_values, v_values)), delimiter=',', header='Time,Average V (Brightness) Value')
        counter += 1
    
save_file()
while True:
    
    ret, frame = cam.read() 
    if not ret:
        print("Failed to grab frame")
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    v_values_masked = hsv[:, :, 2][mask > 0]
    average_v_masked = np.mean(v_values_masked)   
  
    time_values.append(len(time_values) + 1)
    v_values.append(average_v_masked)

# Save the plot data to a file
# Generate a timestamp for the filename
timestamp = time.strftime("%Y%m%d%H%M%S")

# Save the plot data to a new file with a timestamp in the filename
np.savetxt(f'./brightness_data_{timestamp}.csv', np.column_stack((time_values, v_values)), delimiter=',', header='Time,Average V (Brightness) Value')
print("Final Data saved to file, Goodbye!")
# Release the camera and close all OpenCV windows
cam.release() # release the camera
cv2.destroyAllWindows() # close the camera window
