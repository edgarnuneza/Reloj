import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Puesto, session
import datetime
import uuid


class PuestoController:
    def __init__(self):
        pass

    def agregar(self, newPuesto):
        try:
            if not newPuesto.nombre:
                raise Exception("Hay campos vacíos")
        
            newPuesto.id = uuid.uuid1()
            newPuesto.id = str(newPuesto.id).replace("-", "")[0:20]
            

            existeNombre = session.query(Puesto).filter(Puesto.nombre == newPuesto.nombre).first()

            if existeNombre:
                raise Exception("El campo del nombre debe ser único")

            session.add(newPuesto)
            session.commit()
            
        except Exception as error:
            raise Exception(error)

    def actualizar(self, updatePuesto):
        try:
            if not updatePuesto.id or not updatePuesto.nombre:
                raise Exception("Hay campos vacíos")
        
            existeNombre = session.query(Puesto).filter(Puesto.nombre == updatePuesto.nombre, Puesto.id != updatePuesto.id).first()
            
            if existeNombre:
                raise Exception("El campo debe ser único")

            puestoBd = self.get(updatePuesto.id)

            if not puestoBd:
                raise Exception("No se encontro el puesto")

            puestoBd.nombre = updatePuesto.nombre
            session.add(puestoBd)
            session.commit()
        except Exception as error:
            raise Exception(error)

    def eliminar(self, id):
        puestoEliminar = self.get(id)
        session.delete(puestoEliminar)
        session.commit()

    def get(self, nombre):
        puesto = session.query(Puesto).get(nombre)

        if puesto == None:
            raise Exception("No se encontro el puesto")
        
        return puesto
        
    def getAll(self):
        return session.query(Puesto).all()

# c = puestoController()

# empleado1=Empleado()
# # empleado1.id= "8f902684-d7e7-11ec-a474-c1f31a9a582d"
# empleado1.nombre='Hector'
# empleado1.apellido_paterno="Hernandez"
# empleado1.apellido_materno="Perez"
# empleado1.matricula='17112019'
# empleado1.puesto='Dios2'
# empleado1.creado = datetime.datetime.now()
# empleado1.actualizado = datetime.datetime.now()

# c.agregar(empleado1)

# try:
#     print(c.agregar(empleado1))
# except Exception as e:
#     print(e)

    