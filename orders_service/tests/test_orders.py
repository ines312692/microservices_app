import pytest
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

from orders_service.main import app
from orders_service.models import Orders


@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="module", autouse=True)
def initialize_db():
    # Initialise une base en mémoire SQLite pour tests
    initializer(['models'], db_url="sqlite://:memory:")
    yield
    finalizer()


@pytest.mark.anyio
async def test_create_order():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/orders",
            json={
                "address": "123 Test St",
                "item": "Product A"
            },
            headers={"request_user_id": "1"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "123 Test St"
    assert data["item"] == "Product A"
    assert "id" in data


@pytest.mark.anyio
async def test_get_orders():
    # Crée d'abord une commande en base
    order = await Orders.create(address="456 Other St", item="Product B", created_by=1)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/orders", headers={"request_user_id": "1"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(o["address"] == "456 Other St" for o in data)
