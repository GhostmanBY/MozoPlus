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
        mozo_existente = False
        for item in registro:
            if nombre_mozo in item:
                mozo_existente = True
                item[nombre_mozo]["Horario_entrada"] = fecha
                break

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
    # Bloque para la fecha y hora
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
        if name == filas[1]:
            nombre_mozo = filas[1]

            ruta_mesas = os.path.join(base_dir, f"../Docs/Registro/{fecha_hoy}_{nombre_mozo}.json")

            if os.path.exists(ruta_mesas):
                with open(ruta_mesas, "r", encoding="utf-8") as file:
                    mesas = json.load(file)
            else:
                mesas = []

            if os.path.exists(ruta_registro):
                with open(ruta_registro, "r", encoding="utf-8") as file:
                    registro = json.load(file)
            else:
                return {"message": "No se ha cargado el sistema de login"}

            for item in registro:
                if nombre_mozo in item:
                    item[nombre_mozo]['Horario_salida'] = fecha
                    item[nombre_mozo]['Mesas totales'] = len(mesas)
                    break
            else:
                return {"message": f"No se encontró el registro para el mozo {nombre_mozo}"}

            with open(ruta_registro, "w", encoding="utf-8") as file:
                json.dump(registro, file, ensure_ascii=False, indent=4)
            
            return {"message": f"Salida registrada para {nombre_mozo}"}

    return {"message": f"No se encontró el mozo {name}"}

if __name__ == "__main__":
    #verificar("admin")
    login_out("Juan Pérez")
