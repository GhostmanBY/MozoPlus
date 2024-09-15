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
    valor: list[str]


# Endpoint para ver las mesas


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
        "Mozo": {},
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
            "Mozo": [],
        }
        with open(f"Docs/mesas.json", "w") as file:
            json.dump(mesas, file, indent=4)


# endpoint para editar una mesa a la ruta /mesas/{mesa} se remplaza {mesa} por el numero de la mesa


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


async def abrir_mesa(mesa: int, mozo: str):
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
        "Mozo": mozo,
    }

    try:
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


async def cerrar_mesa(mesa: int):
    """
    Cierra una mesa y actualiza su disponibilidad a True.
    """
    archivo = f"tmp/Mesa {mesa}.json"
    try:
        # Leemos el archivo de la mesa
        with open(archivo, "r") as file:
            contenido = file.read()

        data = json.loads(contenido)

        nombre_mozo = data["Mozo"]

        # Captura de la hora de cierre de la mesa y el dia
        fecha_hoy = datetime.datetime.now().date()
        fecha_txt = datetime.datetime.now()
        fecha = fecha_txt.strftime("%H:%M")

        # Añade la hora al json
        data.update({"Hora": fecha})

        # Guarda los cambios
        with open(f"Docs/{fecha_hoy}_{nombre_mozo}.json", "a") as file:
            json.dump(data, file, indent=4)

        # Actualizamos el estado de la mesa
        mesa_data = {
            "Mesa": mesa,
            "Disponible": True,
            "productos": [],
            "cantidad_comensales": 0,
            "comensales_infantiles": [False, 0],
            "Mozo": [],
        }
        # Guardamos los cambios en el archivo
        with open(archivo, "w") as file:
            json.dump(mesa_data, file, indent=4)

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
    crear_comanda(mesa, nombre_mozo)


def cantidad_de_mesas():
    """
    Cuenta la cantidad de mesas totales.
    """
    cantidad = {"tables": []}

    for i in range(len(os.listdir("tmp"))):
        cantidad["tables"].append([{"id": {i + 1}}])
    return cantidad


# MARK: UTILS
def verifica_directorio(directorio):
    """
    Verifica si el directorio existe, si no es asi, lo crea.
    """
    if not os.path.exists(directorio):
        os.makedirs(directorio)


def crear_comanda(mesa, mesero):
    """
    Crea una comanda con un formato específico y la guarda en un archivo.

    :param mesa: Número de mesa
    :param mesero: Nombre del mesero
    """
    items = []
    with open(f"tmp/Mesa {mesa}.json", "r") as file:
        data = json.load(file)
        productos = data["productos"]
        file.close()
    with open(f"Docs/Menu.json", "r") as file:
        menu = json.load(file)
        file.close()

    for categoria in menu:
        for item in productos:
            for plato in menu[categoria]:

                if item == plato["Nombre"]:
                    items.append([plato["Nombre"], 1, plato["Precio"]])

    # Generar un número único para la comanda
    numero_comanda = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")

    # Calcular el total
    total = sum(cantidad * precio for _, cantidad, precio in items)

    # Crear el contenido de la comanda
    contenido = f"""
=======================================
           COMANDA #{numero_comanda}
=======================================
Fecha: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Mesa: {mesa}
Mesero: {mesero}

Items:
---------------------------------------
{"Item".ljust(20)} {"Cant.".rjust(5)} {"Precio".rjust(10)} {"Total".rjust(10)}
---------------------------------------
"""

    for item, cantidad, precio in items:
        subtotal = cantidad * precio
        contenido += f"{item.ljust(20)} {str(cantidad).rjust(5)} {f'${precio:.2f}'.rjust(10)} {f'${subtotal:.2f}'.rjust(10)}\n"

    contenido += f"""
---------------------------------------
{"TOTAL:".ljust(36)} {f'${total:.2f}'.rjust(10)}
=======================================
"""

    # Guardar la comanda en un archivo
    with open(f"Docs/comandas/comanda_{numero_comanda}.txt", "w") as archivo:
        archivo.write(contenido)

    print(f"Comanda #{numero_comanda} creada y guardada exitosamente.")


if __name__ == "__main__":
    import uvicorn

    crear_comanda(1, "Juan")
