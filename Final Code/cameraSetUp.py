import cv2
import numpy as np

def mainFunc(mask):
    while True:
        existence, frame = camera.read()
        if cv2.waitKey(1) == ord('q'):
            break
        croppedFrame = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Fix the camera goofball", croppedFrame)

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)
    mask = np.zeros((480, 640), dtype='uint8')
    cv2.rectangle(mask, (150,90), (480, 420), (255,255,255), -1)
    mainFunc(mask)
    camera.release()
    exit()