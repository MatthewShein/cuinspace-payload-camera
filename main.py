import numpy as np
import cv2

print(cv2.__version__)

cam = cv2.VideoCapture(0)

cv2.namedWindow("Python Webcam App")

img_counter = 0

while True:
    ret,frame = cam.read()
    width = int(cam.get(3))
    height = int(cam.get(4))

    if not ret:
        print("failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Bitwise mask, to only get blues
    # 1 1 = 1
    # 0 1 = 0
    # 1 0 = 0
    # 0 0 = 0

    cv2.imshow("Test",result)
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)

    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Escape hit, closing app")
        break

    elif k%256 == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("Screenshot taken")
        img_counter+=1


cam.release()
cv2.destroyAllWindows()

#BGR_color = np.array([[[255,0,0]]])
#print(cv2.cvtColor(BGR_color, cv2.COLOR_BGR2HSV)) #printing one pixel