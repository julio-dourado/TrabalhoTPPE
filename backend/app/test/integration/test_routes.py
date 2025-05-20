# backend/app/test/integration/test_routes.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.db import SessionLocal
from app.models.user import User

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    db = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

@pytest.mark.parametrize("user_data, expected_status_code", [
    ({"nome": "John Doe",  "email": "johndoe@example.com", "senha": "securepwd"}, 201),
    #({"nome": "John Doe",  "email": "short@example.com", "senha": "12345"}, 422),
    #({"nome": "Jane Doe",  "email": "johndoe@example.com", "senha": "securepwd"}, 400),
])
def test_create_user_integration(user_data, expected_status_code):
    response = client.post("/user/", json=user_data)
    assert response.status_code == expected_status_code
    if expected_status_code == 201:
        body = response.json()
        assert body["nome"]  == user_data["nome"]
        assert body["email"] == user_data["email"]

