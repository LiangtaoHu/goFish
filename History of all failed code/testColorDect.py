import cv2
import time
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX 
ORANGE_MIN = np.array([0, 65, 0],np.uint8)
ORANGE_MAX = np.array([20, 255, 255],np.uint8)

prev_frame_time = 0
new_frame_time = 0
frameCount = 0

camera = cv2.VideoCapture('IMG_0357.mov')  
width = int(camera.get(3))
height = int(camera.get(4))
mask = np.zeros((height, width), dtype='uint8')
cv2.rectangle(mask, (80,40), (475,430), (255,255,255), -1)

#camera.set(3, 160)
#camera.set(4, 120)  

def filterAndMergeContours(contours):
    finalContours = []
    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > 15:
            finalContours.append(cnt)
    print(len(contours))
    print(len(finalContours))
    return np.vstack(finalContours) if len(finalContours) > 0 else np.array([[]])

while True:
    frameCount += 1
    existence, frame = camera.read()
    # TERMINATION CONDITIONS
    if cv2.waitKey(1) == ord('q'):
        break   
    croppedFrame = cv2.bitwise_and(frame, frame, mask=mask)
    croppedFrameCopy = croppedFrame.copy()
    hsv_image = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2HSV)
    frame_thres = cv2.inRange(hsv_image, ORANGE_MIN, ORANGE_MAX)
    # FIND AND DRAW CONTOURS
    #for i, cnt in enumerate(contours):
    #    if cv2.contourArea(cnt) > 5:
    #        cv2.drawContours(image=croppedFrameCopy, contours=filterAndMergeContours(contours), contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    contours, hierarchy = cv2.findContours(image=frame_thres, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(filterAndMergeContours(contours))
    cv2.polylines(croppedFrameCopy, [hull], True, (0,255,0), 1)
    m = cv2.moments(filterAndMergeContours(contours))
    cX = int(m["m10"] / m["m00"])
    cY = int(m["m01"] / m["m00"])
    cv2.circle(croppedFrameCopy, (cX, cY), 1, (0, 255, 0), 1)
    # FIND AND DISPLAYS REAL TIME FPS
    new_frame_time = time.time() 
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps) 
    fps = str(fps) 
    cv2.putText(croppedFrameCopy, str(frameCount), (7, 70), FONT, 3, (100, 255, 0), 3, cv2.LINE_AA) 
    print(frameCount)
    # FINAL OUTPUT
    #cv2.imshow("Filtered", frame_thres)
    cv2.imshow('Detection', croppedFrameCopy)
    #cv2.imshow("Original", frame)
camera.release()
cv2.destroyAllWindows()

