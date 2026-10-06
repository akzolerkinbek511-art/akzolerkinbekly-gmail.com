"""
ОН 7.2 — 45-тапсырма: API тестілеу (pytest + httpx)
FoodExpress API коллекциясы симуляциясы
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Минималды FastAPI stub (нақты API орнына)
app = FastAPI()

ORDERS = {}
USERS = {"+77001234567": {"id": 1, "name": "Test User"}}


@app.post("/auth/login")
def login(phone: str, otp: str):
    if phone in USERS and otp == "123456":
        return {"access_token": "fake-jwt", "refresh_token": "fake-refresh"}
    raise HTTPException(401, "Invalid OTP")


@app.get("/restaurants")
def restaurants(page: int = 1):
    return {"items": [{"id": 1, "name": "Test Rest", "rating": 4.5}], "total": 1}


@app.post("/orders", status_code=201)
def create_order(payload: dict):
    oid = len(ORDERS) + 1
    ORDERS[oid] = {"id": oid, "status": "new", **payload}
    return ORDERS[oid]


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in ORDERS:
        raise HTTPException(404, "Not found")
    return ORDERS[order_id]


@app.post("/orders/{order_id}/pay")
def pay(order_id: int, method: str = "kaspi"):
    if order_id not in ORDERS:
        raise HTTPException(404, "Not found")
    ORDERS[order_id]["status"] = "paid"
    return {"status": "success", "transaction_id": f"tx_{order_id}"}


# ---------- Тесттер ----------
@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_login_success(client):
    r = await client.post("/auth/login", params={"phone": "+77001234567", "otp": "123456"})
    assert r.status_code == 200
    assert "access_token" in r.json()


@pytest.mark.asyncio
async def test_login_fail(client):
    r = await client.post("/auth/login", params={"phone": "+77001234567", "otp": "000000"})
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_list_restaurants(client):
    r = await client.get("/restaurants")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_create_order(client):
    payload = {"restaurant_id": 1, "address_id": 1, "items": [{"dish_id": 10, "quantity": 2}]}
    r = await client.post("/orders", json=payload)
    assert r.status_code == 201
    assert r.json()["status"] == "new"


@pytest.mark.asyncio
async def test_get_order(client):
    payload = {"restaurant_id": 1, "address_id": 1, "items": [{"dish_id": 10, "quantity": 1}]}
    create = await client.post("/orders", json=payload)
    oid = create.json()["id"]
    r = await client.get(f"/orders/{oid}")
    assert r.status_code == 200
    assert r.json()["id"] == oid


@pytest.mark.asyncio
async def test_get_order_404(client):
    r = await client.get("/orders/99999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_pay_order(client):
    payload = {"restaurant_id": 1, "address_id": 1, "items": [{"dish_id": 10, "quantity": 1}]}
    create = await client.post("/orders", json=payload)
    oid = create.json()["id"]
    r = await client.post(f"/orders/{oid}/pay", params={"method": "kaspi"})
    assert r.status_code == 200
    assert r.json()["status"] == "success"


@pytest.mark.asyncio
async def test_pay_not_found(client):
    r = await client.post("/orders/99999/pay", params={"method": "kaspi"})
    assert r.status_code == 404


# Іске қосу: pytest test_api.py -v
# Postman коллекциясы: жоғарыдағы 5 эндпоинтті import ету жасауға болады
