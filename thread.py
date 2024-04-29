import cv2
import numpy as np
import time
import threading
import os

#Raspberry Pi Camera Command
# raspivid -t 0

cam = cv2.VideoCapture(1)

time_values = []
v_values = []

csv_counter = 0
csv_limit = 60

frame_counter = 0
frame_limit = 3600

def save_csv():
    global csv_counter
    if csv_counter < csv_limit:
        threading.Timer(60.0, save_csv).start()
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        print("Saving data to file " + timestamp)
        np.savetxt(f'./brightness_data_{timestamp}.csv', np.column_stack((time_values, v_values)), delimiter=',', header='Time,Average V (Brightness) Value')
        os.fsync(open(f'./brightness_data_{timestamp}.csv', 'a'))  # Add fsync after saving
        csv_counter += 1

# def save_frame():
#     global frame_counter
#     if frame_counter < frame_limit:
#         threading.Timer(1.0, save_frame).start()
#         timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
#         print("Saving frame to file " + timestamp)
#         ret, frame = cam.read() 
#         if ret:
#             cv2.imwrite(f'frame_{timestamp}.jpg', frame)  
        
# def save_frame():
#     global frame_counter
#     if frame_counter < frame_limit:
#         threading.Timer(1.0, save_frame).start()
#         timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
#         print("Saving frame to file " + timestamp)
#         ret, frame = cam.read()
#         if ret:
#             try:
#                 # Specify the directory where the file will be saved
#                 directory = "/home/payload/Desktop/Matt/cuinspace-payload-camera/frames"

#                 # Create the directory if it doesn't exist
#                 os.makedirs(directory, exist_ok=True)

#                 # Create a temporary filename with proper extension (e.g., '.jpg')
#                 temp_filename = os.path.join(directory, f'frame_{timestamp}.jpg.tmp')

#                 # Encode image using cv2.imencode
#                 ret2, image_data = cv2.imencode('.jpg', frame)
#                 # Check for encoding success
#                 if ret2:
#                     # Open the temporary file in binary write mode
#                     with open(temp_filename, 'wb') as f:
#                         f.write(image_data.tobytes())  # Write image data directly

#                     # Rename the temporary file to the final filename (atomic rename on some filesystems)
#                     os.rename(temp_filename, os.path.join(directory, f'frame_{timestamp}.jpg'))
#             except OSError as e:
#                 print(f"Error during image saving: {e}")
#             frame_counter += 1

def save_frame():
    global frame_counter
    if frame_counter < frame_limit:
        threading.Timer(1.0, save_frame).start()
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        print("Saving frame to file " + timestamp)
        ret, frame = cam.read()
        if ret:
            try:
                # Specify the directory where the file will be saved
                directory = "/home/payload/Desktop/Matt/cuinspace-payload-camera/frames"

                # Create the directory if it doesn't exist
                os.makedirs(directory, exist_ok=True)

                # Create a temporary filename with proper extension (e.g., '.jpg')
                temp_filename = os.path.join(directory, f'frame_{timestamp}.jpg.tmp')

                # Encode image using cv2.imencode
                ret2, image_data = cv2.imencode('.jpg', frame)
                # Check for encoding success
                if ret2:
                    # Open the temporary file in binary write mode
                    with open(temp_filename, 'wb') as f:
                        f.write(image_data.tobytes())  # Write image data directly
                        fd = f.fileno()
                        os.fsync(fd)

                    # Rename the temporary file to the final filename (atomic rename on some filesystems)
                    os.rename(temp_filename, os.path.join(directory, f'frame_{timestamp}.jpg'))

            except OSError as e:
                print(f"Error during image saving: {e}")
            frame_counter += 1

save_frame()
save_csv()

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
