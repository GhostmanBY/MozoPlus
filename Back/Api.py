import sys
import os
import redis
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from fastapi import FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from Back.models import ValorInput
from Back.Login_de_mozo_back import verificar, login_out
from Back.Menu_de_mesas_Back import (
    ver_mesas,
    cantidad_de_mesas,
    editar_mesa,
    abrir_mesa,
    cerrar_mesa,
    crear_comanda,
    crear_sub_mesa,
    editar_sub_mesa,
    cerrar_sub_mesa,
    imprir,
    guardar_mesa
)
from Back.Panel_Admin_Back import obtener_menu_en_json, obtener_cubiertos_json

app = FastAPI()

# Configuración de CORS (Cross-Origin Resource Sharing)
# Permite que el API sea accesible desde cualquier origen, lo que es útil para entornos de desarrollo.
# En producción, puedes restringir los orígenes para mejorar la seguridad.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aquí permitimos todas las URLs, puedes especificar algunas si lo prefieres.
    allow_credentials=True,  # Permite el uso de cookies o credenciales en las solicitudes.
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],  # Permite todos los encabezados (headers) en las solicitudes.
)
import redis

redis_client = redis.Redis(
  host='redis-17127.c280.us-central1-2.gce.redns.redis-cloud.com',
  port=17127,
  password='e6xm6izMHbIjytMSlyoZ35mvapmKr6MV')
# Configuración de Redis
MENU_CACHE_KEY = "menu_cache"
CACHE_EXPIRATION = 36000  # 10 horas en segundos

# Ruta POST para verificar un código de mozo.
# Esta ruta recibe un código y utiliza la función `verificar` para comprobar si el código pertenece a un mozo registrado.
@app.post("/verificar/{code}")
async def ruta_verificar(code: str):
    try:
        # Llama a la función 'verificar' para buscar el código de mozo.
        data = await verificar(code)
        
        # Si no se encuentra el mozo (data == 0), se lanza un error 404.
        if data == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mozo no encontrado.")
        
        # Si todo es correcto, se devuelve la información del mozo.
        return data
    except HTTPException as http_exc:
        # Lanza excepciones HTTP personalizadas si ya están definidas.
        raise http_exc
    except Exception as e:
        # En caso de un error inesperado, se lanza un error 500 con el mensaje del error.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para cerrar sesión (logout) de un mozo.
