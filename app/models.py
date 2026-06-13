from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Videojuego(Base):
    __tablename__ = "videojuegos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    precio = Column(Float, nullable=False)