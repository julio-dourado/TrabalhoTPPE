import httpx
import pytest

@pytest.fixture
def base_url():
    return "http://localhost:8000"

def test_db_connection(base_url):
    client = httpx.Client(base_url=base_url)
    response = client.get("/")
    assert response.status_code == 200
