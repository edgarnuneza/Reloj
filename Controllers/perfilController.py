import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Perfil, session
import datetime

class PerfilController:
    def __init__(self):
        pass

    def agregar(self, newPerfil):
        try:
            if not newPerfil.nombre or not newPerfil.descripcion:
                raise Exception("Hay campos vacíos")
        
            existeNombre = session.query(Perfil).filter(Perfil.nombre == newPerfil.nombre).first()

            if existeNombre:
                raise Exception("El campo debe ser único")

            newPerfil.creado = datetime.datetime.now()
            newPerfil.actualizado = datetime.datetime.now()

            session.add(newPerfil)
            session.commit()
            
        except Exception as error:
            raise Exception(error)

    def actualizar(self, updatePerfil):
        try:
            if not updatePerfil.id or not updatePerfil.nombre or not updatePerfil.descripcion:
                raise Exception("Hay campos vacíos")
        
            existeNombre = session.query(Perfil).filter(Perfil.nombre == updatePerfil.nombre, Perfil.id != updatePerfil.id).first()
            
            if existeNombre:
                raise Exception("El campo debe ser único")

            perfilBd = self.get(updatePerfil.id)

            if not perfilBd:
                raise Exception("No se encontro el perfil")

            perfilBd.nombre = updatePerfil.nombre
            perfilBd.descripcion = updatePerfil.descripcion
            perfilBd.actualizado = datetime.datetime.now()

            session.add(perfilBd)
            session.commit()
        except Exception as error:
            raise Exception(error)

    def eliminar(self, id):
        perfilEliminar = self.get(id)
        session.delete(perfilEliminar)
        session.commit()

    def get(self, id):
        perfil = session.query(Perfil).get(id)

        if perfil == None:
            raise Exception("No se encontro el perfil")
        
        return perfil

p = Perfil()

controller = PerfilController()
p.id = 2
p.nombre = "Admin4"
p.descripcion = "Administra todo el show"

try:
    controller.eliminar(2)
except Exception as e:
    print(e)

