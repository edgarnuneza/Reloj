import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Empleado, session
import datetime
import uuid

class EmpleadoController:
    def __init__(self):
        pass

    def agregar(self, newEmpleado):

        existeMatricula = employee = session.query(Empleado).filter(Empleado.matricula == newEmpleado.matricula).first()

        if existeMatricula:
            print("Esta repetido")
            return

        newEmpleado.id = uuid.uuid1()
        newEmpleado.creado = datetime.datetime.now()
        newEmpleado.actualizado = datetime.datetime.now()

        try:
            session.add(empleado1)
            session.commit()
        except:
            print("No se pudo guardar")

    def actualizar(self, updateEmpleado):
        

    def eliminar(self, id):

    def get(self, id):




c = EmpleadoController()

empleado1=Empleado()
empleado1.id= uuid.uuid1()
empleado1.nombre='Hector'
empleado1.apellido_paterno="Hernandez"
empleado1.apellido_materno="Perez"
empleado1.matricula='17112018'
empleado1.puesto='Coordinador'
empleado1.creado = datetime.datetime.now()
empleado1.actualizado = datetime.datetime.now()

# session.add(empleado1)
# session.commit()

c.agregar(empleado1)