import sqlite3
import os
from fastapi import FastAPI
import uvicorn

ruta_db = os.path.join("DB", "Panel_admin.db")

app = FastAPI()
@app.post("/verificar/{code}")
async def verificar(code: str):
    # Se conecta a la base de datos y crea el cursor
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    instruccion = "SELECT * from Usuario"  # Captura en especifico de la columna mozo el nombre que se le ingresa
    cursor.execute(instruccion)  # Ejecuta la accion

    datos = (
        cursor.fetchall()
    )  # La variable datos pasa a tener todos los valores que tiene cursos, metiendo en una lista con sub indices
    print(datos)
    conn.commit()  # Guarda los cambios hechos a la base de datos
    conn.close()  # Cierra la coneccion con la base de datos

    for filas in datos:        
        if datos != []:  # Comprobacion si tiene datos o no
            if code == filas[1]:
                return f"{code} encontrado"
            else:
                return f"{code} no encontrado"
        else:
            return "No esta en el sistema"
        
uvicorn.run(app, host="127.0.0.1", port=8000)