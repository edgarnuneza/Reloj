from Model.model import Empleado, session, Perfil
import datetime

# empleado1=Empleado()
# #empleado1.id=2
# empleado1.nombre='Hector'
# empleado1.apellidoPaterno="Hernandez"
# empleado1.apellidoMaterno="Perez"
# empleado1.matricula='17112016'
# empleado1.puesto='Coordinador'

perfil1 = Perfil()
# perfil1.id = 1
perfil1.nombre = 'test'
perfil1.descripcion = 'ejemplo'
perfil1.creado = datetime.datetime.now()
perfil1.actualizado = datetime.datetime.now()


#Empleado.query.filter_by(id=1).delete()
#session.delete(empleado1)
employee = session.query(Empleado) \
        .filter(Empleado.matricula == 1) \
        .first()
#print(employee.puesto)
#session.delete(employee)

session.add(perfil1)
session.commit()