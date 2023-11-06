from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.firebase import db

router = APIRouter()

class HotelRoom(BaseModel):
    id: int
    room_number: int
    capacity: int

@router.post("/", response_model=HotelRoom)
def create_hotel_room(room: HotelRoom):
    room_data = room.dict()
    db.child("hotel_rooms").child(room.id).set(room_data)
    return room_data

@router.get("/{room_id}", response_model=HotelRoom)
def get_hotel_room(room_id: int):
    room_data = db.child("hotel_rooms").child(room_id).get()
    if room_data.val() is not None:
        return room_data.val()
    else:
        raise HTTPException(status_code=404, detail="Hotel room not found")

# Si vous souhaitez mettre à jour les informations d'une chambre d'hôtel
@router.put("/{room_id}", response_model=HotelRoom)
def update_hotel_room(room_id: int, room: HotelRoom):
    existing_room_data = db.child("hotel_rooms").child(room_id).get()
    if existing_room_data.val() is not None:
        updated_room_data = room.dict()
        db.child("hotel_rooms").child(room_id).update(updated_room_data)
        return updated_room_data
    else:
        raise HTTPException(status_code=404, detail="Hotel room not found")

# Et si vous devez supprimer une chambre d'hôtel
@router.delete("/{room_id}", response_model=dict)
def delete_hotel_room(room_id: int):
    existing_room_data = db.child("hotel_rooms").child(room_id).get()
    if existing_room_data.val() is not None:
        db.child("hotel_rooms").child(room_id).remove()
        return {"message": "Hotel room deleted"}
    else:
        raise HTTPException(status_code=404, detail="Hotel room not found")
