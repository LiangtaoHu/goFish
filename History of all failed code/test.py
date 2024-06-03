# SET UP LIBRARIES
from ultralytics import YOLO
import keyboard
import cv2
import math
# SET UP CAMERA, USING MAIN CAMERA AND THEN SETTING THE WIDTH AND LENGTH
camera = cv2.VideoCapture(0)
WIDTH = 640
HEIGHT = 480
camera.set(3, WIDTH)
camera.set(4, HEIGHT)
# LOAD IN MODEL
fishModel = YOLO("C:/Users/Liangtao Hu/Documents/my personal items/SeniorResearch/best3n.pt")
print("FINISHED SETUP")
while True:
    existence, frame = camera.read() # Get two values, if the frame even exists and the image array vector.
    results = fishModel(frame, stream=True, verbose=False) # Get detection results on image and do it efficently via stream=True param. Includes ALL detected objects. (doesn't matter for us cus we're just gonna have one fish.)
    for result in results:
        boxes = result.boxes
        if len(boxes) == 0:
            continue
        # FIND MOST CONFIDENT BOX
        allConfs = [box.conf for box in boxes]
        maxConf = max(allConfs)
        if maxConf < 0.2:
            continue
        index = allConfs.index(maxConf)
        box = boxes[index]
        coords = [int(x) for x in box.xyxy[0]]
        boxCenter = ((coords[0]+coords[2])/2, (coords[1]+coords[3])/2)
        angle = math.atan2(HEIGHT/2-boxCenter[1], boxCenter[0]-WIDTH/2)
        if angle < 0: 
            angle += (math.pi*2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if not(boxCenter[0] > 64 and boxCenter[0] < 576 and boxCenter[1] < 416 and boxCenter[1] > 64):
            print(angle)
        cv2.rectangle(frame, (64, 64), (576, 416), (255, 0, 0), 1)
        cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (255, 0, 0), 5)
        cv2.putText(frame, str(maxConf), [coords[0], coords[1]], font, 1, (0,0,0), 5)
        cv2.circle(frame, (int(boxCenter[0]), int(boxCenter[1])), 5, (255,0,0), 5)
        cv2.line(frame, (int(boxCenter[0]), int(boxCenter[1])), (int(WIDTH/2), int(HEIGHT/2)), (255, 0, 0), 5)
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    # if keyboard.is_pressed('esc'):
    #     camera.release()
    #     cv2.destroyAllWindows()
    #     exit()
camera.release()
cv2.destroyAllWindows()