import httpx
import pytest

BASE_URL = "http://localhost:8001"


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c

def test_flujo_negocio_completo_con_iva(client):
    res_crear = client.post("/videojuegos", json={
        "nombre": "Hollow Knight",
        "genero": "Metroidvania",
        "precio": 100000
    })
    assert res_crear.status_code == 200
    juego_id = res_crear.json()["id"]

    res_desc = client.put(f"/videojuegos/{juego_id}/descuento", params={"porcentaje": 10})
    assert res_desc.status_code == 200

    res_consulta = client.get(f"/videojuegos/{juego_id}")
    assert res_consulta.status_code == 200
    precio_final = res_consulta.json()["precio"]

    assert precio_final == 90000.0

    iva = precio_final * 0.19
    total_con_iva = precio_final + iva
    assert total_con_iva == 107100.0

def test_aislamiento_sesiones_no_se_mezclan(client):
    res1 = client.post("/videojuegos", json={"nombre": "Dark Souls", "genero": "RPG", "precio": 150000})
    res2 = client.post("/videojuegos", json={"nombre": "Celeste", "genero": "Plataformas", "precio": 40000})

    id1 = res1.json()["id"]
    id2 = res2.json()["id"]

    client.put(f"/videojuegos/{id1}/descuento", params={"porcentaje": 50})

    consulta_2 = client.get(f"/videojuegos/{id2}")
    assert consulta_2.json()["precio"] == 40000.0


def test_flujo_error_sistema_resiliente(client):
    res = client.put("/videojuegos/999999/descuento", params={"porcentaje": 15})

    assert res.status_code == 404
    assert res.json()["detail"] == "No encontrado"