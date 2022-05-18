from sqlalchemy import ForeignKey, PrimaryKeyConstraint, create_engine, null  
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://postgres:tecnologiA78#@localhost:5432/reloj"

db = create_engine(db_string)  
base = declarative_base()

class Empleado(base):  
    __tablename__ = 'empleado'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellidoPaterno = Column(String, nullable=False)
    apellidoMaterno = Column(String, nullable=False)
    matricula = Column(String, nullable=False, index=True, unique=True)
    puesto = Column(String, nullable=False)

class Perfil(base):
    __tablename__ = 'perfil'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)

class Movimiento(base):
    __tablename__ = 'movimiento'

    id = Column(Integer, primary_key=True)
    id_empleado = Column(Integer, ForeignKey('empleado.id'))
    tipo_movimiento = Column(String, nullable=False)
    tiempo = Column(DateTime, nullable=False)

class Usuario(base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Permisos(base):
    __tablename__ = 'permisos'

    id = Column(Integer, primary_key=True)
    id_perfil = Column(Integer, ForeignKey('perfil.id'))
    permiso = Column(String, nullable=False)

class Config(base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    nombre =  Column(String, nullable=False)
    valor =  Column(String, nullable=False)

class Fotografias(base):
    __tablename__ = 'fotografias'

    id = Column(Integer, primary_key=True)
    id_empleado = Column(Integer, ForeignKey('empleado.id'))
    ruta = Column(String, nullable=False)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)