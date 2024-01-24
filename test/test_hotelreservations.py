import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is created in a file named main.py
from unittest.mock import patch

client = TestClient(app)



def test_create_hotel_reservation_success():
    # Mocking Firebase database call and other external dependencies
    with patch('database.firebase.db.child') as mock_db:
        mock_db.return_value.child.return_value.set.return_value = None
        reservation_data = {
            "id": 1,
            "client_id": 100,
            "room_id": 200,
            "check_in_date": "2024-01-01",
            "check_out_date": "2024-01-05"
        }
        response = client.post("/hotel-reservations", json=reservation_data)
        assert response.status_code == 200
        assert response.json() == reservation_data

def test_create_hotel_reservation_invalid_data():
    response = client.post("/hotel-reservations", json={"id": "invalid", "client_id": "invalid", "room_id": "invalid", "check_in_date": "invalid", "check_out_date": "invalid"})
    assert response.status_code == 422  # Unprocessable Entity

# Additional tests can be added for handling exceptions like non-existing client or room.
