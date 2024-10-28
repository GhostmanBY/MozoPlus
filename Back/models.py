from pydantic import BaseModel

class Mesa(BaseModel):
    disponible: bool
    productos: list
    cantidad_comensales: int
    comensales_infantiles: list
    Extra: str


class ValorInput(BaseModel):
    categoria: str
    valor: list[str] | str | int

