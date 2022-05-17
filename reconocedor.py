from cmath import rect
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import platform

from numpy import rec

class Reconocedor:
    def __init__(self, data, detector):
        self.data = data
        self.detector = detector
        self.fps = FPS().start()

    def reconocer(self, image):
        image = imutils.resize(image, width=500)

        # convert the input image from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale image
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        name = ''

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"],
                encoding, tolerance=0.46)
            name = "Desconocido"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
            
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(image, (left, top), (right, bottom),
                (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)

        # display the image to our screen
        # cv2.imshow("image", image)
        # key = cv2.waitKey(1) & 0xFF


        if not name == 'None':
            print(name)
        # update the FPS counter
        self.fps.update()

    def identificarRostro(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        if len(rects) == 0:
            return False

        else: 
            return True

    