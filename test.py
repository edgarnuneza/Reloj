from contextlib import redirect_stderr
from unittest import result
from flask import Flask, redirect, url_for, jsonify
from flask import render_template
from flask import Response, session
import cv2
from ReconocedorRostros.reconocedor import Reconocedor
from imutils.video import VideoStream
import threading
import copy
from collections import Counter
from email.mime import image
from functools import total_ordering
from flask import Flask, session

import pickle
from types import coroutine
from ReconocedorRostros.capturador import Capturador
from Controllers.empleadoController import EmpleadoController
from Controllers.movimientoController import MovimientoController
from Model.model import Empleado, Movimiento
from flask import request
import datetime

# Librerias emociones
from prepare_training_data import prepare_training_data
import numpy as np
from predict import predict
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'hector'

numeroCamara = 0
cap = cv2.VideoCapture(numeroCamara)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

data = pickle.loads(
    open("./Data/Reconocimiento/pr_encodings.pkl", "rb").read())
detector = cv2.CascadeClassifier(
    "./Data/Reconocimiento/haarcascade_frontalface_default.xml")
r = Reconocedor(data, detector)
c = Capturador()
rostroPersona = ''

totalFotos = 15
count = 0
results = []
idEmpleado = ''
empleadoActual = Empleado()


@app.route("/generate")
def generate():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:

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
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
    if isLogged() == False:
        cap.release()
        return render_template("login.html")
    else:
        return redirect(url_for('empleados'))


def validation(user, password):
    import psycopg2
    conexion1 = psycopg2.connect(
        database="reloj", user="edgar", password="123")
    cursor1 = conexion1.cursor()
    cursor1.execute("select * from Usuario")
    lista = list(cursor1)
    conexion1.close()
    for fila in lista:
        if fila[1] == user and fila[2] == password:
            return True
    return False


def isLogged():
    # name = session.get('usuario', 'not set')
    # if name != 'not set':
    #     return True
    # else:
    #     return False
    return True


@app.route("/do_login", methods=["POST"])
def do_login():
    return redirect(url_for('empleados'))

    # if request.method == 'POST':
    #     user = request.form["user"]
    #     password = request.form["password"]
    #     if validation(user, password):
    #         session["usuario"] = user
    #         return redirect(url_for('empleados'))
    # else:
    #     # return redirect("/login")
    #     return redirect(url_for('index'))


@app.route("/reconocerPersona")
def reconocerPersona():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        return render_template("Grabando.html")


@app.route("/movimiento")
def movimiento():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        return render_template("Movimientos.html")


