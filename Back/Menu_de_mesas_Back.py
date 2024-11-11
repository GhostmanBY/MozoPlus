import os
import time
import random
import sqlite3
import json
import datetime
from fastapi.responses import JSONResponse
from escpos.printer import File
from PIL import Image

#Este if es para que cuando se compile desde el archivo no se tenga que cambiar la ruta de la importacion
if __name__ == "__main__":    
    from models import Mesa, ValorInput
else:
    from Back.models import Mesa, ValorInput

base_dir = os.path.dirname(os.path.abspath(__file__))



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
    print("Creando mesas temporales")
    
    # Borrar todas las mesas existentes en la carpeta tmp
    tmp_dir = os.path.join(base_dir, "../tmp")
    for archivo in os.listdir(tmp_dir):
        ruta_archivo = os.path.join(tmp_dir, archivo)
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
    
    # Generar nuevas mesas
    with open(os.path.join(base_dir, "../Docs/mesas.json"), "r", encoding="utf-8") as file:
        mesas = json.load(file)

    for mesa in mesas:
        with open(os.path.join(tmp_dir, f"{mesa}.json"), "w", encoding="utf-8") as file:
            json.dump(mesas[mesa], file, ensure_ascii=False, indent=4)
        print(f"Mesa creada: {mesa}")

    return {
        "Disponible": True,
        "productos": [],
        "cantidad_comensales": 0,
        "comensales_infantiles": 0,
        "Mozo": {},
        "Pagado": False,
        "Metodo": "",
        "Extra": None,
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
            "comensales_infantiles": 0,
            "Mozo": [],
            "Pagado": False,
            "Metodo": "",
            "Extra": None,
        }
        with open(
            os.path.join(base_dir, f"../Docs/mesas.json"), "w", encoding="utf-8"
        ) as file:
            json.dump(mesas, file, ensure_ascii=False, indent=4)


# endpoint para editar una mesa a la ruta /mesas/{mesa} se remplaza {mesa} por el numero de la mesa


async def guardar_mesa(mesa: int, input: ValorInput):
    """
    Edita una mesa reemplazando los valores de la categoria {categoria} con {valor}.
    """
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa}.json")
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = json.load(file)
        
        if contenido["Disponible"] == True:
            return JSONResponse(content=f"Mesa {mesa} no está ocupada", status_code=400)
        
        if input.categoria not in contenido:
            return JSONResponse(content=f"Categoría {input.categoria} no existe en la mesa {mesa}", status_code=400)

        if isinstance(input.valor, list):
            if isinstance(contenido[input.categoria], list):
                contenido[input.categoria] = input.valor
            else:
                contenido[input.categoria] = input.valor
        else:
            contenido[input.categoria] = input.valor

        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(contenido, file, ensure_ascii=False, indent=4)

        return JSONResponse(content=f"Mesa número {mesa} {input.categoria} actualizada a {input.valor}", media_type="application/json")
    except Exception as e:
        return JSONResponse(content=f"Algo ha salido mal: {str(e)}", status_code=500)

async def editar_mesa(mesa: int):

    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa}.json")

    try:
        with open(archivo, "r", encoding="utf-8") as file:
            contenido = json.load(file)

        return contenido

    except Exception as e:
        return JSONResponse(content=f"Algo ha salido mal: {str(e)}", status_code=500)


async def abrir_mesa(mesa: int, mozo: str):
    # Captura de la hora de cierre de la mesa y el día
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")
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
        "comensales_infantiles": 0,
        "Mozo": mozo,
        "Hora": fecha,
        "Fecha": str(fecha_hoy),
        "Pagado": False,
        "Metodo": "",
        "Extra": None
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
    # Captura de la hora de cierre de la mesa y el día
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")
    
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
        
        # Actualizamos el estado de la mesa a disponible
        mesa_data = {
            "Mesa": mesa,
            "Disponible": True,
            "productos": [],
            "cantidad_comensales": 0,
            "comensales_infantiles": 0,
            "Mozo": [],
            "Extra": None,
        }
        # Guardamos los cambios en el archivo de la mesa
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(mesa_data, file, ensure_ascii=False, indent=4)

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

