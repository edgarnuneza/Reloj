from contextlib import redirect_stderr
from unittest import result
from flask import Flask, redirect, url_for, jsonify
from flask import render_template
from flask import Response
import cv2
from ReconocedorRostros.reconocedor import Reconocedor
from imutils.video import VideoStream
import threading
import copy
from collections import Counter
from email.mime import image
from functools import total_ordering
import pickle
from types import coroutine
from ReconocedorRostros.capturador import Capturador
from Controllers.empleadoController import EmpleadoController

app = Flask(__name__)

cap = cv2.VideoCapture(2)

data = pickle.loads(open("./Data/Reconocimiento/pr_encodings.pkl", "rb").read())
detector = cv2.CascadeClassifier("./Data/Reconocimiento/haarcascade_frontalface_default.xml")
r = Reconocedor(data, detector)
c = Capturador()


if not cap.isOpened():
    print("Cannot open camera")
    exit()

totalFotos = 15
count = 0
results = []
idEmpleado = ''

@app.route("/generate")
def generate():
    global count
    global results
    global totalFotos

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

            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    reiniciar()
    return render_template("grabador.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/capturador/<empleadoId>")
def capturador(empleadoId):
    global cap
    global c
    cap.release()
    c.identificador = empleadoId
    
    return Response(c.capturar(), 
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/getRostroIdentificado")
def getRostroIdentificado():
    global results
    return Response(identificarRostro(results),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

def identificarRostro(results):
    
    contadorRostros = {}
    
    for i in range(0, len(results)):

        if not results[i][0] in contadorRostros:
            contadorRostros[results[i][0]] = 1
        else:
            contadorRostros[results[i][0]] = contadorRostros.get(results[i][0]) + 1

    rostroFinal = max(contadorRostros, key=contadorRostros.get)
    print(rostroFinal)
    
    imagenMostrar = None

    for resultado in reversed(results):
        if resultado[0] == rostroFinal:
            imagenMostrar = resultado[1]
            break
    
    if rostroFinal == 'Desconocido':
        imagenMostrar = cv2.imread('./Data/desconocido.jpg')
    
    (flag, encodedImage) = cv2.imencode(".jpg", imagenMostrar)
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
    bytearray(encodedImage) + b'\r\n')

@app.route('/api/count')
def hello():
    global totalFotos
    global count

    if count > totalFotos:
        return jsonify(isCaptured = True)
    else:
        return jsonify(isCaptured = False)


@app.route('/api/countcaptura')
def countCaptura():
    global c

    return jsonify(detener = c.detener)

@app.route('/foto/<empleadoId>')
def foto(empleadoId):
    empleadoC = EmpleadoController()

    try:
        empleadoEntrenar = empleadoC.get(empleadoId)
    except Exception as e:
        empleadoId = None
        print(e)
        
    if empleadoId == None:
        return "No funciono la busqueda de ID"
    else:
        return render_template('capturar.html', data=empleadoId)
    
def reiniciar():
    global totalFotos 
    global count
    global results 
    global idEmpleado 
    global redireccionar

    totalFotos = 15
    count = 0
    results = []
    idEmpleado = ''
    redireccionar = True

if __name__ == "__main__":
     app.run(debug=False)

cap.release()