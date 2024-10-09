import sqlite3
import os
import json
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

ruta_db = os.path.join(base_dir, "../DB/Panel_admin.db")
Mozo_registro = {}

async def verificar(code: str):
    #bloque para la fecha y hora
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")
    
    ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")

    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = "SELECT * from Usuario"  # Captura en especifico de la columna mozo el nombre que se le ingresa
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices
    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    for filas in datos:        
        if datos != []:  # Comprobacion si tiene datos o no
            if code == filas[2]:
                Mozo_registro[f"{filas[1]}"]= {
                    "Horario_entrada": fecha,
                    "Horario_salida": None,
                    "Mesas totales": None,
                    "Fecha": f"{fecha_hoy}"
                }

                # Cargar comandas existentes o iniciar lista vacía
                if os.path.exists(ruta_registro):
                    with open(ruta_registro, "r", encoding="utf-8") as file:
                        try:
                            registro = json.load(file)
                        except json.JSONDecodeError:
                            registro = []
                else:
                    registro = []

                registro.append(Mozo_registro)
                for i in range(len(registro)):
                    print(f"Empleado: {registro[i]}\n")

                with open(ruta_registro, "w", encoding="utf-8") as file:
                    json.dump(registro, file, ensure_ascii=False, indent=4)
                    
                data = {
                    "verificado": 1,
                    "ID": filas[0],
                    "Nombre": filas[1]
                } 
                return data #code encontrado
    return 0

async def login_out(code: int):
    #bloque para la fecha y hora
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")
    
    ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")

    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = "SELECT * from Usuario"
    cursor.execute(instruccion)

    datos = cursor.fetchall()

    conn.commit()
    conn.close()

    for filas in datos:
        if code == filas[2]:
            nombre_mozo = filas[1]

            # Abre el archivo JSON que contiene las mesas del mozo
            with open(os.path.join(base_dir, f"../Docs/Registro/{fecha_hoy}_{nombre_mozo}.json"), "r", encoding="utf-8") as file:
                mesas = json.load(file)

            # Intenta cargar el archivo registro, si no existe, inicializa 'registro' como una lista vacía
            if os.path.exists(ruta_registro):
                with open(ruta_registro, "r", encoding="utf-8") as file:
                    registro = json.load(file)
                    print(registro)
            else:
                return f"No se a cargado el sistem de login"
                break

            # Verifica si 'registro' es una lista
            if isinstance(registro, list):
                for i in range(len(registro)):
                    for item in registro:
                        if nombre_mozo in item:  # Verificar si el nombre del mozo es una clave
                            print(registro)
                            registro[i][nombre_mozo]['Horario_salida'] = fecha
                            registro[i][nombre_mozo]['Mesas totales'] = len(mesas)
                            break

                # Guarda el diccionario actualizado en el archivo JSON
                with open(ruta_registro, "w", encoding="utf-8") as file:
                    print(nombre_mozo)
                    json.dump(registro, file, ensure_ascii=False, indent=4)
        break

if __name__ == "__main__":
    verificar("admin")
    login_out("admin")
