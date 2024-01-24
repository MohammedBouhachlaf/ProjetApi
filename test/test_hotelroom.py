import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is created in a file named main.py
from unittest.mock import patch

client = TestClient(app)

def test_create_hotel_room_success():
    # Mocking Firebase database call
    with patch('database.firebase.db.child') as mock_db:
        mock_db.return_value.child.return_value.set.return_value = None
        response = client.post("/hotel-rooms", json={"id": 0, "room_number": 0, "capacity": 0})
        assert response.status_code == 200
        assert response.json() == {"id": 0, "room_number": 0, "capacity": 0}

#def test_get_hotel_room_success():
    # Mocking Firebase database call
    #with patch('database.firebase.db.child') as mock_db:
        #mock_db.return_value.child.return_value.get.return_value = {"id": 0, "room_number": 0, "capacity": 0}
        #response = client.get("/hotel-rooms/0")
        #assert response.status_code == 200
        #assert response.json() == {"id": 0, "room_number": 0, "capacity": 0}
def test_get_hotel_room_success():
    # Mocking Firebase database call
    with patch('database.firebase.db.child') as mock_db:
        mock_db.return_value.child.return_value.get.return_value.val.return_value = {"id": 0, "room_number": 0, "capacity": 0}
        response = client.get("hotel-rooms/0")
        assert response.status_code == 200
        assert response.json() == {"id": 0, "room_number": 0, "capacity": 0}


def test_create_hotel_room_invalid_data():
    response = client.post("/hotel-rooms", json={"id": "invalid", "room_number": "101", "capacity": "2"})
    assert response.status_code == 422  # Unprocessable Entity

def test_get_hotel_room_non_existing():
    # Mocking Firebase database call
    with patch('database.firebase.db.child') as mock_db:
        mock_db.return_value.child.return_value.get.return_value = None
        response = client.get("/999")
        assert response.status_code == 404  # Not Found
