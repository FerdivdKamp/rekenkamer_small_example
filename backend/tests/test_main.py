from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_begroeting():
    response = client.get("/v1/begroetingen/Ada")

    assert response.status_code == 200
    assert response.json() == {"boodschap": "Hello Ada!"}
    assert response.headers["API-Version"] == "1.0.0"


def test_openapi_is_public_and_versioned():
    response = client.get("/v1/openapi.json", headers={"Origin": "https://example.com"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["API-Version"] == "1.0.0"
    specification = response.json()
    assert specification["info"]["version"] == "1.0.0"
    assert specification["info"]["contact"]["name"] == "Ferdi van de Kamp"
    assert specification["servers"] == [
        {"url": "/v1"},
        {"url": "http://localhost:8000/v1", "description": "Lokale ontwikkelomgeving"},
    ]
    assert "/begroetingen/{naam}" in specification["paths"]


def test_unknown_begroeting_returns_problem_details():
    response = client.get("/v1/onbekend")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert response.headers["API-Version"] == "1.0.0"
    assert response.json()["status"] == 404


def test_empty_name_returns_problem_details():
    response = client.get("/v1/begroetingen/%20")

    assert response.status_code == 400
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["detail"] == "Naam mag niet leeg zijn."
