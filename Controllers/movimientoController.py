import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Movimiento, session
import datetime
import uuid

class MovimientoController:
    def __init__(self):
        pass

    def agregar(self, newMovimiento):
        try:
            if not newMovimiento.id_empleado or not newMovimiento.tipo_movimiento or not newMovimiento.tiempo:
                raise Exception("Hay campos vacíos")
        
            if not (newMovimiento.tipo_movimiento.lower() == "entrada" or newMovimiento.tipo_movimiento.lower() == "salida"):
                 raise Exception("El tipo de movimiento debe ser entrada o salida")

            newMovimiento.creado = datetime.datetime.now()
            newMovimiento.actualizado = datetime.datetime.now()

            session.add(newMovimiento)
            session.commit()
            
        except Exception as error:
            raise Exception(error)

    def actualizar(self, updateMovimiento):
        try:
            if not updateMovimiento.id or not updateMovimiento.id_empleado or not updateMovimiento.tipo_movimiento or not updateMovimiento.tiempo:
                raise Exception("Hay campos vacíos")
        
            if not (updateMovimiento.tipo_movimiento.lower() == "entrada" or updateMovimiento.tipo_movimiento.lower() == "salida"):
                 raise Exception("El tipo de movimiento debe ser entrada o salida")

            movimientoBd = self.get(updateMovimiento.id)

            if not movimientoBd:
                raise Exception("No se encontro el movimiento")

            movimientoBd.id_empleado = updateMovimiento.id_empleado
            movimientoBd.tipo_movimiento = updateMovimiento.tipo_movimiento
            movimientoBd.tiempo = updateMovimiento.tiempo
            movimientoBd.actualizado = datetime.datetime.now()

            session.add(movimientoBd)
            session.commit()
        except Exception as error:
            raise Exception(error)

    def eliminar(self, id):
        movimientoEliminar = self.get(id)
        session.delete(movimientoEliminar)
        session.commit()

    def get(self, id):
        movimiento = session.query(Movimiento).get(id)

        if movimiento == None:
            raise Exception("No se encontro el movimiento")
        
        return movimiento
    def getAll():
        movimientos = session.query(Movimiento).all()
        return movimientos
    def getMovimientoFiltrado(seld,id):

        movimientoFiltrado=session.query(Movimiento).filter(Movimiento.id_empleado == id).all()
        return movimientoFiltrado
# movimiento1 = Movimiento()
# movimiento1.id = 1
# movimiento1.id_empleado = 'dfb836a1-d7e8-11ec-a474-c1f31a9a582d'
# movimiento1.tipo_movimiento = "entrada"
# movimiento1.tiempo = datetime.datetime.now()

# c = MovimientoController()

# try:
#     c.actualizar(movimiento1)
# except Exception as e:
#     print(e)
