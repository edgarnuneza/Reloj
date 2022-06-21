import sys, os
from numpy import real_if_close
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Usuario, session
import datetime
import hashlib

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

            newUsuario.salt = os.urandom(32)
            newUsuario.password = hashlib.pbkdf2_hmac('sha256', newUsuario.password.encode('utf-8'), newUsuario.salt, 100000)
            newUsuario.creado = datetime.datetime.now()
            newUsuario.actualizado = datetime.datetime.now()

            session.add(newUsuario)
            session.commit()
            
        except Exception as error:
            raise Exception(error)

    def actualizar(self, updateUsuario):
        try:
            if not updateUsuario.id or not updateUsuario.user_name or not updateUsuario.password:
                raise Exception("Hay campos vacíos")
        
            existeNombre = session.query(Usuario).filter(Usuario.user_name == updateUsuario.nombuser_namere, Usuario.id != updateUsuario.id).first()
            
            if existeNombre:
                raise Exception("El campo debe ser único")

            usuarioBd = self.get(updateUsuario.id)

            if not usuarioBd:
                raise Exception("No se encontro el perfil")

            usuarioBd.salt = os.urandom(32)
            usuarioBd.password = hashlib.pbkdf2_hmac('sha256', updateUsuario.password.encode('utf-8'), usuarioBd.salt, 100000)
            usuarioBd.user_name = updateUsuario.user_name
            usuarioBd.password = updateUsuario.password
            usuarioBd.actualizado = datetime.datetime.now()

            session.add(usuarioBd)
            session.commit()
        except Exception as error:
            raise Exception(error)

    def eliminar(self, id):
        usuarioEliminar = self.get(id)
        session.delete(usuarioEliminar)
        session.commit()

    def get(self, id):
        perfil = session.query(Usuario).get(id)

        if perfil == None:
            raise Exception("No se encontro el usuario")
        
        return perfil
    
    def checkPassword(self, idUsuario, passwordToCheck):
        pass