def comanda_preview(numero_mesa, nombre_mozo, lista_platos):
    # Ruta del archivo JSON
    menu_path = os.path.join(base_dir, "../Docs/Menu.json")

    # Leer el menú desde el archivo JSON
    with open(menu_path, "r", encoding="utf-8") as file:
        menu = json.load(file)

    # Procesar lista de platos
    pedido_tmp = []
    pedido_cantidad = []
    for producto in lista_platos:
        if producto not in pedido_tmp:
            cantidad = lista_platos.count(producto)
            pedido_cantidad.append({producto: cantidad})
            #print(f"lista cantidad: {pedido_cantidad}")
            pedido_tmp.append(producto)
            #print(f"lista tmp2: {pedido_tmp}")
    
    # Calcular precios
    total = 0
    i = 0
    pedido_precio = []
    pedido_precio_tmp = []
    print(f"lista tmp: {pedido_precio}")
    for producto in pedido_tmp:
        for categoria in menu["menu"]:
            for item in menu["menu"][categoria]:
                if producto == item["name"]:
                    if producto not in pedido_precio_tmp: 
                        pedido_precio.append({producto: item["price"]})
                        pedido_precio_tmp.append(producto)
                        total += item["price"]
                        print(f"lista tmp: {pedido_precio}")   
            i += 1

    # Crear lista final de items
    item_final = []
    for i, producto in enumerate(pedido_tmp):
        item_final.append({
            "nombre": producto, 
            "cantidad": int(pedido_cantidad[i][producto]), 
            "precio": int(pedido_precio[i][producto])
        })

    # Función para dividir texto en líneas sin cortar palabras
    def split_text_preserving_words(text, length):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= length:
                current_line += (word + " ")
            else:
                if len(word) > length:
                    while len(word) > length:
                        lines.append(word[:length - 1] + "-")
                        word = word[length - 1:]
                    current_line = word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    # Ancho máximo del ticket
    max_ancho = 40

    # Configurar impresora
    printer = File(os.path.join(base_dir, f"../impresora/Comanda {numero_mesa}.bin"))

    # Función para centrar texto
    def center_text(text, width):
        return text.center(width)

    # Encabezado
    printer.text(center_text("COMANDA", max_ancho) + "\n")
    printer.text("=" * max_ancho + "\n")

    # Información del pedido
    fecha_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    printer.text(f"Fecha: {fecha_hora}\n")
    printer.text(f"Mesa: {numero_mesa}\n")
    printer.text(f"Mozo: {nombre_mozo}\n")
    printer.text("-" * max_ancho + "\n")

    # Encabezado de items
    printer.text(f"{'Producto':<20} {'Cant':>5} {'Precio':>8}\n")
    printer.text("-" * max_ancho + "\n")

    # Detalle de items
    total = 0
    for item in item_final:
        nombre = split_text_preserving_words(item["nombre"], 20)
        cantidad = item["cantidad"]
        subtotal = cantidad * item["precio"]
        total += subtotal

        # Imprimir la primera línea de nombre con cantidad y subtotal con signo de peso
        printer.text(f"{nombre[0]:<20} {cantidad:>5} {'$':>3}{subtotal:>8.2f}\n")

        # Imprimir las líneas adicionales de nombre si existen
        for line in nombre[1:]:
            printer.text(f"{line:<20}\n")

    # Total
    printer.text("-" * max_ancho + "\n")
    printer.text(f"{'Total:':<26} {'$':>1}{total:>7.2f}\n")
    printer.text("=" * max_ancho + "\n")

    # Mensaje final centrado
    printer.text(center_text("¡Gracias por su pedido!", max_ancho) + "\n")

    # Comando para cortar el papel
    printer.cut()


