from fastapi import FastAPI
from Login_de_mozo_back import verificar
from Menu_de_mesas_Back import *

app = FastAPI()

@app.post("/verificar/{code}")
async def ruta_verificar(code: str):
    return await verificar(code)  # Asegúrate de usar 'await' si 'verificar' es asincrónica

@app.get("/mesas")
async def ruta_ver_mesas():
    return await ver_mesas()

@app.get("/mesas/cantidad")
async def ruta_cantidad_mesas():
    return await cantidad_de_mesas()

@app.put("/mesas/{mesa}")
async def ruta_editar_mesa(mesa: int, input: dict):
    return await editar_mesa(mesa, input)

@app.post("/mesas/{mesa}/{mozo}/abrir")
async def ruta_abrir_mesa(mesa: int, mozo: str):
    return await abrir_mesa(mesa, mozo)

@app.post("/mesas/{mesa}/cerrar")
async def ruta_cerrar_mesa(mesa: int):
    return await cerrar_mesa(mesa)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)