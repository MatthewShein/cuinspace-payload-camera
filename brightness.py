import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# Open the default camera
# Setting to 1 fixes "Failed to grab frame" idfk why
cam = cv2.VideoCapture(1)

# Initialize lists to store time and average V values
time_values = []
v_values = []

# Initialize plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(time_values, v_values)
ax.set_xlabel('Time')
ax.set_ylabel('Average V (Brightness) Value')

while True:
    # Capture frame-by-frame
    ret, frame = cam.read() # read the camera feed, ret (true or false) and frame (the actual frame captured by the camera)

    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for the blue color range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Extract the V component, hsv is a 3D array, the third dimension is the V component, so we can just extract it
    # V of HSV (which stands for Value) works in conjunction with saturation and describes the brightness or intensity of the color, from 0 to 100 percent, where 0 is completely black, and 100 is the brightest and reveals the most color
    v_values_masked = hsv[:, :, 2][mask > 0]

    # Calculate the average brightness (V value) for masked regions
    average_v_masked = np.mean(v_values_masked) 

    # Track the average brightness value over time
    time_values.append(len(time_values) + 1)
    v_values.append(average_v_masked)

    # Update plot
    line.set_xdata(time_values)
    line.set_ydata(v_values)
    ax.relim() 
    ax.autoscale_view()

    fig.canvas.draw() # draw the plot
    fig.canvas.flush_events() # update the plot
    
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)
    # Display the masked frame (optional)
    # cv2.imshow('Masked Frame', result)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the plot data to a file
# Generate a timestamp for the filename
timestamp = time.strftime("%Y%m%d%H%M%S")

# Save the plot data to a new file with a timestamp in the filename
np.savetxt(f'./brightness_data_{timestamp}.txt', np.column_stack((time_values, v_values)), delimiter=',', header='Time,Average V (Brightness) Value')

# Release the camera and close all OpenCV windows
cam.release() # release the camera
cv2.destroyAllWindows() # close the camera window
plt.close(fig) # close the plot