async def imprir(Mesa_numero):
    with open(os.path.join(base_dir, f"../tmp/Mesa {Mesa_numero}.json"), "r", encoding="utf-8") as file: 
        data = json.load(file)

    num = Mesa_numero
    name_mozo = data['Mozo']
    producto = data['productos']

    comanda_preview(num, name_mozo, producto)

def cantidad_de_mesas():
    """
    Cuenta la cantidad de mesas totales.
    """
    cantidad = {"tables": []}
    directorio_tmp = os.path.join(base_dir, "../tmp")
    
    try:
        print(f"Directorio tmp: {directorio_tmp}")
        archivos = sorted(os.listdir(directorio_tmp))
        print(f"Archivos en tmp: {archivos}")
        
        for i, archivo in enumerate(archivos):
            if archivo.startswith("Mesa") and archivo.endswith(".json"):
                ruta_archivo = os.path.join(directorio_tmp, archivo)
                print(f"Procesando archivo: {ruta_archivo}")
                with open(ruta_archivo, "r", encoding="utf-8") as file:
                    mesa_tmp = json.load(file)
                cantidad["tables"].append({"id": i + 1, "Dispo": mesa_tmp["Disponible"]})
        
        print(f"Cantidad final: {cantidad}")
        return cantidad
    except Exception as e:
        print(f"Error al procesar las mesas: {str(e)}")
        return {"error": f"Error al procesar las mesas: {str(e)}"}


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
        os.path.join(base_dir, f"../Docs/Comandas/comanda_{numero_comanda}.txt"),
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
        os.path.join(base_dir, f"../tmp/Mesa {mesa}.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
        productos = data["productos"]
        file.close()

    with open(
        os.path.join(base_dir, f"../Docs/Menu.json"), "r", encoding="utf-8") as file:
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


# Modelo de datos para una mesa con sub-mesas
mesas = {
    "1": {
        "sub_mesas": {
            "1A": {
                "productos": [],
                "total": 0.0
            },
            "1B": {
                "productos": [],
                "total": 0.0
            }
        }
    }
    # Puedes agregar más mesas y sub-mesas según sea necesario
}

async def crear_sub_mesa(mesa_num, sub_mesa_id):
    """Crea una nueva sub-mesa dentro de una mesa existente."""
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa_num}.json")
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            mesa_data = json.load(file)
        
        if "sub_mesas" not in mesa_data:
            mesa_data["sub_mesas"] = {}
        
        mesa_data["sub_mesas"][sub_mesa_id] = {
            "Mesa": sub_mesa_id,
            "productos": [],
            "cantidad_comensales": 0,
            "comensales_infantiles": 0,
            "Extra": None,
        }

        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(mesa_data, file, ensure_ascii=False, indent=4)

        return JSONResponse(content=f"Sub-mesa {sub_mesa_id} creada en mesa {mesa_num}", media_type="application/json")
    except Exception as e:
        return JSONResponse(content=f"Error al crear sub-mesa: {str(e)}", status_code=500)

async def editar_sub_mesa(mesa_num, sub_mesa_id, input: ValorInput):
    """Edita una sub-mesa reemplazando los valores de la categoría {categoria} con {valor}."""
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa_num}.json")
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            mesa_data = json.load(file)
        
        if "sub_mesas" in mesa_data and sub_mesa_id in mesa_data["sub_mesas"]:
            sub_mesa = mesa_data["sub_mesas"][sub_mesa_id]
            
            if input.categoria not in sub_mesa:
                return JSONResponse(content=f"Categoría {input.categoria} no existe en la sub-mesa {sub_mesa_id}", status_code=400)

            if isinstance(input.valor, list):
                if isinstance(sub_mesa[input.categoria], list):
                    sub_mesa[input.categoria] = input.valor
                else:
                    sub_mesa[input.categoria] = input.valor
            else:
                sub_mesa[input.categoria] = input.valor

            with open(archivo, "w", encoding="utf-8") as file:
                json.dump(mesa_data, file, ensure_ascii=False, indent=4)

            return JSONResponse(content=f"Sub-mesa {sub_mesa_id} en mesa {mesa_num} {input.categoria} actualizada a {input.valor}", media_type="application/json")
        else:
            return JSONResponse(content=f"Sub-mesa {sub_mesa_id} no encontrada en mesa {mesa_num}", status_code=404)
    except Exception as e:
        return JSONResponse(content=f"Error al editar sub-mesa: {str(e)}", status_code=500)

