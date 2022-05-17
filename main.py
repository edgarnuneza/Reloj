import pickle
from types import coroutine
import cv2
from reconocedor import Reconocedor
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

    count = 0
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if count <= 15:
            if r.identificarRostro(frame):
                x = threading.Thread(target=r.reconocer(frame))
                rostros.append(frame)
                print(x.start())
                #r.reconocer(frame)
                count = count + 1
                print(count)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # for rostro in rostros:
    #     print(r.reconocer(rostro))
    #image = vs.read()q

    #print(r.identificarRostro(image))


if __name__ == '__main__':
    grabar()

