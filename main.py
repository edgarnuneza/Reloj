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
            isFace, boxes = r.identificarRostro(frame)
            if isFace:
                x = threading.Thread(target=r.reconocer(frame, results))
                x.start()
                count = count + 1

                for (top, right, bottom, left) in boxes:
                    # draw the predicted face name on the image
                    cv2.rectangle(frame, (left, top), (right, bottom),
                        (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, 'identificando', (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    identificarRostro(results)
    # for i, result in enumerate(results):
    #     print(f"{i} {result}")

def identificarRostro(results):
    cv2.imshow('frame', results[0][1])
    cv2.waitKey(0)


if __name__ == '__main__':
    grabar()

