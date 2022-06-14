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
from Controllers.movimientoController import MovimientoController
from Model.model import Empleado, Movimiento
from flask import request
import datetime


#Librerias emociones
from prepare_training_data import prepare_training_data
import numpy as np
from predict import predict

app = Flask(__name__)

numeroCamara = 2
cap = cv2.VideoCapture(numeroCamara)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

data = pickle.loads(open("./Data/Reconocimiento/pr_encodings.pkl", "rb").read())
detector = cv2.CascadeClassifier("./Data/Reconocimiento/haarcascade_frontalface_default.xml")
r = Reconocedor(data, detector)
c = Capturador()
rostroPersona = ''

totalFotos = 15
count = 0
results = []
idEmpleado = ''

@app.route("/generate")
def generate():
    global count
    global results
    global totalFotos

    iniciarCamara()
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
    cap.release()
    return render_template("login.html")

@app.route("/reconocerPersona")
def reconocerPersona():
    reiniciar()
    return render_template("Grabando.html")

@app.route("/movimiento")
def movimiento():
    return render_template("Movimientos.html")

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
    global cap
    global rostroPersona

    cap.release()

    return render_template("registro.html", data=rostroPersona)

@app.route("/getRostroIdentificado")
def getRostroIdentificado():
    global results
    return Response(identificarRostro(results),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/rostroPersona')
def getRostro():
    global rostroPersona

    if rostroPersona == '':
        return jsonify(rostro = False)
    else: 
        rostroPersona = rostroPersona.capitalize()
        return jsonify(rostro = rostroPersona)

def identificarRostro(results):
    global rostroPersona
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

    # emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # emotion_recognizer.read("modeloLBPH.xml")

    # cv2.imshow('imagen', imagenMostrar)
    # cv2.waitKey(0)

    # predicted_img2 = predict(imagenMostrar, emotion_recognizer)
    
    # rostroPersona = rostroFinal
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

    return jsonify(detener = c.detener, total = c.count)

@app.route('/foto/<empleadoId>')
def foto(empleadoId):
    global c
    empleadoC = EmpleadoController()
    
    try:
        c.identificador = empleadoId
        c.detener = False
        empleadoEntrenar = empleadoC.get(empleadoId)
    except Exception as e:
        empleadoId = None
        print(e)
        
    if empleadoId == None:
        return "No funciono la busqueda de ID"
    else:
        return render_template('capturar.html', data=empleadoId)
    
@app.route("/getEmpleado/<idEmpleado>")
def getEmpleado(idEmpleado):
    controlador = EmpleadoController()
    empleado = controlador.get(idEmpleado)

    return jsonify(id = empleado.id, nombre = empleado.nombre, apaterno = empleado.apellido_paterno, amaterno = empleado.apellido_materno, matricula = empleado.matricula, datosCapturados = empleado.datosCapturados, puesto = empleado.puesto, creado = empleado.creado, actualizado = empleado.actualizado)

@app.route("/updateEmpleado", methods = ['POST', 'GET'])
def updateEmpleado():
    controlador = EmpleadoController()
    empleadoUpdate = Empleado()

    if request.method == 'POST':
        empleadoUpdate.id = request.form['id']
        empleadoUpdate.nombre = request.form['nombre']
        empleadoUpdate.apellido_paterno = request.form['apaterno']
        empleadoUpdate.apellido_materno = request.form['amaterno']
        empleadoUpdate.matricula = request.form['matricula']
        empleadoUpdate.puesto = request.form['puesto']

        # datafromjs = request.form['mydata']
        controlador.actualizar(empleadoUpdate)

    return redirect(url_for('empleados'))



@app.route("/empleados")
def empleados():
    global cap
    cap.release()
    controlador = EmpleadoController()
    datos = controlador.getAll()
    return render_template("vision.html", data= datos)

@app.route('/createempleado', methods = ['POST'])
def createempleado():
    controlador = EmpleadoController()
    empleadoAgregar = Empleado()
    if request.method == 'POST':
        empleadoAgregar.nombre = request.form['nombre']
        empleadoAgregar.apellido_paterno = request.form['apaterno']
        empleadoAgregar.apellido_materno = request.form['amaterno']
        empleadoAgregar.matricula = request.form['matricula']
        empleadoAgregar.puesto = request.form['puesto']
        empleadoAgregar.creado = datetime.datetime.now()
        empleadoAgregar.actualizado = datetime.datetime.now()

        # datafromjs = request.form['mydata']
        controlador.agregar(empleadoAgregar)

    return redirect(url_for('empleados'))

@app.route('/deleteempleado', methods = ['POST'])
def deleteempleado():
    
    controlador = EmpleadoController()

    if request.method == 'POST':
        data = request.json
        print(data)
        controlador.eliminar(data.get('id'))

    return redirect(url_for('empleados'))


@app.route('/verMovimientos/<idEmpleado>')
def verMovimientos(idEmpleado):
    cap.release()
    movimientoController = MovimientoController()

    movimientos = movimientoController.getMovimientoFiltrado(idEmpleado)
    return render_template("Movimientos.html", data=movimientos)

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

def iniciarCamara():
    global cap
    cap = cv2.VideoCapture(numeroCamara)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    

if __name__ == "__main__":
     app.run(debug=False)

cap.release()