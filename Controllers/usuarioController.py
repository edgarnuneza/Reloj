import sys, os
from numpy import real_if_close
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Usuario, session
import datetime

class UsuarioController:
    def __init__(self):
        pass

    def agregar(self, newUsuario):
        try:
            if not newUsuario.user_name or not newUsuario.password:
                raise Exception("Hay campos vacíos")
        
            existeUsuario = session.query(Usuario).filter(Usuario.id == newUsuario.id).first()

            if existeUsuario:
                raise Exception("El campo debe ser único")

            newUsuario.creado = datetime.datetime.now()
            newUsuario.actualizado = datetime.datetime.now()

            session.add(newUsuario)
            session.commit()
            
        except Exception as error:
            raise Exception(error)

    def actualizar(self, newUsuario):
        try:
            if not newUsuario.id or not newUsuario.user_name or not newUsuario.password:
                raise Exception("Hay campos vacíos")
        
            existeNombre = session.query(Usuario).filter(Usuario.user_name == newUsuario.nombuser_namere, Usuario.id != newUsuario.id).first()
            
            if existeNombre:
                raise Exception("El campo debe ser único")

            usuarioBd = self.get(newUsuario.id)

            if not usuarioBd:
                raise Exception("No se encontro el perfil")

            usuarioBd.user_name = newUsuario.user_name
            usuarioBd.password = newUsuario.password
            usuarioBd.actualizado = datetime.datetime.now()

            session.add(usuarioBd)
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