@app.route("/video_feed")
def video_feed():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        return Response(generate(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/capturador/<empleadoId>")
def capturador(empleadoId):
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global cap
        global c
        cap.release()
        c.identificador = empleadoId

        return Response(c.capturar(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/deleteCookies")
def deleteCookies():
    session.clear()
    return redirect(url_for('index'))


@app.route("/registro")
def registro():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global cap
        global rostroPersona

        cap.release()

        return render_template("registro.html", data=rostroPersona)


@app.route("/getRostroIdentificado")
def getRostroIdentificado():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global results
        return Response(identificarRostro(results),
                        mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/rostroPersona')
def getRostro():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global rostroPersona

        if rostroPersona == '':
            return jsonify(rostro=False)
        else:
            rostroPersona = rostroPersona.capitalize()
            return jsonify(rostro=rostroPersona)


def identificarRostro(results):
    global rostroPersona
    contadorRostros = {}

    for i in range(0, len(results)):

        if not results[i][0] in contadorRostros:
            contadorRostros[results[i][0]] = 1
        else:
            contadorRostros[results[i][0]] = contadorRostros.get(
                results[i][0]) + 1

    rostroFinal = max(contadorRostros, key=contadorRostros.get)
    print(rostroFinal)

    imagenMostrar = None

    for resultado in reversed(results):
        if resultado[0] == rostroFinal:
            imagenMostrar = resultado[1]
            break

    if rostroFinal == 'Desconocido':
        imagenMostrar = cv2.imread('./Data/desconocido.jpg')
    else:
        crearEmpleado(rostroFinal)

    # emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # emotion_recognizer.read("modeloLBPH.xml")

    # cv2.imshow('imagen', imagenMostrar)
    # cv2.waitKey(0)

    # predicted_img2 = predict(imagenMostrar, emotion_recognizer)

    # rostroPersona = rostroFinal
    (flag, encodedImage) = cv2.imencode(".jpg", imagenMostrar)
    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
           bytearray(encodedImage) + b'\r\n')


@app.route('/api/count')
def hello():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global totalFotos
        global count

        if count > totalFotos:
            return jsonify(isCaptured=True)
        else:
            return jsonify(isCaptured=False)


@app.route('/api/countcaptura')
def countCaptura():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global c

        return jsonify(detener=c.detener, total=c.count)


@app.route('/foto/<empleadoId>')
def foto(empleadoId):
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
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
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        controlador = EmpleadoController()
        empleado = controlador.get(idEmpleado)

        return jsonify(id=empleado.id, nombre=empleado.nombre, apaterno=empleado.apellido_paterno, amaterno=empleado.apellido_materno, matricula=empleado.matricula, datosCapturados=empleado.datosCapturados, puesto=empleado.puesto, creado=empleado.creado, actualizado=empleado.actualizado)


@app.route("/updateEmpleado", methods=['POST', 'GET'])
def updateEmpleado():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
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
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global cap
        cap.release()
        controlador = EmpleadoController()
        datos = controlador.getAll()
        datos = datos[::-1]
        return render_template("vision.html", data=datos)


@app.route('/createempleado', methods=['POST'])
def createempleado():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
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


@app.route('/deleteempleado', methods=['POST'])
def deleteempleado():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:

        controlador = EmpleadoController()
        movController = MovimientoController()
        if request.method == 'POST':
            data = request.json
            movController.eliminarMovimientosEmpleado(data.get('id'))
            controlador.eliminar(data.get('id'))

        return redirect(url_for('empleados'))


@app.route('/api/empleadoactual')
def empleadoactual():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        global empleadoActual

        return jsonify(id=empleadoActual.id, nombre=empleadoActual.nombre, apaterno=empleadoActual.apellido_paterno, amaterno=empleadoActual.apellido_materno, matricula=empleadoActual.matricula, datosCapturados=empleadoActual.datosCapturados, puesto=empleadoActual.puesto, creado=empleadoActual.creado, actualizado=empleadoActual.actualizado)


@app.route('/verMovimientos/<idEmpleado>')
def verMovimientos(idEmpleado):
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        cap.release()
        movimientoController = MovimientoController()

        movimientos = movimientoController.getMovimientoFiltrado(idEmpleado)
        return render_template("Movimientos.html", data=movimientos)


@app.route('/registrarmovimiento', methods=['POST'])
def registrarMovimiento():
    if isLogged() == False:
        return redirect(url_for('index'))
    else:
        controladorMovimiento = MovimientoController()
        movimiento = Movimiento()

        if request.method == 'POST':
            data = request.json
            print(data)
            movimiento.id_empleado = data.get('id_empleado')
            movimiento.tipo_movimiento = data.get('tipo')
            movimiento.tiempo = datetime.datetime.now()
            movimiento.creado = datetime.datetime.now()
            controladorMovimiento.agregar(movimiento)

        return redirect(url_for('verMovimientos', idEmpleado=data.get('id_empleado')))


def reiniciar():
    global totalFotos
    global count
    global results
    global idEmpleado
    global redireccionar
    global empleadoActual

    totalFotos = 15
    count = 0
    results = []
    idEmpleado = ''
    redireccionar = True
    empleadoActual = Empleado()


def iniciarCamara():
    global cap
    cap = cv2.VideoCapture(numeroCamara)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()


def crearEmpleado(id):
    global empleadoActual

    controlador = EmpleadoController()
    empleadoActual = controlador.get(id)

if __name__ == "__main__":
    app.run(debug=False)

cap.release()
