from fastapi.testclient import TestClient

from app.main import app
from app.database import db_usuarios, db_productos, FAKE_DB


client = TestClient(app)


# EJERCICIO 1 - USUARIOS

def test_registro_usuario_exitoso():
    db_usuarios.clear()

    response = client.post(
        "/usuarios/",
        json={
            "username": "usuario1",
            "edad": 20
        }
    )

    assert response.status_code == 201
    assert response.json()["username"] == "usuario1"

    db_usuarios.clear()


def test_registro_usuario_edad_invalida():
    db_usuarios.clear()

    response = client.post(
        "/usuarios/",
        json={
            "username": "usuario2",
            "edad": 17
        }
    )

    assert response.status_code == 422
    assert len(db_usuarios) == 0


def test_registro_usuario_duplicado():
    db_usuarios.clear()

    usuario = {
        "username": "usuario3",
        "edad": 25
    }

    primera_respuesta = client.post(
        "/usuarios/",
        json=usuario
    )

    assert primera_respuesta.status_code == 201

    segunda_respuesta = client.post(
        "/usuarios/",
        json=usuario
    )

    assert segunda_respuesta.status_code == 400

    db_usuarios.clear()


def test_busqueda_usuario_existente():
    db_usuarios.clear()

    client.post(
        "/usuarios/",
        json={
            "username": "usuario4",
            "edad": 30
        }
    )

    response = client.get("/usuarios/1")

    assert response.status_code == 200
    assert response.json()["username"] == "usuario4"
    assert response.json()["search"] == "general"

    db_usuarios.clear()


def test_busqueda_usuario_inexistente():
    db_usuarios.clear()

    response = client.get("/usuarios/999")

    assert response.status_code == 404

    db_usuarios.clear()


def test_user_id_invalido():
    db_usuarios.clear()

    response = client.get("/usuarios/0")

    assert response.status_code == 422


# EJERCICIO 2 - SEGURIDAD / TOKEN

def test_crear_item_token_correcto():
    FAKE_DB.clear()

    response = client.post(
        "/items/?token=nivel-intermedio-2026",
        json={
            "name": "Teclado",
            "price": 85.50,
            "sku": "TECLA"
        }
    )

    assert response.status_code == 201

    FAKE_DB.clear()


def test_crear_item_token_incorrecto():
    FAKE_DB.clear()

    response = client.post(
        "/items/?token=token-incorrecto",
        json={
            "name": "Teclado",
            "price": 85.50,
            "sku": "TECLA"
        }
    )

    assert response.status_code == 401


def test_crear_item_sin_token():
    FAKE_DB.clear()

    response = client.post(
        "/items/",
        json={
            "name": "Teclado",
            "price": 85.50,
            "sku": "TECLA"
        }
    )

    assert response.status_code == 401


def test_listar_items_sin_token():
    FAKE_DB.clear()

    response = client.get("/items/")

    assert response.status_code == 401

def test_listar_productos_sin_token():
    db_productos.clear()

    response = client.get("/productos/")

    assert response.status_code == 401


def test_listar_productos_con_token():
    db_productos.clear()

    response = client.get(
        "/productos/?token=nivel-intermedio-2026"
    )

    assert response.status_code == 200
    assert response.json() == []

    db_productos.clear()