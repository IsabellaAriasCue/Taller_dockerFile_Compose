from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models import Videojuego
from .schemas import VideojuegoCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"mensaje": "API Venta de Videojuegos"}

@app.post("/videojuegos")
def crear_videojuego(videojuego: VideojuegoCreate):

    db: Session = SessionLocal()

    nuevo = Videojuego(
        nombre=videojuego.nombre,
        genero=videojuego.genero,
        precio=videojuego.precio
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

@app.get("/videojuegos")
def listar_videojuegos():

    db: Session = SessionLocal()

    return db.query(Videojuego).all()

@app.delete("/videojuegos/{id}")
def eliminar_videojuego(id: int):

    db: Session = SessionLocal()

    juego = db.query(Videojuego).filter(
        Videojuego.id == id
    ).first()

    if not juego:
        raise HTTPException(
            status_code=404,
            detail="No encontrado"
        )

    db.delete(juego)
    db.commit()

    return {"mensaje": "Eliminado"}

@app.get("/videojuegos/{id}")
def obtener_videojuego(id: int):

    db: Session = SessionLocal()

    juego = db.query(Videojuego).filter(
        Videojuego.id == id
    ).first()

    if not juego:
        raise HTTPException(
            status_code=404,
            detail="No encontrado"
        )

    return juego

@app.put("/videojuegos/{id}/descuento")
def aplicar_descuento(id: int, porcentaje: float):

    db: Session = SessionLocal()

    juego = db.query(Videojuego).filter(Videojuego.id == id).first()

    if not juego:
        raise HTTPException(status_code=404, detail="No encontrado")

    if porcentaje <= 0 or porcentaje > 100:
        raise HTTPException(status_code=400, detail="Porcentaje inválido")

    juego.precio = juego.precio - (juego.precio * (porcentaje / 100))

    db.commit()
    db.refresh(juego)

    return juego