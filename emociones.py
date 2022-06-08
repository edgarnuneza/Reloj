from prepare_training_data import prepare_training_data
import numpy as np
from predict import predict
import cv2

# cap = cv2.VideoCapture(2)

# ret, frame = cap.read()
# if not ret:
#     print("Can't receive frame (stream end?). Exiting ...")

frame = cv2.imread('./cr7.jpeg')
emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
emotion_recognizer.read("modeloLBPH.xml")
predicted_img2 = predict(frame, emotion_recognizer)

cv2.imshow('frame' ,predicted_img2)
cv2.waitKey(0)