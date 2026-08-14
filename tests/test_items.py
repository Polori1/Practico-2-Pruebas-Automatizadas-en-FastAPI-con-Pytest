from fastapi.testclient import TestClient

from app.main import app
from app.database import FAKE_DB


client = TestClient(app)


def test_read_items_empty():
    FAKE_DB.clear()

    response = client.get(
        "/items/?token=nivel-intermedio-2026"
    )

    assert response.status_code == 200
    assert response.json() == []

    FAKE_DB.clear()


def test_create_item_validation_error():
    FAKE_DB.clear()

    payload = {
        "name": "ab",
        "price": -10,
        "sku": "ABC"
    }

    response = client.post(
        "/items/?token=nivel-intermedio-2026",
        json=payload
    )

    assert response.status_code == 422
    assert len(FAKE_DB) == 0


def test_create_item_success():
    FAKE_DB.clear()

    payload = {
        "name": "Teclado Mecánico",
        "price": 85.50,
        "sku": "TECLA"
    }

    response = client.post(
        "/items/?token=nivel-intermedio-2026",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Teclado Mecánico"
    assert response.json()["sku"] == "TECLA"
    assert len(FAKE_DB) == 1

    FAKE_DB.clear()


def test_get_item_not_found():
    FAKE_DB.clear()

    response = client.get(
        "/items/999?token=nivel-intermedio-2026"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Item no encontrado"


def test_create_item_invalid_sku_length():
    FAKE_DB.clear()

    payload = {
        "name": "Mouse Optico",
        "price": 25.0,
        "sku": "ABC"
    }

    response = client.post(
        "/items/?token=nivel-intermedio-2026",
        json=payload
    )

    assert response.status_code == 422
    assert len(FAKE_DB) == 0


def test_workflow_create_and_get_item():
    FAKE_DB.clear()

    payload = {
        "name": "Monitor 24",
        "price": 199.99,
        "sku": "MON24"
    }

    post_response = client.post(
        "/items/?token=nivel-intermedio-2026",
        json=payload
    )

    assert post_response.status_code == 201

    created_id = post_response.json()["id"]

    get_response = client.get(
        f"/items/{created_id}?token=nivel-intermedio-2026"
    )

    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Monitor 24"
    assert get_response.json()["sku"] == "MON24"

    FAKE_DB.clear()