import os
import time
import random
import sqlite3
import json
import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
# MARK: MESAS


app = FastAPI()


class Mesa(BaseModel):
    disponible: bool
    productos: list
    cantidad_comensales: int
    comensales_infantiles: list


class ValorInput(BaseModel):
    categoria: str
    valor: list


# Endpoint para ver las mesas
@app.get("/mesas")
async def ver_mesas():
    """
    Devuelve una lista con las mesas y sus respectivos valores.
    """
    mesas = []
    # Listar y filtrar los archivos en el directorio 'tmp'
    archivos = sorted(
        [
            name
            for name in os.listdir("tmp")
            if os.path.isfile(os.path.join("tmp", name))
        ]
    )

    # Recorrer los archivos esperados
    for i in range(len(archivos)):
        archivo = f"tmp/Mesa {i+1}.json"
        if os.path.exists(archivo):
            with open(archivo, "r") as file:
                datos = json.load(file)
                mesas.append(
                    datos
                )  # Suponiendo que cada archivo contiene un diccionario
        else:
            print(f"Archivo {archivo} no encontrado.")

    return mesas


def crea_mesas_tmp():
    """
    Crea mesas con los valores por defecto en el directorio 'tmp'.
    """
    with open("Docs/mesas.json", "r") as file:
        mesas = json.load(file)

    for mesa in mesas:
        with open(f"tmp/{mesa}.json", "w") as file:
            json.dump(mesas[mesa], file, indent=4)

    return {
        "Disponible": True,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": [False, 0],
    }


def creas_mesas(cantidad):
    """
    Crea mesas con los valores por defecto en el archivo 'Docs/mesas.json'.
    """
    mesas = {}
    for i in range(1, cantidad + 1):
        mesas[f"Mesa {i}"] = {
            "Mesa": i,
            "Disponible": True,
            "productos": [],
            "cantidad_comensales": 0,
            "comensales_infantiles": [False, 0],
        }
        with open(f"Docs/mesas.json", "w") as file:
            json.dump(mesas, file, indent=4)


# endpoint para editar una mesa a la ruta /mesas/{mesa} se remplaza {mesa} por el numero de la mesa
@app.put("/mesas/{mesa}")
async def editar_mesa(mesa: int, input: ValorInput):
    """
    Edita una mesa reemplazando los valores de la categoria {categoria} con {valor}.
    """
    archivo = f"tmp/Mesa {mesa}.json"  # Consistencia en el nombre del archivo
    try:
        with open(archivo, "r") as file:
            contenido = json.load(file)

        if input.categoria not in contenido:
            return JSONResponse(
                content=f"Categoría {input.categoria} no existe en la mesa {mesa}",
                status_code=400,
            )

        # Verifica que el tipo de datos sea una lista
        if not isinstance(contenido[input.categoria], list):
            return JSONResponse(
                content=f"La categoría {input.categoria} no es una lista",
                status_code=400,
            )

        contenido[input.categoria].extend(input.valor)

        with open(archivo, "w") as file:
            json.dump(contenido, file, indent=4)

        return JSONResponse(
            content=f"Mesa número {mesa} {input.categoria} actualizada a {input.valor}",
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(content=f"Algo ha salido mal: {str(e)}", status_code=500)



@app.post("/mesas/{mesa}/abrir")
async def abrir_mesa(mesa: int):
    """
    Abre una mesa y actualiza su disponibilidad a False.
    """
    verifica_directorio("tmp")
    archivo = f"tmp/Mesa {mesa}.json"

    mesa_data = {
        "Mesa": mesa,
        "Disponible": False,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": [False, 0],
    }

    try:
        # Si el archivo ya existe, cargamos los datos
        if os.path.exists(archivo):
            with open(archivo, "r") as file:
                mesa_data = json.load(file)

        # Actualizamos el estado de disponibilidad
        mesa_data["Disponible"] = False

        # Guardamos los cambios en el archivo
        with open(archivo, "w") as file:
            json.dump(mesa_data, file, indent=4)

        return JSONResponse(
            content=f"Mesa {mesa} abierta y disponibilidad actualizada a False",
            media_type="application/json",
        )
    except Exception as e:
        return JSONResponse(
            content=f"Error al abrir la mesa: {str(e)}", status_code=500
        )


@app.post("/mesas/{mesa}/cerrar")
async def cerrar_mesa(mesa: int):
    """
    Cierra una mesa y actualiza su disponibilidad a False.
    """
    archivo = f"tmp/Mesa {mesa}.json"
    try:
        # Leemos el archivo de la mesa
        with open(archivo, "r") as file:
            contenido = file.read()
        # Guardamos el contenido en un archivo de texto
        fecha_hoy = datetime.datetime.now().date()
        with open(f"Docs/{fecha_hoy}.txt", "a") as txt:
            txt.write("\n\n" + str(datetime.datetime.now()) + "\n")
            txt.write(contenido)
        # Actualizamos el estado de la mesa
        mesa_data = {
            "Disponible": True,
            "productos": [],
            "cantidad_comensales": 0,
            "comensales_infantiles": [False, 0],
        }
        # Guardamos los cambios en el archivo
        with open(archivo, "w") as file:
            json.dump(mesa_data, file, indent=4)

        if os.path.exists(archivo):
            os.remove(archivo)
        return JSONResponse(
            content=f"Mesa {mesa} cerrada", media_type="application/json"
        )
    except FileNotFoundError:
        # Si el archivo no existe, devuelve un error 404
        return JSONResponse(content="Mesa no encontrada", status_code=404)
    except Exception as e:
        # Cualquier otro error, devuelve un error 500
        return JSONResponse(
            content=f"Error al cerrar la mesa: {str(e)}", status_code=500
        )


# MARK: UTILS
def verifica_directorio(directorio):
    """
    Verifica si el directorio existe, si no es asi, lo crea.
    """
    if not os.path.exists(directorio):
        os.makedirs(directorio)


if __name__ == "__main__":
    import uvicorn

    """creas_mesas(10)
    crea_mesas_tmp()"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

