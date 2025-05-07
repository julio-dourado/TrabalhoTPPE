import httpx

def test_db_connection(base_url='http://localhost:8000'):  
    client = httpx.Client(base_url=base_url)
    response = client.get("/")
    assert response.status_code == 200
