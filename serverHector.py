from contextlib import redirect_stderr
from unittest import result
from flask import Flask, redirect, url_for, jsonify
from flask import render_template
from flask import Response
from collections import Counter
from email.mime import image
from functools import total_ordering
import pickle
from types import coroutine
from Controllers.empleadoController import EmpleadoController
from flask import request
from Model.model import Empleado
import datetime

app = Flask(__name__)

@app.route("/")
def test():
    return render_template("vision.html", data='edgar')

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
    controlador = EmpleadoController()
    datos = controlador.getAll()
    return render_template("vision.html", data= datos)

@app.route("/movimiento")
def movimiento():
    return "hola"

@app.route("/reconocerPersona")
def reconocerPersona():
    return "hola"


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

    return render_template('vision.html')



if __name__ == "__main__":
     app.run(debug=True)