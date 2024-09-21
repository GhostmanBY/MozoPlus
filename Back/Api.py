from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Mesa, ValorInput
from Login_de_mozo_back import verificar, login_out
from Menu_de_mesas_Back import (
    ver_mesas,
    cantidad_de_mesas,
    editar_mesa,
    abrir_mesa,
    cerrar_mesa,
    crear_comanda,
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O puedes restringirlo a una URL específica
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)


@app.post("/verificar/{code}")
async def ruta_verificar(code: str):
    return await verificar(
        code
    )  # Asegúrate de usar 'await' si 'verificar' es asincrónica


@app.post("/salir/{code}")
async def ruta_login_out(code: str):
    return await login_out(code)


@app.get("/mesas")
async def ruta_ver_mesas():
    return await ver_mesas()


@app.get("/mesas/cantidad")
async def ruta_cantidad_mesas():
    return await cantidad_de_mesas()


@app.put("/mesas/{mesa}")
async def ruta_editar_mesa(mesa: int, input: ValorInput):
    """
    ejemplo de el json enviado en la peticion
    {
      "categoria":"productos",
      "valor": ["vino", "sorrentino"]
    }
    """
    return await editar_mesa(mesa, input)


@app.post("/mesas/{mesa}/{mozo}/abrir")
async def ruta_abrir_mesa(mesa: int, mozo: str):
    return await abrir_mesa(mesa, mozo)


@app.post("/mesas/{mesa}/cerrar")
async def ruta_cerrar_mesa(mesa: int):
    await crear_comanda(mesa)
    return await cerrar_mesa(mesa)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
