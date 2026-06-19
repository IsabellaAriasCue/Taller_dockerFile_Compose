import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database import Base
from app.models import Videojuego

@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:15") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_crear_videojuego_persiste_correctamente(db_session):
    nuevo_juego = Videojuego(nombre="Sekiro", genero="Accion", precio=150000)
    db_session.add(nuevo_juego)
    db_session.commit()

    assert nuevo_juego.id is not None

def test_aplicar_descuento_calcula_y_persiste_bien(db_session):

    juego = Videojuego(nombre="Hades", genero="Roguelike", precio=100000)
    db_session.add(juego)
    db_session.commit()

    juego.precio = juego.precio - (juego.precio * (20 / 100))
    db_session.commit()
    db_session.refresh(juego)

    assert juego.precio == 80000.0

def test_obtener_videojuego_retorna_datos_exactos(db_session):
    juego = Videojuego(nombre="Persona 5", genero="JRPG", precio=200000)
    db_session.add(juego)
    db_session.commit()

    busqueda = db_session.query(Videojuego).filter(Videojuego.id == juego.id).first()
    assert busqueda is not None
    assert busqueda.nombre == "Persona 5"

def test_eliminar_videojuego_borrado_fisico(db_session):
    juego = Videojuego(nombre="Doom", genero="Shooter", precio=90000)
    db_session.add(juego)
    db_session.commit()
    juego_id = juego.id

    assert db_session.query(Videojuego).filter(Videojuego.id == juego_id).count() == 1

    db_session.delete(juego)
    db_session.commit()

    assert db_session.query(Videojuego).filter(Videojuego.id == juego_id).count() == 0