# Recibe un código de mozo y llama a la función 'login_out'.
@app.post("/salir/{name}")
async def ruta_login_out(name: str):
    try:
        result = await login_out(name)
        
        if isinstance(result, dict) and "message" in result:
            return result
        else:
            return {"message": "Salida exitosa."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta GET para obtener una lista de mesas disponibles.
@app.get("/mesas")
async def ruta_ver_mesas():
    try:
        # Llama a la función 'ver_mesas' para obtener la lista de mesas.
        mesas = await ver_mesas()
        
        # Si no se encuentran mesas, lanza un error 404.
        if not mesas:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron mesas.")
        
        # Devuelve la lista de mesas si todo es correcto.
        return mesas
    except Exception as e:
        # Captura cualquier error inesperado y lanza un error 500.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta GET para obtener la cantidad total de mesas.
@app.get("/mesas/cantidad")
async def ruta_cantidad_mesas():
    try:
        result = cantidad_de_mesas()
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Ruta PUT para editar una mesa o un grupo de mesas enlazadas.
@app.put("/mesas/{mesa}")
async def ruta_editar_mesa(mesa: int, input: ValorInput):
    try:
        result = await guardar_mesa(mesa, input)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mesa {mesa} no encontrada.")
    
        return {"message": "Mesa(s) editada(s) exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para abrir una mesa.
# Recibe el número de mesa y el nombre del mozo.
@app.post("/mesas/{mesa}/{mozo}/abrir")
async def ruta_abrir_mesa(mesa: int, mozo: str):
    try:
        # Llama a la función 'abrir_mesa' con el número de mesa y el nombre del mozo.
        result = await abrir_mesa(mesa, mozo)

        # Si no se encuentra la mesa o el mozo, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa o mozo no encontrado.")
        
        # Devuelve el resultado de la operación si todo es correcto.
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para cerrar una mesa o un grupo de mesas enlazadas.
@app.post("/mesas/{mesa}/cerrar")
async def ruta_cerrar_mesa(mesa: int):
    try:
        await crear_comanda(mesa)
        
    
        result = await cerrar_mesa(mesa)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mesa {mesa} no encontrada.")
    
        return {"message": "Mesa(s) cerrada(s) exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Ruta GET para obtener el menú en formato JSON.
@app.get("/menu")
async def ruta_menu():
    try:
        # Intentar obtener el menú desde Redis
        cached_menu = redis_client.get(MENU_CACHE_KEY)
        if cached_menu:
            return json.loads(cached_menu)
        
        # Si no está en caché, obtenerlo de la base de datos
        menu_data = obtener_menu_en_json()
        
        # Guardar en caché
        redis_client.setex(MENU_CACHE_KEY, CACHE_EXPIRATION, json.dumps(menu_data))
        
        return menu_data
    except redis.RedisError:
        # Si hay un error con Redis, fallback a la base de datos
        return obtener_menu_en_json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/precio")
async def ruta_cubierto():
    precio_cubierto = obtener_cubiertos_json()

    if not precio_cubierto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio no encontrado")
    
    return precio_cubierto


# Ruta POST para crear una sub-mesa.
# Recibe el número de mesa y el ID de la sub-mesa.
@app.post("/mesas/{mesa}/sub_mesa/{sub_mesa_id}")
async def ruta_crear_sub_mesa(mesa: int, sub_mesa_id: str):
    try:
        # Llama a la función 'crear_sub_mesa' con el número de mesa y el ID de la sub-mesa.
        result = await crear_sub_mesa(mesa, sub_mesa_id)
        
        # Si no se encuentra la mesa, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve el resultado de la creación de la sub-mesa si todo es correcto.
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para agregar un producto a una sub-mesa.
# Recibe el número de mesa, el ID de la sub-mesa y el producto.
@app.post("/mesas/{mesa}/sub_mesa/{sub_mesa_id}/editar")
async def ruta_editar_sub_mesa(mesa: int, sub_mesa_id: str, producto: ValorInput):
    try:
        # Llama a la función 'editar_sub_mesa' con el número de mesa, el ID de la sub-mesa y el producto.
        result = await editar_sub_mesa(mesa, sub_mesa_id, producto)
        
        # Si no se encuentra la mesa, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve el resultado de la adición del producto a la sub-mesa si todo es correcto.
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para cerrar una sub-mesa.
# Recibe el número de mesa y el ID de la sub-mesa.
@app.post("/mesas/{mesa}/sub_mesa/{sub_mesa_id}/cerrar")
async def ruta_cerrar_sub_mesa(mesa: int, sub_mesa_id: str):
    try:
        # Llama a la función 'cerrar_sub_mesa' con el número de mesa y el ID de la sub-mesa.
        result = await cerrar_sub_mesa(mesa, sub_mesa_id)
        
        # Si no se encuentra la mesa, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve el resultado de la cierre de la sub-mesa si todo es correcto.
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para abrir un grupo de mesas enlazadas.
@app.post("/mesas/enlazar/{mesas}/{mozo}/abrir")
async def ruta_abrir_mesas_enlazadas(mesas: str, mozo: str):
    try:
        # Convierte la cadena de mesas en una lista de enteros.
        mesas_list = list(map(int, mesas.split(',')))
        
        # Llama a la función 'abrir_mesa' para cada mesa en el grupo.
        for mesa in mesas_list:
            result = await abrir_mesa(mesa, mozo)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mesa {mesa} o mozo no encontrado.")
        
        # Devuelve un mensaje de éxito si todas las mesas se abrieron correctamente.
        return {"message": "Mesas enlazadas abiertas exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta PUT para editar un grupo de mesas enlazadas.
@app.put("/mesas/enlazar/{mesas}")
async def ruta_editar_mesas_enlazadas(mesas: str, input: ValorInput):
    try:
        mesas_list = list(map(int, mesas.split(',')))
        
        for mesa in mesas_list:
            result = await editar_mesa(mesa, input)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mesa {mesa} no encontrada.")
        
        return {"message": "Mesas enlazadas editadas exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta POST para cerrar un grupo de mesas enlazadas.
@app.post("/mesas/enlazar/{mesas}/cerrar")
async def ruta_cerrar_mesas_enlazadas(mesas: str):
    try:
        mesas_list = list(map(int, mesas.split(',')))
        
        # Crea una comanda antes de cerrar las mesas.
        await crear_comanda(mesas_list)
        
        for mesa in mesas_list:
            result = await cerrar_mesa(mesa)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mesa {mesa} no encontrada.")
        
        return {"message": "Mesas enlazadas cerradas exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/precomanda/{num_comanda}")
async def ruta_precomanda(num_comanda: int):
    await imprir(num_comanda)
    return {"message": "Ok."}


# Bloque principal para ejecutar la aplicación con Uvicorn.
# Este código solo se ejecuta si el archivo se ejecuta directamente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
