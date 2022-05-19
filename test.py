from Model.model import Empleado, session

empleado1=Empleado()
empleado1.id=1
empleado1.nombre='Hector'
empleado1.apellidoPaterno="Hernandez"
empleado1.apellidoMaterno="Perez"
empleado1.matricula='17112016'
empleado1.puesto='Coordinador'

#Empleado.query.filter_by(id=1).delete()
#session.delete(empleado1)
employee = session.query(Empleado) \
        .filter(Empleado.id == 1) \
        .first()
#print(employee.puesto)
session.delete(employee)
session.commit()