async def cerrar_sub_mesa(mesa_num, sub_mesa_id):
    """Cierra una sub-mesa y procesa el pago."""
    archivo = os.path.join(base_dir, f"../tmp/Mesa {mesa_num}.json")
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            mesa_data = json.load(file)
        
        if "sub_mesas" in mesa_data and sub_mesa_id in mesa_data["sub_mesas"]:
            sub_mesa = mesa_data["sub_mesas"][sub_mesa_id]
            
            # Crear comanda para la sub-mesa
            await crear_comanda_sub_mesa(mesa_num, sub_mesa_id, sub_mesa)

            # Eliminar la sub-mesa
            del mesa_data["sub_mesas"][sub_mesa_id]

            with open(archivo, "w", encoding="utf-8") as file:
                json.dump(mesa_data, file, ensure_ascii=False, indent=4)

            return JSONResponse(content=f"Sub-mesa {sub_mesa_id} cerrada en mesa {mesa_num}", media_type="application/json")
        else:
            return JSONResponse(content=f"Sub-mesa {sub_mesa_id} no encontrada en mesa {mesa_num}", status_code=404)
    except Exception as e:
        return JSONResponse(content=f"Error al cerrar sub-mesa: {str(e)}", status_code=500)

async def crear_comanda_sub_mesa(mesa_num, sub_mesa_id, sub_mesa):
    """Crea una comanda para una sub-mesa y la guarda en un archivo."""
    items = sub_mesa["productos"]
    numero_comanda = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
    total = 0

    contenido = f"""
=======================================
    COMANDA SUB-MESA #{numero_comanda}
=======================================
Fecha: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Mesa: {mesa_num}
Sub-Mesa: {sub_mesa_id}

--------------------------------------------------
{"Item".ljust(20)} {"Cant.".rjust(5)} {"Precio".rjust(10)} {"Total".rjust(10)}
--------------------------------------------------
"""

    # Supongamos que tienes un archivo de menú donde puedes buscar los detalles de cada producto
    with open(os.path.join(base_dir, "../Docs/Menu.json"), "r", encoding="utf-8") as file:
        menu = json.load(file)

    for item_name in items:
        for categoria in menu["menu"]:
            for plato in menu["menu"][categoria]:
                if item_name == plato["name"]:
                    cantidad = 1  # Asume cantidad 1 si no está especificada
                    precio = plato["price"]
                    subtotal = cantidad * precio
                    total += subtotal
                    contenido += f"{item_name.ljust(20)} {str(cantidad).rjust(5)} {f'${precio:,.2f}'.rjust(10)} {f'${subtotal:,.2f}'.rjust(10)}\n"

    contenido += f"""
---------------------------------------------------
{"TOTAL:".ljust(36)} {f'${total:,.2f}'.rjust(10)}
===================================================
"""

    # Guardar la comanda en un archivo
    with open(
        os.path.join(base_dir, f"../Docs/Comandas/comanda_sub_mesa_{numero_comanda}.txt"),
        "w",
        encoding="utf-8",
    ) as archivo:
        archivo.write(contenido)


if __name__ == "__main__":
    lista =[
        "Agua mineral",
        "Agua mineral gasificada",
        "Norton clásico 375",
        "Norton clásico 375",
        "Norton clásico 750",
        "Don valentin",
        "Killka 750"
    ]
    mesa = 5
    mozo = "Nahuel Romero"
    comanda_preview(mesa, mozo, lista)
                

    


