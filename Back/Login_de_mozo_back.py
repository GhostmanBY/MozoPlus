import sqlite3
import os
import json
import datetime
import redis

base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_db = os.path.join(base_dir, "../DB/Panel_admin.db")

# Configuración de Redis
redis_client = redis.Redis(
    host='redis-17127.c280.us-central1-2.gce.redns.redis-cloud.com',
    port=17127,
    password='e6xm6izMHbIjytMSlyoZ35mvapmKr6MV'
)

MOZO_CACHE_PREFIX = "mozo:"
MOZO_CACHE_EXPIRATION = 36000  # 10 horas en segundos

async def verificar(code: str):
    # Intentar obtener del cache primero
    cache_key = f"{MOZO_CACHE_PREFIX}{code}"
    cached_mozo = redis_client.get(cache_key)
    
    if cached_mozo:
        nombre_mozo = cached_mozo.decode('utf-8')
    else:
        # Se conecta a la base de datos y crea el cursor
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()

        instruccion = "SELECT * FROM Usuario WHERE codigo = ?"
        cursor.execute(instruccion, (code,))

        fila = cursor.fetchone()
        conn.close()

        if not fila:
            return None

        nombre_mozo = fila[1]
        # Guardar en cache
        redis_client.setex(cache_key, MOZO_CACHE_EXPIRATION, nombre_mozo)

    # Bloque para la fecha y hora
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")

    ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")

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

    # Guardar el registro actualizado
    os.makedirs(os.path.dirname(ruta_registro), exist_ok=True)
    with open(ruta_registro, "w", encoding="utf-8") as file:
        json.dump(registro, file, indent=4, ensure_ascii=False)

    # Guardar estado activo en Redis
    redis_client.setex(f"{MOZO_CACHE_PREFIX}active:{nombre_mozo}", MOZO_CACHE_EXPIRATION, "1")
    
    data = {
        "verificado": 1,
        "ID": fila[0],
        "Nombre": nombre_mozo
    }
    return data  # Code encontrado y procesado
    return 0  # Code no encontrado

async def login_out(name: str):
    fecha_hoy = datetime.datetime.now().date()
    fecha_txt = datetime.datetime.now()
    fecha = fecha_txt.strftime("%H:%M")

    ruta_registro = os.path.join(base_dir, f"../Docs/Registro/registro_mozos_{fecha_hoy}.json")

    if not os.path.exists(ruta_registro):
        return False

    with open(ruta_registro, "r", encoding="utf-8") as file:
        try:
            registro = json.load(file)
        except json.JSONDecodeError:
            return False

    mozo_encontrado = False
    for item in registro:
        if name in item:
            mozo_encontrado = True
            item[name]["Horario_salida"] = fecha
            # Limpiar el cache de Redis
            redis_client.delete(f"{MOZO_CACHE_PREFIX}active:{name}")
            break

    if not mozo_encontrado:
        return False

    with open(ruta_registro, "w", encoding="utf-8") as file:
        json.dump(registro, file, indent=4, ensure_ascii=False)

    ruta_mesas = os.path.join(base_dir, f"../Docs/Registro/{fecha_hoy}_{name}.json")

    if os.path.exists(ruta_mesas):
        with open(ruta_mesas, "r", encoding="utf-8") as file:
            mesas = json.load(file)
    else:
        mesas = []

    for item in registro:
        if name in item:
            item[name]['Mesas totales'] = len(mesas)
            break

    with open(ruta_registro, "w", encoding="utf-8") as file:
        json.dump(registro, file, indent=4, ensure_ascii=False)

    return True

if __name__ == "__main__":
    #verificar("admin")
    login_out("Juan Pérez")
