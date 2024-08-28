import os
import time
import random
import sqlite3

ruta_db = os.path.join("DB", "Panel_admin.db")

def limpiar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


#Funcion que genera un codigo con 4 letras y 3 numeros, para la identificacion de los mozos
def Generar_Codigo():    
    lista_Letras = ["A", "B", "C", "D", "E", "F", "G",
                    "H", "I", "J", "K", "L", "M", "N", 
                    "O","P", "Q", "S", "T", "R", "U", 
                    "V", "W", "X", "Y", "Z"]
    #Se inicializa codigo para poder iterar los espacios del str
    codigo = list("AOOE505")
    #Un ciclo for para iterar la variable de codigo
    for i in range(0, 6):
            #Se utiliza el motodo radiant de la libreria ramdom para elejir una letra de forma alatoria
            valor_R_letra = random.randint(0, len(lista_Letras)-1)
            #If para que pare de sumar letras y pase a añadir numeros del 0 al 9
            if i <= 3:
                codigo[i] = lista_Letras[valor_R_letra]
            elif i <= 6:
                valor_R_numero = random.randint(0, 9)

                #Se le asigna el numero pero como un str para que haga conflictos con la iteracion de la variable
                codigo[i] = str(valor_R_numero)
    
    #Una vez que el codigo ya tiene sus caracteres corespondientes, se vuelve a unir la lista en una sola cadena con el .join
    codigo = ''.join(codigo)

    return codigo

#Creacion de las tables 
def crear_tablas():
    conn = sqlite3.connect(ruta_db) #Se conecta a la base de datos creada
    cursor = conn.cursor() #Crea el cursor para ejecutar comandos en la base de datos

    #Ejecuta una instruccion
    #Se crean las tabla si no existen (por eso la aclaracion de IF NOT), una vez la tabla creada crea la columna con su tipo de dato
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Productos(
        Nombre TEXT,
        Precio INTEGER,)"""
    ) 
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Usuarios(
        Mozo TEXT,
        Codigo TEXT PRIMARY KEY,
        Plaza INTEGER)"""
    )

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

def Cargar_Producto(name, precio):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    #Se crea una variable para darle instrucciones, estas se dan con parametros especificos propios de SQL
    instruccion = "INSERT INTO Productos (nombre, precio) VALUES (?, ?)" #Ingresa a la base de datos los valores que resive por eso es INSERT
    cursor.execute(instruccion, (name, precio)) #Ejecuta la accion 

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

def Modificar_Productos(name, categoria, nuevo_valor):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 

    instruccion = f"UPDATE Productos SET {categoria} = {nuevo_valor} WHERE Nombre like '{name}'" #Actualiza los valores que se le indiquen en la base de datos por eso UPDATE
    cursor.execute(instruccion) #Ejecuta la accion 

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

def Mostrar_Productos():
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 

    instruccion = f"SELECT * FROM Productos" #Captura todos los datos de la base de datos por eso SELECT
    cursor.execute(instruccion) #Ejecuta la accion 

    datos = cursor.fetchall() #La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

    return datos

def Eliminar_Producto(name):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 
    
    instruccion = f"DELETE FROM Productos WHERE Nombre like '{name}'" #Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion) #Ejecuta la accion 

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

def Registro_Empleado(name, codigo, Plaza):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 

    instruccion = f"INSERT INTO Usuarios (mozo, codigo, plaza) VALUES (?, ?, ?)" #Ingresa a la base de datos los valores que resive por eso es INSERT
    cursor.execute(instruccion, (name, codigo, Plaza)) #Ejecuta la accion 

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

def Mostrar_Empleados():
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 

    instruccion = f"SELECT * FROM Usuarios" #Captura todos los datos de la base de datos por eso SELECT
    cursor.execute(instruccion) #Ejecuta la accion 

    datos = cursor.fetchall()

    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 

    return datos

def Modificar_Empleados(name, categoria, valor):
    conn  = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    instruccion = f"SELECT * from Usuarios WHERE Mozo like '{name}'"
    cursor.execute(instruccion) #Ejecuta la accion 
    
    datos = cursor.fetchall() #La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices
    
    if datos: #Se ve si datos tiene o no valores
        instruccion = f"UPDATE Usuarios SET {categoria} = ? WHERE Mozo like ?" #Se actualiza los datos
        cursor.execute(instruccion, (valor, name)) #Ejecuta la accion 
        conn.commit() #Guarda los cambios hechos a la base de datos
    else:
        return "No se encunetra el nombre del mozo ingresado"
        
    conn.close() #Cierra la coneccion con la base de datos 

def Eliminar_empleados(name):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 
    
    instruccion = f"DELETE FROM Usuarios WHERE Mozo like '{name}'" #Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion) #Ejecuta la accion 
    
    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 
    
