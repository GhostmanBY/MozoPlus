import os
import datetime
import json

# Leemos el archivo de la mesa
mesa = 1

archivo = f"tmp/Mesa {mesa}.json"

with open(archivo, "r", encoding="utf-8") as file:
    contenido = file.read()

# Convertimos el contenido a un diccionario
data = json.loads(contenido)

nombre_mozo = "Nahuel"

# Captura de la hora de cierre de la mesa y el dia
fecha_hoy = datetime.datetime.now().date()
fecha_txt = datetime.datetime.now()
fecha = fecha_txt.strftime("%H:%M")

# Añade la hora al json
data.update({"Hora": fecha})

cantidad = 0
Comanda_orden = {}

if os.path.exists(f"Docs/{fecha_hoy}_{nombre_mozo}.json"):
    with open(archivo, "r", encoding="utf-8") as file:
        Cantidad_comandas = file.read()
    if Cantidad_comandas == None:
        Comanda_orden["Comanda_1"] = {
            data
        }
    else:
        for i in Cantidad_comandas:
            cantidad += 1
            print(cantidad)
        Comanda_orden[f"Comanda_{cantidad}"] = {
            data
        }
    print(Comanda_orden)