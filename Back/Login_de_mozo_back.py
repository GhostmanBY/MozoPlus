import sqlite3
import os
import json
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

ruta_db = os.path.join(base_dir, "../DB/Panel_admin.db")
Mozo_registro = {}

fecha_hoy = datetime.datetime.now().date()
fecha_txt = datetime.datetime.now()
fecha = fecha_txt.strftime("%H:%M")

ruta_registro = os.path.join(base_dir, f"../Docs/registro_mozos_{fecha_hoy}.json")

async def verificar(code: str):
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
                    "Mesas totales": None
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

                with open(ruta_registro, "w", encoding="utf-8") as file:
                    json.dump(registro, file, ensure_ascii=False, indent=4)
                data = {
                    "verificado": 1,
                    "ID": filas[0],
                    "Nombre": filas[1]
                } 
                return data #code encontrado
    return 0

def login_out(code: int):
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
            with open(os.path.join(base_dir, f"Docs/{fecha_hoy}_{nombre_mozo}.json"), "r", encoding="utf-8") as file:
                mesas = json.load(file)

            # Intenta cargar el archivo registro, si no existe, inicializa 'registro' como una lista vacía
            if os.path.exists(ruta_registro):
                with open(ruta_registro, "r", encoding="utf-8") as file:
                    registro = json.load(file)
                    print(registro)
            else:
                registro = []  # Inicializa registro como lista vacía si no existe el archivo

            # Verifica si 'registro' es una lista
            if isinstance(registro, list):
                mozo_encontrado = None
                for item in registro:
                    if nombre_mozo in item:  # Verificar si el nombre del mozo es una clave
                        mozo_encontrado = item
                        print("nombre mozo: ", nombre_mozo)
                        print("nombre mozo encontrado: ", mozo_encontrado)
                        break

                # Actualiza los datos del mozo encontrado
                if mozo_encontrado:
                    mozo_encontrado[nombre_mozo]['Horario_salida'] = fecha
                    mozo_encontrado[nombre_mozo]['Mesas totales'] = len(mesas)

                # Guarda el diccionario actualizado en el archivo JSON
                with open(ruta_registro, "w", encoding="utf-8") as file:
                    json.dump(registro, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    login_out("ZNMC547")
