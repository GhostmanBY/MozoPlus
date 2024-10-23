import sqlite3
import os
import json
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

ruta_db = os.path.join(base_dir, "../DB/Panel_admin.db")

async def verificar(code: str):
    # Bloque para la fecha y hora
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")

    ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")

    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = "SELECT * FROM Usuario WHERE codigo = ?"
    cursor.execute(instruccion, (code,))

    fila = cursor.fetchone()
    conn.close()

    if fila:
        nombre_mozo = fila[1]
        
        # Cargar registro existente o iniciar lista vacía
        if os.path.exists(ruta_registro):
            with open(ruta_registro, "r", encoding="utf-8") as file:
                try:
                    registro = json.load(file)
                except json.JSONDecodeError:
                    registro = []
        else:
            registro = []

        # Verificar si el mozo ya está registrado
        mozo_existente = any(nombre_mozo in mozo for mozo in registro)

        if not mozo_existente:
            Mozo_registro = {
                nombre_mozo: {
                    "Horario_entrada": fecha,
                    "Horario_salida": None,
                    "Mesas totales": None,
                    "Fecha": f"{fecha_hoy}"
                }
            }
            registro.append(Mozo_registro)

            with open(ruta_registro, "w", encoding="utf-8") as file:
                json.dump(registro, file, ensure_ascii=False, indent=4)

        data = {
            "verificado": 1,
            "ID": fila[0],
            "Nombre": nombre_mozo
        }
        return data  # Code encontrado y procesado
    return 0  # Code no encontrado

async def login_out(name: str):
    #bloque para la fecha y hora
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")
    
    ruta_registro_check = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")
    i = 1
    while os.path.exists(ruta_registro_check):
        
        ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}_{i+1}.json")
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = "SELECT * from Usuario"
    cursor.execute(instruccion)

    datos = cursor.fetchall()

    conn.commit()
    conn.close()

    for filas in datos:
        if name == filas[1]:
            print("a")
            nombre_mozo = filas[1]

            ruta_mesas = os.path.join(base_dir, f"../Docs/Registro/{fecha_hoy}_{nombre_mozo}.json")

            if os.path.exists(ruta_mesas):
                # Abre el archivo JSON que contiene las mesas del mozo
                with open(ruta_mesas, "r", encoding="utf-8") as file:
                    mesas = json.load(file)
            else:
                mesas = []

            # Intenta cargar el archivo registro, si no existe, inicializa 'registro' como una lista vacía
            if os.path.exists(ruta_registro):
                with open(ruta_registro, "r", encoding="utf-8") as file:
                    
                    registro = json.load(file)
                    if name in registro:
                        registro['Horario_salida'] = fecha
            else:
                return f"No se a cargado el sistema de login"

            # Verifica si 'registro' es una lista
            i = 0
            if isinstance(registro, list):
                for item in registro:
                    if nombre_mozo in item:  # Verificar si el nombre del mozo es una clave
                        registro[i][nombre_mozo]['Horario_salida'] = fecha
                        registro[i][nombre_mozo]['Mesas totales'] = len(mesas)
                        break
                    i += 1

                # Guarda el diccionario actualizado en el archivo JSON
                with open(ruta_registro, "w", encoding="utf-8") as file:
                    print(nombre_mozo)
                    json.dump(registro, file, ensure_ascii=False, indent=4)
        

if __name__ == "__main__":
    #verificar("admin")
    login_out("Juan Pérez")
