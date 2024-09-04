import os
import time
import random
import sqlite3
from fastapi import FastAPI

ruta_db = os.path.join("DB", "Panel_admin.db")

def limpiar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# MARK: DB
# Creacion de las tables
def crear_tablas():
    conn = sqlite3.connect(ruta_db)  # Se conecta a la base de datos creada
    cursor = conn.cursor()  # Crea el cursor para ejecutar comandos en la base de datos

    # Ejecuta una instruccion
    # Se crean las tabla si no existen (por eso la aclaracion de IF NOT), una vez la tabla creada crea la columna con su tipo de dato
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Menu(
        Categoria TEXT,
        Nombre TEXT,
        Precio INTEGER)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Usuario(
        ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        Nombre TEXT,
        Codigo TEXT,
        Plaza INTEGER)"""
    )

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

#MARK: FuncionesAUX
# Funcion que genera un codigo con 4 letras y 3 numeros, para la identificacion de los mozos
def Generar_Codigo():
    lista_Letras = [
        "A", "B", "C", "D", "E", "F",
        "G", "H", "I", "J", "K", "L",
        "M", "N", "O", "P", "Q", "S", 
        "T", "R", "U", "V", "W", "X", 
        "Y", "Z",
    ]
    # Se inicializa codigo para poder iterar los espacios del str
    codigo = list("AOOE505")
    # Un ciclo for para iterar la variable de codigo
    for i in range(0, 6):
        # Se utiliza el motodo radiant de la libreria ramdom para elejir una letra de forma alatoria
        valor_R_letra = random.randint(0, len(lista_Letras) - 1)
        # If para que pare de sumar letras y pase a añadir numeros del 0 al 9
        if i <= 3:
            codigo[i] = lista_Letras[valor_R_letra]
        elif i <= 6:
            valor_R_numero = random.randint(0, 9)

            # Se le asigna el numero pero como un str para que haga conflictos con la iteracion de la variable
            codigo[i] = str(valor_R_numero)

    # Una vez que el codigo ya tiene sus caracteres corespondientes, se vuelve a unir la lista en una sola cadena con el .join
    codigo = "".join(codigo)

    return codigo


# MARK: empleados
def Alta_Mozo(name, codigo, Plaza):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"INSERT INTO Usuario (nombre, codigo, plaza) VALUES (?, ?, ?)"  # Ingresa a la base de datos los valores que resive por eso es INSERT
    cursor.execute(instruccion, (name, codigo, Plaza))  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


def Mostrar_Mozos():
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * FROM Usuario"  # Captura todos los datos de la base de datos por eso SELECT
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = cursor.fetchall()

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    return datos


def Editar_Mozo(name, categoria, valor):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * from Usuario WHERE Mozo like '{name}'"
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices

    if datos:  # Se ve si datos tiene o no valores
        instruccion = f"UPDATE Usuario SET {categoria} = ? WHERE Mozo like ?"  # Se actualiza los datos
        cursor.execute(instruccion, (valor, name))  # Ejecuta la accion
        conn.commit()  # Guarda los cambios hechos a la base de datos
    else:
        return "No se encunetra el nombre del mozo ingresado"

    conn.close()  # Cierra la coneccion con la base de datos


def Eliminar_empleados(name):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"DELETE FROM Usuario WHERE Mozo like '{name}'"  # Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos



# MARK: MENUS
def Cargar_Producto(name, precio):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Se crea una variable para darle instrucciones, estas se dan con parametros especificos propios de SQL
    instruccion = "INSERT INTO Productos (nombre, precio) VALUES (?, ?)"  # Ingresa a la base de datos los valores que resive por eso es INSERT
    cursor.execute(instruccion, (name, precio))  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


def Modificar_Productos(name, categoria, nuevo_valor):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"UPDATE Productos SET {categoria} = {nuevo_valor} WHERE Nombre like '{name}'"  # Actualiza los valores que se le indiquen en la base de datos por eso UPDATE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


def Mostrar_Productos():
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * FROM Productos"  # Captura todos los datos de la base de datos por eso SELECT
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    return datos


def Eliminar_Producto(name):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"DELETE FROM Productos WHERE Nombre like '{name}'"  # Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

if __name__ == "__main__":
    crear_tablas()
    codigo=Generar_Codigo()
    Alta_Mozo("Nahuel Romero", codigo, 2)
    print(Mostrar_Mozos())
