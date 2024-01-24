import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is created in a file named main.py
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_create_client_success():
    # Mocking user authentication and Firebase database call
    with patch('authentification.auth.get_current_user') as mock_auth, \
         patch('database.firebase.db.child') as mock_db:
        mock_auth.return_value = MagicMock(id=123)  # Mock authenticated user
        mock_db.return_value.child.return_value.set.return_value = None
        client_data = {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
        response = client.post("/clients", json=client_data)
        assert response.status_code == 200
        assert response.json() == client_data

def test_create_client_invalid_data():
    # Mocking user authentication
    with patch('database.firebase.db.child'):
        response = client.post("/clients", json={"id": "invalid", "name": 123, "email": "not-an-email"})
        assert response.status_code == 422  # Unprocessable Entity

def test_create_client_unauthenticated():
    # Simulating unauthenticated access
    with patch('authentification.auth.get_current_user', return_value=None):
        response = client.post("/clients", json={"id": 1, "name": "John Doe", "email": "johndoe@example.com"})
        assert response.status_code == 401  # Unauthorized or similar depending on your authentication setup
