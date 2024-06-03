import threading
import serial
import cv2
import numpy as np
import math
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
readSerialValue = ""
angle = 10

class SerialReaderThread(threading.Thread):
    def __init__(self):
        self.j = 0
        super().__init__()
        self.stopCond = threading.Event() #Intially Event will basically be the equivalent of False
    def run(self):
        global angle, readSerialValue
        # This overrides the run function and a thread only calls this ONCE!!!
        while not self.stopped():
            if readSerialValue == "":
                readSerialValue = 0
            else:
                try:
                    readSerialValue = ser.readline().decode('utf-8').rstrip()
                except:
                    pass
            # Codes [Stupid AF]
            # 0 -> "Heyyyyyy, come over :)"
            # 1 -> "I'm busy..."
            # 2 -> "We fucked up somewhere"
            print("1 " + str(self.j)) 
            if angle != 10 and self.j == 0:
                print("DOING SHIT")
                print(self.j)
                print(readSerialValue)
                print(angle)
                print("Sending angle")
                self.j = 1
                ser.write(str(angle).encode('utf-8'))
            if readSerialValue == "2":
                self.j = 0
    def stop(self):
        self.stopCond.set() #Change it to true
    def stopped(self):
        return self.stopCond.is_set() #Is it set yes or no.

def filterAndMergeContours(contours):
    finalContours = []
    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) > 15:
            finalContours.append(cnt)
    if len(finalContours) == 0:
        return []
    else:
        return np.vstack(finalContours)

def mainFunctionality(camera, mask, min, max, width, height):
    global angle
    prev_frame_time = 0
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        existence, frame = camera.read()
        if cv2.waitKey(1) == ord('q'):
            break
        croppedFrame = cv2.bitwise_and(frame, frame, mask=mask)
        croppedFrameCopy = croppedFrame.copy()
        hsv_image = cv2.cvtColor(croppedFrame, cv2.COLOR_BGR2HSV)
        frame_thres = cv2.inRange(hsv_image, min, max)
        contours, hierarchy = cv2.findContours(image=frame_thres, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
        temp = filterAndMergeContours(contours)
        if len(temp) != 0:
            hull = cv2.convexHull(filterAndMergeContours(contours))

            cv2.polylines(croppedFrameCopy, [hull], True, (0,255,0), 1)
            m = cv2.moments(filterAndMergeContours(contours))
            cX = int(m["m10"] / m["m00"])
            cY = int(m["m01"] / m["m00"])
            cv2.circle(croppedFrameCopy, (cX, cY), 1, (0, 255, 0), 5)

            cv2.rectangle(croppedFrameCopy, (128, 48), (512, 432), (255, 0, 0), 2)
            if not(cX > (330*0.1+150) and cX < (480-330*0.1) and cY > (90+330*0.1) and cY < (420-330*0.1)):
                temp = math.atan2(height/2-cY, cX-width/2)
                if temp < 0:
                    temp += (math.pi*2)
                angle = temp
            else:
                angle = 10
        cv2.rectangle(croppedFrameCopy,(183,123), (447,387), (255,0,0),2)
        new_frame_time = time.time() 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 
        fps = int(fps) 
        fps = str(fps) 
        cv2.putText(croppedFrameCopy, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
        cv2.imshow('Detection', croppedFrameCopy)

if __name__ == "__main__":
    ORANGE_MIN = np.array([0, 65, 0],np.uint8)
    ORANGE_MAX = np.array([20, 255, 255],np.uint8)
    WIDTH = 640
    HEIGHT = 480

    camera = cv2.VideoCapture(0)
    camera.set(3, WIDTH)
    camera.set(4, HEIGHT)
    mask = np.zeros((HEIGHT, WIDTH), dtype='uint8')
    offset = (WIDTH-HEIGHT)/2
    cv2.rectangle(mask, (150,90), (480, 420), (255,255,255), -1)
    
    bs = SerialReaderThread()
    bs.start()
    print("shit")
    mainFunctionality(camera, mask, ORANGE_MIN, ORANGE_MAX, WIDTH, HEIGHT)
    bs.stop()
    ser.stop()
    exit()
