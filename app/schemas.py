from pydantic import BaseModel

class VideojuegoCreate(BaseModel):
    nombre: str
    genero: str
    precio: float

class VideojuegoResponse(VideojuegoCreate):
    id: int

    class Config:
        from_attributes = True