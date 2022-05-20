from sqlalchemy import TIMESTAMP, ForeignKey, PrimaryKeyConstraint, create_engine, null  
from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://postgres:123@localhost:5432/reloj"

db = create_engine(db_string)  
base = declarative_base()

class Empleado(base):  
    __tablename__ = 'empleado'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=False)
    matricula = Column(String, nullable=False, index=True, unique=True)
    puesto = Column(String, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)
    
class Perfil(base):
    __tablename__ = 'perfil'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

class Movimiento(base):
    __tablename__ = 'movimiento'

    id = Column(Integer, primary_key=True)
    id_empleado = Column(String, ForeignKey('empleado.id'))
    tipo_movimiento = Column(String, nullable=False)
    tiempo = Column(TIMESTAMP, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

class Usuario(base):
    __tablename__ = 'usuario'

    id = Column(String, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

class Permisos(base):
    __tablename__ = 'permisos'

    id = Column(Integer, primary_key=True)
    id_perfil = Column(Integer, ForeignKey('perfil.id'))
    permiso = Column(String, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

class Config(base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    nombre =  Column(String, nullable=False)
    valor =  Column(String, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

class FotografiaPerfil(base):
    __tablename__ = 'fotografia_perfil'

    id = Column(Integer, primary_key=True)
    id_empleado = Column(String, ForeignKey('empleado.id'))
    ruta = Column(String, nullable=False)
    creado = Column(TIMESTAMP, nullable=False)
    actualizado = Column(TIMESTAMP, nullable=True)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)