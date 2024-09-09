import sqlite3
import os
from fastapi import FastAPI
import uvicorn

ruta_db = os.path.join("DB", "Panel_admin.db")


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
                print(filas)
                data = {
                    "verificado": 1,
                    "ID": filas[0],
                    "Nombre": filas[1],
                    "Plaza": filas[3]
                } 
                return data #code encontrado
    return 0
        
