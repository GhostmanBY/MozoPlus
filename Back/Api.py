import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import ValorInput
from Back.Login_de_mozo_back import verificar, login_out
from Back.Menu_de_mesas_Back import (
    ver_mesas,
    cantidad_de_mesas,
    guardar_mesa,
    editar_mesa,
    abrir_mesa,
    cerrar_mesa,
    crear_comanda,
    crear_sub_mesa,
    agregar_producto_sub_mesa,
    cerrar_sub_mesa,
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

# Ruta PUT para editar una mesa.
# Recibe el número de la mesa y un JSON con los valores que se van a editar.
@app.put("/mesas/{mesa}")
async def ruta_guardar_mesa(mesa: int, input: ValorInput):
    """
    Ejemplo del JSON enviado en la petición:
    {
      "categoria": "productos",
      "valor": ["vino", "sorrentino"]
    }
    """
    try:
        # Llama a la función 'editar_mesa' con el número de mesa y los nuevos valores.
        result = await guardar_mesa(mesa, input)
        
        # Si la mesa no se encuentra, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Si la petición no es procesable, lanza un error 422 y un print.
        if isinstance(result, dict) and "error" in result:
            print(f"INFO:    {requests.client.host}:{requests.client.port} - {requests.method} {requests.url.path} {result['error']}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Error en la entidad {result['entity']}: {result['error']}"
            )
        
        # Devuelve el resultado de la edición.
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/mesas/{mesa}")
async def ruta_editar_mesa(mesa: int):
    try:
        # Llama a la función 'editar_mesa' con el número de mesa y los nuevos valores.
        result = await editar_mesa(mesa)
        
        # Si la mesa no se encuentra, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
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

# Ruta POST para cerrar una mesa.
# Primero crea una comanda y luego cierra la mesa.
@app.post("/mesas/{mesa}/cerrar")
async def ruta_cerrar_mesa(mesa: int):
    try:
        # Crea una comanda antes de cerrar la mesa.
        await crear_comanda(mesa)
        
        # Cierra la mesa usando la función 'cerrar_mesa'.
        result = await cerrar_mesa(mesa)
        
        # Si no se encuentra la mesa, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve un mensaje de éxito si la mesa se cerró correctamente.
        return {"message": "Mesa cerrada exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Ruta GET para obtener el menú en formato JSON.
@app.get("/menu")
async def ruta_menu():
    # Llama a la función 'obtener_menu_en_json' para obtener el menú.
        menu = obtener_menu_en_json()
        
        # Si no se encuentra el menú, lanza un error 404.
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menú no encontrado.")
        
        print(menu)
        # Devuelve el menú en formato JSON si todo es correcto.
        return menu

@app.get("/precio")
async def ruta_cubierto():
    precio_cubierto = obtener_cubiertos_json()

    if not precio_cubierto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio no encontrado")
    
    return precio_cubierto

# Ruta POST para crear una sub-mesa.
# Recibe el número de mesa y el ID de la sub-mesa.
@app.post("/mesas/{mesa}/sub_mesa")
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
@app.post("/mesas/{mesa}/sub_mesa/{sub_mesa_id}/producto")
async def ruta_agregar_producto_sub_mesa(mesa: int, sub_mesa_id: str, producto: ValorInput):
    try:
        # Llama a la función 'agregar_producto_sub_mesa' con el número de mesa, el ID de la sub-mesa y el producto.
        result = await agregar_producto_sub_mesa(mesa, sub_mesa_id, producto)
        
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

# Bloque principal para ejecutar la aplicación con Uvicorn.
# Este código solo se ejecuta si el archivo se ejecuta directamente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
