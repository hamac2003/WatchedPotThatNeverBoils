import cv2
import numpy as np
import time
import serial
import time


# Author: Harrison McIntyre
# Last Updated: 7.31.2020
# Contact: hamac2003@gmail.com



### References / Credits

#Below are links to some of the example code and/or libraries that I integrated into my project.

"""
[Facial Detection](https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/)

[Raspberry Pi / Desktop - Arduino Serial Communication](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)

[OpenCV Image Stacking](https://answers.opencv.org/question/175912/how-to-display-multiple-images-in-one-window/)

"""




# Connect to the arduino at "/dev/ttyACM0"
switch = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
switch.flush()

def sendSerial(state):
    switch.write(state.encode('utf-8'))
    line_0 = switch.readline().decode('utf-8').rstrip()
    time.sleep(0.1)

time.sleep(3)


videos = []

faceLocations = []

foundFace = False


print("Loading Face Detector Model...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")


# Load all camera feeds
for i in range(6):
    print("Aquiring Video " + str(i))
    videos.append(cv2.VideoCapture(i))
    videos[i].set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    videos[i].set(cv2.CAP_PROP_FRAME_HEIGHT, 240)   
    time.sleep(1)



while True:
    images = []
    foundFace = False
    for i in range(len(videos)):
        ret, image = videos[i].read()

        # grab the frame dimensions and convert it to a blob
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        


        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < 0.5:
                continue
            foundFace = True
            sendSerial("1\n")
            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        images.append(image)

    if not foundFace:
        sendSerial("2\n")

    halfImage_1 = np.hstack((images[0],images[1],images[2]))
    halfImage_2 = np.hstack((images[3],images[4],images[5]))
    
    fullImage = np.vstack((halfImage_1,halfImage_2))

    cv2.imshow("AllImages", fullImage)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
