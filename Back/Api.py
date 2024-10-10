from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import ValorInput
from Login_de_mozo_back import verificar, login_out
from Menu_de_mesas_Back import (
    ver_mesas,
    cantidad_de_mesas,
    editar_mesa,
    abrir_mesa,
    cerrar_mesa,
    crear_comanda,
    restaurar_mesa,
)
from Panel_Admin_Back import obtener_menu_en_json

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
@app.post("/salir/{code}")
async def ruta_login_out(code: str):
    try:
        # Llama a la función 'login_out' con el código del mozo.
        result = await login_out(code)
        
        # Si no se encuentra el mozo, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Código de mozo no válido.")
        elif "No se a cargado el sistem de login" in result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mozo no logueado.")
        # Si la salida es exitosa, se devuelve un mensaje de éxito.
        return {"message": "Salida exitosa."}
    except HTTPException as http_exc:
        raise http_exc
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
        # Llama a la función 'cantidad_de_mesas' y devuelve el resultado.
        return cantidad_de_mesas()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta PUT para editar una mesa.
# Recibe el número de la mesa y un JSON con los valores que se van a editar.
@app.put("/mesas/{mesa}")
async def ruta_editar_mesa(mesa: int, input: ValorInput):
    """
    Ejemplo del JSON enviado en la petición:
    {
      "categoria": "productos",
      "valor": ["vino", "sorrentino"]
    }
    """
    try:
        # Llama a la función 'editar_mesa' con el número de mesa y los nuevos valores.
        result = await editar_mesa(mesa, input)
        
        # Si la mesa no se encuentra, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve el resultado de la edición.
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

# Ruta POST para resetear una mesa a su estado inicial.
@app.post("/mesas/{mesa}/reset")
async def ruta_reset(mesa: int):
    try:
        # Llama a la función 'restaurar_mesa' para resetear la mesa.
        result = await restaurar_mesa(mesa)
        
        # Si no se encuentra la mesa, lanza un error 404.
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada.")
        
        # Devuelve un mensaje de éxito si la mesa fue reseteada correctamente.
        return {"message": "Mesa reseteada exitosamente."}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Ruta GET para obtener el menú en formato JSON.
@app.get("/menu")
async def ruta_menu():
    try:
        # Llama a la función 'obtener_menu_en_json' para obtener el menú.
        menu = obtener_menu_en_json()
        
        # Si no se encuentra el menú, lanza un error 404.
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menú no encontrado.")
        
        # Devuelve el menú en formato JSON si todo es correcto.
        return menu
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Bloque principal para ejecutar la aplicación con Uvicorn.
# Este código solo se ejecuta si el archivo se ejecuta directamente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
