from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database.firebase import db

router = APIRouter()

class HotelReservation(BaseModel):
    id: int
    client_id: int
    room_id: int
    check_in_date: str
    check_out_date: str

@router.post("/", response_model=HotelReservation)
def create_hotel_reservation(reservation: HotelReservation):
    # Ici, vérifiez l'existence du client et de la chambre dans la DB (omis pour la brièveté)
    
    # Ajoutez la réservation à Firebase
    reservation_data = reservation.dict()
    db.child("reservations").child(reservation.id).set(reservation_data)
    return reservation_data

@router.get("/{reservation_id}", response_model=HotelReservation)
def get_hotel_reservation(reservation_id: int):
    reservation_data = db.child("reservations").child(reservation_id).get()
    if reservation_data.val() is not None:
        return reservation_data.val()
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")

@router.put("/{reservation_id}", response_model=HotelReservation)
def update_hotel_reservation(reservation_id: int, reservation: HotelReservation):
    reservation_data = db.child("reservations").child(reservation_id).get()
    if reservation_data.val() is not None:
        updated_reservation_data = reservation.dict()
        db.child("reservations").child(reservation_id).update(updated_reservation_data)
        return updated_reservation_data
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")

@router.delete("/{reservation_id}", response_model=dict)
def delete_hotel_reservation(reservation_id: int):
    reservation_data = db.child("reservations").child(reservation_id).get()
    if reservation_data.val() is not None:
        db.child("reservations").child(reservation_id).remove()
        return {"message": "Reservation deleted"}
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")
