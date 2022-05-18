from functools import total_ordering
import pickle
from types import coroutine
import cv2
from ReconocedorRostros.reconocedor import Reconocedor
from imutils.video import VideoStream
import threading


__name__ = "__main__"

def grabar():
    data = pickle.loads(open("./pr_encodings.pkl", "rb").read())
    detector = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

    r = Reconocedor(data, detector)
    cap = cv2.VideoCapture(2)
    vs = VideoStream(2)
    rostros = []

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    totalFotos = 15
    count = 0
    results = []
    
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if count <= totalFotos:
            if r.identificarRostro(frame):
                x = threading.Thread(target=r.reconocer(frame, results, count))
                rostros.append(frame)
                x.start()
                count = count + 1

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    for i, result in enumerate(results):
        print(f"{i} {result}")


if __name__ == '__main__':
    grabar()

