import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_seller():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Владимир",
            "last_name": "Смирнов",
            "e_mail": "smirnovve2003@gmail.com",
            "password": "1972"
        }
        response = await ac.post("/api/v1/seller/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["first_name"] == payload["first_name"]
        assert "password" not in data

@pytest.mark.asyncio
async def test_get_all_sellers():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/seller/")
        assert response.status_code == 200
        sellers = response.json()
        assert isinstance(sellers, list)
        if sellers:
            assert "password" not in sellers[0]  

@pytest.mark.asyncio
async def test_get_seller():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Иван",
            "last_name": "Самарин",
            "e_mail": "samarin2003@gmail.com",
            "password": "secret"
        }
        create_resp = await ac.post("/api/v1/seller/", json=payload)
        seller_id = create_resp.json()["id"]
        
        # 
        response = await ac.get(f"/api/v1/seller/{seller_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == seller_id
        assert "books" in data 
        assert "password" not in data  

@pytest.mark.asyncio
async def test_update_seller():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Аль",
            "last_name": "Пачино",
            "e_mail": "pacinogodfather1972@gmail.com",
            "password": "kopolla"
        }
        create_resp = await ac.post("/api/v1/seller/", json=payload)
        seller_id = create_resp.json()["id"]
        
        update_payload = {
            "first_name": "СергейUpdated",
            "last_name": "СергеевUpdated",
            "e_mail": "sergeev_updated@check.com",
            "password": "secret" 
        }
        response = await ac.put(f"/api/v1/seller/{seller_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "СергейUpdated"
        assert data["last_name"] == "СергеевUpdated"
        assert data["e_mail"] == "sergeev_updated@check.com"
        assert "password" not in data 

@pytest.mark.asyncio
async def test_delete_seller():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Алексей",
            "last_name": "Алексеев",
            "e_mail": "alekseev@check.com",
            "password": "secret"
        }
        create_resp = await ac.post("/api/v1/seller/", json=payload)
        seller_id = create_resp.json()["id"]
        
        # Удаление продавца
        del_resp = await ac.delete(f"/api/v1/seller/{seller_id}")
        assert del_resp.status_code == 204

        # Проверка, что продавец был удален
        get_resp = await ac.get(f"/api/v1/seller/{seller_id}")
        assert get_resp.status_code == 404  

@pytest.mark.asyncio
async def test_create_seller_with_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Некорректные данные 
        payload = {
            "first_name": "",
            "last_name": "",
            "e_mail": "invalid-email",
            "password": ""
        }
        response = await ac.post("/api/v1/seller/", json=payload)
        assert response.status_code == 422 
        data = response.json()
        assert "detail" in data

@pytest.mark.asyncio
async def test_update_seller_with_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "e_mail": "ivanov@example.com",
            "password": "password"
        }
        create_resp = await ac.post("/api/v1/seller/", json=payload)
        seller_id = create_resp.json()["id"]

        # Некорректные данные для обновления
        update_payload = {
            "first_name": "",
            "last_name": "",
            "e_mail": "invalid-email",
            "password": "secret"
        }
        response = await ac.put(f"/api/v1/seller/{seller_id}", json=update_payload)
        assert response.status_code == 422 
        data = response.json()
        assert "detail" in data
