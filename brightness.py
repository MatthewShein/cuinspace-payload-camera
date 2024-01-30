import cv2
import numpy as np
import matplotlib.pyplot as plt

# Open the default camera
cam = cv2.VideoCapture(0)

# Initialize lists to store time and average V values
time_values = []
v_values = []

# Initialize plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(time_values, v_values)
ax.set_xlabel('Time')
ax.set_ylabel('Average V Value')

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()

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

    # Extract the V component
    v_values_masked = hsv[:, :, 2][mask > 0]

    # Calculate the average V value for masked regions
    average_v_masked = np.mean(v_values_masked)

    # Track the average V value over time
    time_values.append(len(time_values) + 1)
    v_values.append(average_v_masked)

    # Update plot
    line.set_xdata(time_values)
    line.set_ydata(v_values)
    ax.relim()
    ax.autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()
    
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)
    # Display the masked frame (optional)
    # cv2.imshow('Masked Frame', result)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
