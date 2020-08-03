import numpy as np
import time
import cv2
import dlib
from gpiozero import LED


# Author: Harrison McIntyre
# Last Updated: 8.3.2020
# Contact: hamac2003@gmail.com



### References / Credits

#Below are links to some of the example code and/or libraries that I integrated into my project.

"""
[Facial Detection (Dlib)](https://www.pyimagesearch.com/2018/04/02/faster-facial-landmark-detector-with-dlib/)

[Raspberry Pi / Desktop - Arduino Serial Communication](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)

"""

burner = LED(3)

burner.on()

# start the video stream thread
print("[INFO] starting video stream thread...")
video_capture = cv2.VideoCapture(0)

time.sleep(1.0)

detector = dlib.get_frontal_face_detector()

# Initialize some variables                                                                                                                                                                                                                             v b nbmb  3333333       q
rects = None
shape = None
frameNum = 0
testNum = 0
rects = []


while True:
    start = time.time()
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    small_frame = frame.copy()

    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    image_shape = gray.shape
    

    if True:
        frameNum = 0
        face_locations = []

        frameNum = 0
        
        start = time.time()
        # detect faces in the grayscale frame
        rects = None
        rects = detector(gray, 0)
    # loop over the face detections
    for rect in rects:
        cv2.rectangle(frame, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (255, 0, 0), 2)
    if len(rects) > 0:
        burner.off()
    else:
        burner.on()
    end = time.time()

    cv2.imshow("Frame", frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
