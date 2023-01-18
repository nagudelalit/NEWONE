from fastapi.testclient import TestClient
from .main import app, HTMLResponse
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_handleform(client):
    response = client.get("/questions")
    assert response.status_code == 200


def test_read_user(client):
    data = {"username": "testuser"}
    response = client.post("/submit", json=data)
    assert response.status_code == 200
    assert response.json() == {"error": 0,
                               "message": "Registered Successfully"}


def test_getuserdetails(client):
    headers = {"Cookie": "X-Authorization=testuser"}
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"details": "testuser"}


"""def test_handleform(client):
    response = client.get("/questions")
    assert response.status_code == 200
    assert isinstance(response, HTMLResponse)
    assert response.html == templates.TemplateResponse("question.html", {"request": request})

def test_handleform(client):
    response = client.get("/questions")
    assert response.status_code == 200
    assert isinstance(response, HTMLResponse)
    assert response.html == templates.TemplateResponse("question.html", {"request": request})


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response, HTMLResponse)
    assert response.html == templates.TemplateResponse("register.html", {"request": request})


def test_handleform(client):
    # Send a GET request to the endpoint
    response = client.get("/questions")
    
    # Make assertions about the response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html"
    assert b"question.html" in response.content

def test_read_user(client):
    user = {"username": "testuser", "password": "testpass"}
    response = client.post("/submit", json=user)
    assert response.status_code == 200
    assert response.json() == {"error": 0,
                               "message": "Registered Successfully"}
    assert "X-Authorization" in response.cookies
    assert response.cookies["X-Authorization"] == "testuser" 
    
    
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response, HTMLResponse)
    assert response.html == templates.TemplateResponse("register.html", {"request": request})"""

"""def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_handleform():
    response = client.get("/questions")
    assert response.status_code == 200"""
