import os
import time
import random
import sqlite3
import json
import datetime
from fastapi.responses import JSONResponse
from models import Mesa, ValorInput

base_dir = os.path.dirname(os.path.abspath(__file__))

# Captura de la hora de cierre de la mesa y el día
fecha_hoy = datetime.datetime.now().date()
fecha_txt = datetime.datetime.now()
fecha = fecha_txt.strftime("%H:%M")

# MARK: MESAS


async def ver_mesas():
    """
    Devuelve una lista con las mesas y sus respectivos valores.
    """
    mesas = []
    # Listar y filtrar los archivos en el directorio 'tmp'
    archivos = sorted(
        [
            name
            for name in os.listdir(os.path.join(base_dir, "../tmp"))
            if os.path.isfile(os.path.join(os.path.join(base_dir, "../tmp"), name))
        ]
    )

    # Recorrer los archivos esperados
    for i in range(len(archivos)):
        archivo = os.path.join(base_dir, f"../tmp/Mesa {i+1}.json")
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as file:
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
    with open(
        os.path.join(base_dir, f"../Docs/mesas.json"), "r", encoding="utf-8"
    ) as file:
        mesas = json.load(file)

    for mesa in mesas:
        with open(
            os.path.join(base_dir, f"../tmp/{mesa}.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(mesas[mesa], file, ensure_ascii=False, indent=4)

    return {
        "Disponible": True,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": [False, 0],
        "Mozo": {},
        "Pagado": False,
        "Metodo": "",
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
            "Pagado": False,
            "Metodo": "",
        }
        with open(
            os.path.join(base_dir, f"../Docs/mesas.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(mesas, file, ensure_ascii=False, indent=4)


# endpoint para editar una mesa a la ruta /mesas/{mesa} se remplaza {mesa} por el numero de la mesa


async def editar_mesa(mesa: int, input: ValorInput):
    """
    Edita una mesa reemplazando los valores de la categoria {categoria} con {valor}.
    """
    archivo = os.path.join(
        base_dir, f"../tmp/Mesa {mesa}.json"
    )  # Consistencia en el nombre del archivo
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = json.load(file)
        if contenido["Disponible"] == "true" or contenido["Disponible"] == True:
            return JSONResponse(content=f"Mesa {mesa} no disponible", status_code=400)
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

        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(contenido, file, ensure_ascii=False, indent=4)

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
    verifica_directorio(os.path.join(base_dir, "tmp"))
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa}.json")

    mesa_data = {
        "Mesa": mesa,
        "Disponible": False,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": [False, 0],
        "Mozo": mozo,
        "Hora": fecha,
        "Fecha": str(fecha_hoy),
        "Pagado": False,
        "Metodo": "",
    }

    try:
        # Guardamos los cambios en el archivo
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(mesa_data, file, ensure_ascii=False, indent=4)

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
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa}.json")
    try:
        # Leemos el archivo de la mesa
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = file.read()

        # Convertimos el contenido a un diccionario
        data = json.loads(contenido)

        if data["Disponible"]:
            return JSONResponse(
                content=f"Mesa {mesa} no disponible, debe abrirla primero",
                status_code=400,
            )

        nombre_mozo = data["Mozo"]

        # Añade la hora de cierre al JSON de la mesa
        data.update({"Hora_cierre": fecha})

        # Archivo de comandas por fecha y mozo
        comanda_archivo = os.path.join(
            base_dir, f"../Docs/Registro/{fecha_hoy}_{nombre_mozo}.json"
        )

        # Cargar comandas existentes o iniciar lista vacía
        if os.path.exists(comanda_archivo):
            with open(comanda_archivo, "r", encoding="utf-8") as file:
                try:
                    comandas = json.load(file)
                except json.JSONDecodeError:
                    comandas = []
        else:
            comandas = []

        # Añadir la nueva comanda
        comandas.append(data)

        # Sobrescribir el archivo con todas las comandas
        with open(comanda_archivo, "w", encoding="utf-8") as file:
            json.dump(comandas, file, ensure_ascii=False, indent=4)

        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return JSONResponse(
            content=f"Mesa {mesa} cerrada", media_type="application/json"
        )

    except FileNotFoundError:
        # Si el archivo no existe, devuelve un error 404
        return JSONResponse(content="Mesa no encontrada", status_code=404)
    except json.JSONDecodeError:
        # Error al decodificar el JSON
        return JSONResponse(
            content="Error al procesar el archivo JSON", status_code=400
        )
    except Exception as e:
        # Cualquier otro error, devuelve un error 500
        return JSONResponse(
            content=f"Error al cerrar la mesa: {str(e)}", status_code=500
        )


async def restaurar_mesa(mesa: int):
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa}.json")

    # Actualizamos el estado de la mesa a disponible
    mesa_data = {
        "Mesa": mesa,
        "Disponible": True,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": [False, 0],
        "Mozo": [],
    }

    # Guardamos los cambios en el archivo de la mesa
    with open(archivo, "w", encoding="utf-8") as file:
        json.dump(mesa_data, file, ensure_ascii=False, indent=4)


def cantidad_de_mesas():
    """
    Cuenta la cantidad de mesas totales.
    """
    cantidad = {"tables": []}


    for i in range(len(os.listdir(os.path.join(base_dir, "../tmp")))):
        with open(os.path.join(base_dir, f"../tmp/Mesa {i+1}.json"), "r", encoding="utf-8") as file:
            mesa_tmp = json.load(file)
        cantidad["tables"].append({"id": i + 1,"Dispo": mesa_tmp["Disponible"]})
    return cantidad

    # return cantidad


async def crear_comanda(mesa):
    """
    Crea una comanda con un formato específico y la guarda en un archivo.

    :param mesa: Número de mesa
    :param mesero: Nombre del mesero
    """
    items = []
    with open(
        os.path.join(base_dir, f"../tmp/Mesa {mesa}.json"), "r", encoding="utf-8"
    ) as file:
        data = json.load(file)
        mozo = data["Mozo"]
        productos = data["productos"]
        pagado = data["Pagado"]
        metodo = data["Metodo"]
        file.close()
    with open(
        os.path.join(base_dir, f"../Docs/Menu.json"), "r", encoding="utf-8"
    ) as file:
        menu = json.load(file)
        file.close()

    for categoria in menu["menu"]:
        for item in productos:
            for plato in menu["menu"][categoria]:

                if item == plato["name"]:
                    items.append([plato["name"], 1, plato["price"]])

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
Mozo: {mozo}

--------------------------------------------------
{"Item".ljust(20)} {"Cant.".rjust(5)} {"Precio".rjust(10)} {"Total".rjust(10)}
--------------------------------------------------
"""

    for item, cantidad, precio in items:
        subtotal = cantidad * precio
        contenido += f"{item.ljust(20)} {str(cantidad).rjust(5)} {f'${precio:,.2f}'.rjust(10)} {f'${subtotal:,.2f}'.rjust(10)}\n"

    contenido += f"""
---------------------------------------------------
{"TOTAL:".ljust(36)} {f'${total:,.2f}'.rjust(10)}
===================================================
"""

    # Guardar la comanda en un archivo
    with open(
        os.path.join(base_dir, f"../Docs/comandas/comanda_{numero_comanda}.txt"),
        "w",
        encoding="utf-8",
    ) as archivo:
        archivo.write(contenido)

    # print(f"Comanda #{numero_comanda} creada y guardada exitosamente.")


# MARK: UTILS
def verifica_directorio(directorio):
    """
    Verifica si el directorio existe, si no es asi, lo crea.
    """
    if not os.path.exists(directorio):
        os.makedirs(directorio)


def dividir_cuenta(mesa, cantidad):
    total = 0
    with open(
        os.path.join(base_dir, f"../tmp/Mesa {mesa}.json"), "r", encoding="utf-8"
    ) as file:
        data = json.load(file)
        productos = data["productos"]
        file.close()

    with open(
        os.path.join(base_dir, f"../Docs/Menu.json"), "r", encoding="utf-8"
    ) as file:
        menu = json.load(file)
        file.close()

    for categoria in menu:
        for item in productos:
            for plato in menu[categoria]:

                if item == plato["Nombre"]:
                    total += float(plato["Precio"])
    total = total / cantidad
    total = round(total, 2)
    return total


if __name__ == "__main__":
    creas_mesas(10)
    crea_mesas_tmp()
    