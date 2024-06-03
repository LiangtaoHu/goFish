import cv2
import time
import numpy as np
import math

FONT = cv2.FONT_HERSHEY_SIMPLEX 
ORANGE_MIN = np.array([0, 65, 0],np.uint8)
ORANGE_MAX = np.array([20, 255, 255],np.uint8)
WIDTH = 640
HEIGHT = 480

prev_frame_time = 0
new_frame_time = 0

camera = cv2.VideoCapture(0)  
camera.set(3, WIDTH)
camera.set(4, HEIGHT)

mask = np.zeros((HEIGHT, WIDTH), dtype='uint8')
print(WIDTH-HEIGHT)
cv2.rectangle(mask, (80,0), (560,HEIGHT), (255,255,255), -1) 

def filterAndMergeContours(contours):
    finalContours = []
    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > 15:
            finalContours.append(cnt)
    return np.vstack(finalContours)

while True:
    existence, frame = camera.read()
    # TERMINATION CONDITIONS
    if cv2.waitKey(1) == ord('q'):
        break
    croppedFrame = cv2.bitwise_and(frame, frame, mask=mask)
    croppedFrameCopy = croppedFrame.copy()
    hsv_image = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2HSV)
    frame_thres = cv2.inRange(hsv_image, ORANGE_MIN, ORANGE_MAX)
    contours, hierarchy = cv2.findContours(image=frame_thres, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(filterAndMergeContours(contours))

    cv2.polylines(croppedFrameCopy, [hull], True, (0,255,0), 1)
    m = cv2.moments(filterAndMergeContours(contours))
    cX = int(m["m10"] / m["m00"])
    cY = int(m["m01"] / m["m00"])
    cv2.circle(croppedFrameCopy, (cX, cY), 1, (0, 255, 0), 1)

    # CHECK IF ITS ON THE BORDER.
    # VISUALIZE THE BORDER.
    # cv2.rectangle(croppedFrameCopy, (128, 48), (512, 432), (255, 0, 0), 2)
    if (cX > 512 or cX < 128) and (cY > 432 or cY < 48):
        angle = math.atan2(HEIGHT/2 - cY, cX-WIDTH/2)
        if angle < 0: 
            angle += (math.pi*2)
        print(angle)
    # FIND AND DISPLAYS REAL TIME FPS
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps) 
    fps = str(fps) 
    cv2.putText(croppedFrameCopy, fps, (7, 70), FONT, 3, (100, 255, 0), 3, cv2.LINE_AA) 

    cv2.imshow('Detection', croppedFrameCopy)

camera.release()
cv2.destroyAllWindows()