def verificar(name, code):
    #Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor() 
    
    instruccion = f"SELECT * from Usuarios WHERE Mozo like ?" #Captura en especifico de la columna mozo el nombre que se le ingresa
    cursor.execute(instruccion, (name)) #Ejecuta la accion 
    
    datos = cursor.fetchall() #La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices
    
    conn.commit() #Guarda los cambios hechos a la base de datos
    conn.close() #Cierra la coneccion con la base de datos 
    
    if datos != []: #Comprobacion si tiene datos o no
        if code == datos[0][1]:
            return True
        else:
            return False
    else:
        return 2

#Si se ejecuta este archivo desde el mismo se ejecutan todo lo que este por debajo de este if si no, no se hace
if __name__ == "__main__":
    crear_tablas() #Se crean las tablas

    #Menu inicial
    po = 0
    while po != 3: #Ciclo para que se muestre hasta que el usuario quiera salir
        limpiar()
        po = int(input("""
Ingrese la opcion que quiere realizar
1- Carta
2- Personal
3- Salir
RTA: """)) 

        #Menu de productos
        if po == 1:
            op = 0
            while op != 5: #Ciclo para que se muestre hasta que el usuario quiera salir
                op = int(input("""
Ingrese la opcion que quiere realizar:
1- Cargar producto
2- Mostrar producto
3- Modificar producto
4- Eliminar producto
5- Volver
RTA: """))
                #Acciones del menu Carta
                if op == 1:
                    nombre = input("Ingrese el nombre del producto: ")
                    precio = int(input("Ingrese el precio del producto: "))
                    Cargar_Producto(nombre, precio)

                    input("Presione enter...")
                    limpiar()

                elif op == 2:
                    datos = Mostrar_Productos()
                    for i in range(0, len(datos)):
                        for j in range(0, 2):
                            if j == 0:
                                print(f"Nombre: {datos[i][j]}")
                            elif j == 1:
                                print(f"Precio: {datos[i][j]}")
                        print("-"*15)

                    input("Preisone Enter...")
                    limpiar()

                elif op == 3:
                    nombre = input("Ingrese el nombre del producto: ")
                    categoria = input("Ingrese lo que va a modificar si el preico o el stock: ")
                    valor_nuevo = int(input(f"Ingrese el {categoria} del producto: "))
                    Modificar_Productos(nombre, categoria.capitalize(), valor_nuevo)
                    
                    input("Presione enter...")
                    limpiar()

                elif op == 4:
                    nombre = input("Ingrese el nombre del producto a eliminar: ")
                    Eliminar_Producto(nombre)

                    input("Presione enter...")
                    limpiar()

        elif po == 2:

            #Menu de empleados
            pop = 0
            while pop != 6: #Ciclo para que se muestre hasta que el usuario quiera salir
                pop = int(input("""
Ingrese la opciona que quiere realizar:
1- Registrar nuevo empleado
2- Mostrar empleados
3- Modificar empleado
4- Eliminar empleado
5- Verificar
6- Volver
RTA: """))
                #Acciones del menu de empleados
                if pop == 1:
                    datos = Mostrar_Empleados()
                    
                    name = input("Ingrese el nombre del mozo: ")
                    
                    codigo = Generar_Codigo()

                    Plaza = int(input("Ingrese la plaza a la que va a estar asiganado: "))
        
                    Registro_Empleado(name, codigo, Plaza)

                    input("Presione enter...")
                    limpiar()
                elif pop == 2:
                    datos = Mostrar_Empleados()
                    for i in range(0, len(datos)):
                        for j in range(0, 4):
                            if j == 0:
                                print(f"Mozo: {datos[i][j]}")
                            elif j == 1:
                                print(f"Codigo: {datos[i][j]}")
                            elif j == 2:
                                print(f"Plaza: {datos[i][j]}")
                        print("-"*15)

                    input("Preisone Enter...")
                    limpiar()

                elif pop == 3:
                    name = input("Ingrese el nombre del mozo: ")
                    categoria = input("Que quiere cambiar el codigo o la plaza?: ")
                    
                    if categoria.capitalize() == "Codigo":
                        valor_nuevo = Generar_Codigo()
                        print("Espere cambiando codigo...")

                        time.sleep(5)

                        input("Cambiado con exito!!(Preisone enter...)")
                    elif categoria.capitalize() == "Plaza":
                        valor_nuevo = int(input("Ingrese la nueva plaza: "))
                        input("Preisone Enter...")

                    Modificar_Empleados(name, categoria, valor_nuevo)
                    limpiar()
                    
                elif pop == 4:
                    name = input("Ingrese el nombre del mozo a eliminar: ")
                    Eliminar_empleados(name)

                    input("Preisone Enter...")
                    limpiar()
                
                elif pop == 5:
                    name = input("Ingrese su nombre: ")
                    code = input("Ingrese su codigo: ")
                    
                    resultado = verificar(name, code)
                    if resultado == True:
                        print("Bienvenido")
                    elif resultado == 2:
                        print("Usted no esta en el sistema")
                    else:
                        print("Su codigo no es correcto")

                    input("Preisone Enter...")
                    limpiar()