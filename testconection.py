



def validation(user, password):
    import psycopg2    
    conexion1 = psycopg2.connect(database="reloj", user="edgar", password="123")
    cursor1=conexion1.cursor()
    cursor1.execute("select * from Usuario")
    lista = list(cursor1)
    conexion1.close()
    for fila in lista:
        if fila[1] == user and fila[2]== password:
            return True
    return False    
                
    

print(validation("alexis", "1234"))