from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HotelRoom(BaseModel):
    id: int
    room_number: int
    capacity: int

hotel_rooms = []

@router.post("/")
def create_hotel_room(room: HotelRoom):
    hotel_rooms.append(room)
    return room

@router.get("/{room_id}")
def get_hotel_room(room_id: int):
    for room in hotel_rooms:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=404, detail="Hotel room not found")
