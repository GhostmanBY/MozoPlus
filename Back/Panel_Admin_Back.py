import os
import json
import random
import sqlite3

base_dir = os.path.dirname(os.path.abspath(__file__))

ruta_db = os.path.join(base_dir, "../DB/Panel_admin.db")
ruta_json = os.path.join(base_dir, "../Docs/mesas.json")


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
        Codigo TEXT)"""
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
def Alta_Mozo(name):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * FROM Usuario WHERE nombre = ?"
    cursor.execute(instruccion, (name,))

    if cursor.fetchone() is None:
        instruccion = f"INSERT INTO Usuario (nombre, codigo) VALUES (?, ?)"  # Ingresa a la base de datos los valores que resive por eso es INSERT
        cursor.execute(instruccion, (name, Generar_Codigo()))  # Ejecuta la accion
    else: return "Mozo existente"

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


def Mostrar_Mozos(pagina):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Límite de mozos por página
    limite = 25
    offset = pagina * limite

    # Consulta SQL con límite y desplazamiento
    cursor.execute("SELECT * FROM Usuario LIMIT ? OFFSET ?", (limite, offset))  # Ejecuta la accion

    datos = cursor.fetchall()

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    return datos


def Editar_Mozo(name, categoria, valor):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * from Usuario WHERE Nombre like '{name}'"
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices

    if datos:  # Se ve si datos tiene o no valores
        instruccion = f"UPDATE Usuario SET {categoria} = ? WHERE Nombre like ?"  # Se actualiza los datos
        cursor.execute(instruccion, (valor, name))  # Ejecuta la accion
        conn.commit()  # Guarda los cambios hechos a la base de datos
    else:
        return "No se encunetra el nombre del mozo ingresado"

    conn.close()  # Cierra la coneccion con la base de datos


def Eliminar_empleados(name):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"DELETE FROM Usuario WHERE Nombre like '{name}'"  # Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


# MARK: MENUS
def Cargar_Producto(categoria, name, precio):
    name_new = name.capitalize()
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Se crea una variable para darle instrucciones, estas se dan con parametros especificos propios de SQL
    instruccion = "INSERT INTO Menu (categoria, nombre, precio) VALUES (?, ?, ?)"  # Ingresa a la base de datos los valores que resive por eso es INSERT
    cursor.execute(instruccion, (categoria, name_new, precio))  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos


def Modificar_Menu(name, categoria, nuevo_valor):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"UPDATE Menu SET {categoria} = {nuevo_valor} WHERE Nombre = '{name}'"  # Actualiza los valores que se le indiquen en la base de datos por eso UPDATE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos
    Recargar_menu()

def Mostrar_Menu(pagina):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Límite de platos por página
    limite = 50
    offset = pagina * limite

    # Consulta SQL con límite y desplazamiento
    cursor.execute("SELECT * FROM Menu LIMIT ? OFFSET ?", (limite, offset)) # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    return datos

def Mostrar_menu_json():
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"SELECT * FROM Menu"  # Captura todos los datos de la base de datos por eso SELECT
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = cursor.fetchall()

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    return datos


def Eliminar_Producto(name):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = f"DELETE FROM Menu WHERE Nombre = '{name}'"  # Elimina la fila en la que este el nombre que se le ingresa por eso DELETE
    cursor.execute(instruccion)  # Ejecuta la accion

    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos
    Recargar_menu()

def Recargar_menu():
    try:
        with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as json_file:
            data_disc = json.load(json_file)  # Cargar el contenido del archivo JSON
    except FileNotFoundError:
        # Si el archivo no existe, creamos una estructura base
        data_disc = {"menu": {}}

    # Obtener los nuevos productos desde la base de datos
    data = Mostrar_menu_json()

    # Organizar los datos en el diccionario
    for item in data:
        categoria = item[0]  # Categoría del producto (ej. "Asado")
        nombre = item[1]  # Nombre del producto (ej. "Carne")
        precio = item[2]  # Precio del producto (ej. 1500)

        if categoria not in data_disc["menu"]:
            data_disc["menu"][categoria] = []  # Si no existe la categoría, la creamos como una lista vacía
        
        # Verificar si el producto ya está dentro de la categoría
        if not any(prod['name'] == nombre for prod in data_disc["menu"][categoria]):
            # Si el producto no está presente, agregarlo
            data_disc["menu"][categoria].append({"name": nombre, "price": precio})

    # Guardar los cambios en el archivo JSON
    with open(os.path.join(base_dir, "../Docs/Menu.json"), "w", encoding="utf-8") as json_file:
        json.dump(data_disc, json_file, ensure_ascii=False, indent=4)

def obtener_menu_en_json():
    print(os.path.join(base_dir, "../Docs/Menu.json"))
    """Devuelve el contenido del menú en formato JSON, asegurando la codificación."""
    with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as file:
        return json.load(file)
        

if __name__ == "__main__":
    #crear_tablas()
    obtener_menu_en_json()
    #Recargar_menu()
    """# Bebidas
    Cargar_Producto("Bebidas", "Café Expreso", 400)
    Cargar_Producto("Bebidas", "Café Americano", 450)
    Cargar_Producto("Bebidas", "Café con Leche", 500)
    Cargar_Producto("Bebidas", "Té Negro", 350)
    Cargar_Producto("Bebidas", "Té Verde", 350)
    Cargar_Producto("Bebidas", "Limonada", 500)
    Cargar_Producto("Bebidas", "Jugo de Naranja Natural", 600)
    Cargar_Producto("Bebidas", "Chocolate Caliente", 550)
    Cargar_Producto("Bebidas", "Batido de Fresa", 700)
    Cargar_Producto("Bebidas", "Agua Mineral", 300)

    # Dulces
    Cargar_Producto("Dulces", "Tarta de Chocolate", 1200)
    Cargar_Producto("Dulces", "Brownie con Helado", 1300)
    Cargar_Producto("Dulces", "Cheesecake de Frutilla", 1100)
    Cargar_Producto("Dulces", "Croissant con Mermelada", 700)
    Cargar_Producto("Dulces", "Muffin de Arándanos", 800)
    Cargar_Producto("Dulces", "Medialuna", 500)
    Cargar_Producto("Dulces", "Churros con Dulce de Leche", 900)
    Cargar_Producto("Dulces", "Helado de Vainilla", 700)
    Cargar_Producto("Dulces", "Pastel de Manzana", 1000)
    Cargar_Producto("Dulces", "Alfajor de Maicena", 450)

    # Salados
    Cargar_Producto("Salados", "Sándwich de Jamón y Queso", 900)
    Cargar_Producto("Salados", "Medialuna con Jamón y Queso", 800)
    Cargar_Producto("Salados", "Empanada de Carne", 700)
    Cargar_Producto("Salados", "Empanada de Pollo", 700)
    Cargar_Producto("Salados", "Pizza Margarita", 1200)
    Cargar_Producto("Salados", "Tostado de Jamón y Queso", 950)
    Cargar_Producto("Salados", "Panini de Pollo", 1100)
    Cargar_Producto("Salados", "Hamburguesa Clásica", 1500)
    Cargar_Producto("Salados", "Wrap de Pollo", 1200)
    Cargar_Producto("Salados", "Tarta de Verduras", 900)

    # Postres
    Cargar_Producto("Postres", "Flan Casero", 600)
    Cargar_Producto("Postres", "Tiramisú", 1000)
    Cargar_Producto("Postres", "Frutillas con Crema", 900)
    Cargar_Producto("Postres", "Mousse de Chocolate", 850)
    Cargar_Producto("Postres", "Helado de Chocolate", 700)
    Cargar_Producto("Postres", "Torta de Zanahoria", 1200)
    Cargar_Producto("Postres", "Crepes con Dulce de Leche", 1100)
    Cargar_Producto("Postres", "Tarta de Limón", 1150)
    Cargar_Producto("Postres", "Budín de Pan", 650)
    Cargar_Producto("Postres", "Helado de Dulce de Leche", 700)"""

    #Recargar_menu()

    """Alta_Mozo("Santiago Mono")
    Alta_Mozo("Juan Pérez")
    Alta_Mozo("María García")
    Alta_Mozo("Carlos Rodríguez")
    Alta_Mozo("Lucía Fernández")
    Alta_Mozo("Pablo González")
    Alta_Mozo("Sofía Martínez")
    Alta_Mozo("Diego López")
    Alta_Mozo("Marta Sánchez")
    Alta_Mozo("Alejandro Ruiz")
    Alta_Mozo("Carmen Ramírez")
    Alta_Mozo("Francisco Torres")
    Alta_Mozo("Laura Díaz")
    Alta_Mozo("Javier Morales")
    Alta_Mozo("Verónica Castillo")
    Alta_Mozo("Luis Ortiz")
    Alta_Mozo("Carolina Ríos")
    Alta_Mozo("Miguel Herrera")
    Alta_Mozo("Gabriela Ponce")
    Alta_Mozo("Ricardo Varela")
    Alta_Mozo("Natalia Vega")
    Alta_Mozo("Tomás Medina")
    Alta_Mozo("Elena Fuentes")
    Alta_Mozo("Rodrigo Aguirre")
    Alta_Mozo("Paula Navarro")
    Alta_Mozo("Andrés Castro")"""

    # names = [
    # "Carlos", "Ana", "Luis", "Marta", "Jorge", "Lucía", "Pedro", "María", "Miguel", "Laura",
    # "Roberto", "Carmen", "Ricardo", "Paula", "Andrés", "Sofía", "Manuel", "Elena", "José", "Sandra",
    # "Gabriel", "Patricia", "Fernando", "Raquel", "Adrián", "Natalia", "David", "Rosa", "Diego", "Clara",
    # "Juan", "Beatriz", "Sergio", "Cristina", "Javier", "Isabel", "Pablo", "Teresa", "Ramón", "Inés",
    # "Raúl", "Susana", "Iván", "Silvia", "Óscar", "Verónica", "Alberto", "Lorena", "Enrique", "Esther",
    # "Alfonso", "Eva", "Mario", "Alejandra", "Francisco", "Julia", "Emilio", "Noelia", "Álvaro", "Nuria",
    # "Agustín", "Mónica", "Vicente", "Marisol", "Ángel", "Sara", "Rubén", "Belén", "Tomás", "Marina",
    # "Santiago", "Irene", "Eduardo", "Alicia", "Hugo", "Rocío", "Cristóbal", "Olga", "Martín", "Jimena",
    # "Gonzalo", "Aurora", "Esteban", "Fátima", "Nicolás", "Amparo", "Ramiro", "Gloria", "Fabián", "Lidia",
    # "Rafael", "Bárbara", "Rodrigo", "Ariadna", "Jesús", "Mercedes", "Sebastián", "Alma", "Bruno", "Victoria"
    # ]
    # for i in range(len(names)):
    #     Alta_Mozo(names[i])

    
