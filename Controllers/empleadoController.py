import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Empleado, session
import datetime
import uuid

class EmpleadoController:
    def __init__(self):
        pass

    def agregar(self, newEmpleado):
        try:
            if not newEmpleado.nombre or not newEmpleado.apellido_paterno or not newEmpleado.matricula:
                raise Exception("Hay campos vacíos")
        
            newEmpleado.id = uuid.uuid1()
            newEmpleado.creado = datetime.datetime.now()
            newEmpleado.actualizado = datetime.datetime.now()

            existeMatricula = session.query(Empleado).filter(Empleado.matricula == empleado.matricula).first()

            if existeMatricula:
                raise Exception("El campo debe ser único")

            session.add(newEmpleado)
            session.commit()
            
        except Exception as error:
            return error

    def actualizar(self, updateEmpleado):
        try:
            if not updateEmpleado.id or not updateEmpleado.nombre or not updateEmpleado.apellido_paterno or not updateEmpleado.matricula:
                raise Exception("Hay campos vacíos")
        
            existeMatricula = session.query(Empleado).filter(Empleado.matricula == updateEmpleado.matricula and Empleado.id != updateEmpleado.id).first()

            if existeMatricula:
                raise Exception("El campo debe ser único")

            
            empleadoBd = session.query(Empleado).get(updateEmpleado.id)

            if empleadoBd == None:
                raise Exception("No se encontro el empleado")

            empleadoBd.nombre = updateEmpleado.nombre
            empleadoBd.apellido_paterno = updateEmpleado.apellido_paterno
            empleadoBd.apellido_materno = updateEmpleado.apellido_materno
            empleadoBd.matricula = updateEmpleado.matricula
            empleadoBd.puesto = updateEmpleado.puesto
            empleadoBd.actualizado = datetime.datetime.now()

            session.commit()
        except Exception as error:
            return error



    # def eliminar(self, id):
    #     pass
    # def get(self, id):
    #     pass


        
        





c = EmpleadoController()

empleado1=Empleado()
empleado1.id= "8f902684-d7e7-11ec-a474-c1f31a9a582d"
empleado1.nombre='Hector'
empleado1.apellido_paterno="Hernandez"
empleado1.apellido_materno="Perez"
empleado1.matricula='17112019'
empleado1.puesto='Dios'
empleado1.creado = datetime.datetime.now()
empleado1.actualizado = datetime.datetime.now()

# session.add(empleado1)
# session.commit()

try:
    c.actualizar(empleado1)
except Exception as e:
    print(e)
