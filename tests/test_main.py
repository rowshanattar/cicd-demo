import pytest
from fastapi.testclient import TestClient

from app.main import _items, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_items():
    """Reset the in-memory store between tests so they don't bleed into each other."""
    _items.clear()
    yield
    _items.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_create_item():
    response = client.post("/items", json={"name": "widget", "description": "a widget"})
    assert response.status_code == 201
    assert response.json() == {"name": "widget", "description": "a widget"}


def test_create_item_appears_in_list():
    client.post("/items", json={"name": "widget"})
    response = client.get("/items")
    assert len(response.json()["items"]) == 1


def test_get_item_found():
    client.post("/items", json={"name": "widget", "description": "a widget"})
    response = client.get("/items/widget")
    assert response.status_code == 200
    assert response.json() == {"name": "widget", "description": "a widget"}


def test_get_item_not_found_returns_404():
    response = client.get("/items/nonexistent")
    assert response.status_code == 404


def test_create_duplicate_item_returns_409():
    client.post("/items", json={"name": "widget"})
    response = client.post("/items", json={"name": "widget"})
    assert response.status_code == 409
