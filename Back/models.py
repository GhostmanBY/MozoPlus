from pydantic import BaseModel

class Mesa(BaseModel):
    disponible: bool
    productos: list
    cantidad_comensales: int
    comensales_infantiles: list


class ValorInput(BaseModel):
    categoria: str
    valor: list[str]

