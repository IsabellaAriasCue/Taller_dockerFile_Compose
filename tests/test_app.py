from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():

    response = client.get("/")

    assert response.status_code == 200

def test_crear_videojuego():

    response = client.post(
        "/videojuegos",
        json={
            "nombre": "FIFA 25",
            "genero": "Deportes",
            "precio": 200000
        }
    )

    assert response.status_code == 200

def test_listar_videojuegos():

    response = client.get("/videojuegos")

    assert response.status_code == 200

def test_buscar_videojuego():

    crear = client.post(
        "/videojuegos",
        json={
            "nombre": "GTA V",
            "genero": "Accion",
            "precio": 180000
        }
    )

    juego_id = crear.json()["id"]

    response = client.get(
        f"/videojuegos/{juego_id}"
    )

    assert response.status_code == 200

def test_aplicar_descuento():

    crear = client.post("/videojuegos", json={
        "nombre": "Elden Ring",
        "genero": "RPG",
        "precio": 100000
    })

    juego_id = crear.json()["id"]

    response = client.put(
        f"/videojuegos/{juego_id}/descuento",
        params={"porcentaje": 10}
    )

    assert response.status_code == 200
    assert response.json()["precio"] == 90000