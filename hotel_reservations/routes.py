from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HotelReservation(BaseModel):
    id: int
    client_id: int
    room_id: int
    check_in_date: str
    check_out_date: str

reservations = []

@router.post("/")
def create_hotel_reservation(reservation: HotelReservation):
    if reservation.client_id not in [client.id for client in clients] or reservation.room_id not in [room.id for room in hotel_rooms]:
        raise HTTPException(status_code=404, detail="Client or hotel room not found")
    reservations.append(reservation)
    return reservation

@router.get("/{reservation_id}")
def get_hotel_reservation(reservation_id: int):
    for reservation in reservations:
        if reservation.id == reservation_id:
            return reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

@router.put("/{reservation_id}")
def update_hotel_reservation(reservation_id: int, reservation: HotelReservation):
    for i, r in enumerate(reservations):
        if r.id == reservation_id:
            reservations[i] = reservation
            return reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

@router.delete("/{reservation_id}")
def delete_hotel_reservation(reservation_id: int):
    for i, reservation in enumerate(reservations):
        if reservation.id == reservation_id:
            del reservations[i]
            return {"message": "Reservation deleted"}
    raise HTTPException(status_code=404, detail="Reservation not found")
