from email.mime import image
from functools import total_ordering
import pickle
from types import coroutine
import cv2
from ReconocedorRostros.reconocedor import Reconocedor
from imutils.video import VideoStream
import threading
import copy
from collections import Counter
import uuid

__name__ = "__main__"

def grabar():
    data = pickle.loads(open("./Data/Reconocimiento/pr_encodings.pkl", "rb").read())
    detector = cv2.CascadeClassifier("./Data/Reconocimiento/haarcascade_frontalface_default.xml")

    r = Reconocedor(data, detector)
    cap = cv2.VideoCapture(0)
    
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
            isFace, img = r.identificarRostro(copy.copy(frame))
            if isFace:
                
                x = threading.Thread(target=r.reconocer(frame, results))
                x.start()
                frame = img
                count = count + 1

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q') or count > totalFotos:
            break

    cap.release()
    cv2.destroyAllWindows()

    identificarRostro(results)

def identificarRostro(results):
    
    contadorRostros = {}
    
    for i in range(0, len(results)):

        if not results[i][0] in contadorRostros:
            contadorRostros[results[i][0]] = 1
        else:
            contadorRostros[results[i][0]] = contadorRostros.get(results[i][0]) + 1

    rostroFinal = max(contadorRostros, key=contadorRostros.get)
    print(type(rostroFinal))
    
    imagenMostrar = None

    for resultado in reversed(results):
        if resultado[0] == rostroFinal:
            imagenMostrar = resultado[1]
            break
    
    nombreImagen = f"./images/{uuid.uuid1()}.png"
    cv2.imwrite(nombreImagen, imagenMostrar)

    # print(nombreImagen, rostroFinal)
    # return [nombreImagen, rostroFinal]
    cv2.imshow('frame', imagenMostrar)
    cv2.waitKey(0)


if __name__ == '__main__':
    grabar()

