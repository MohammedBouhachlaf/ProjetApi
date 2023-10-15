from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import List

app = FastAPI()


clients = []
hotel_rooms = []
reservations = []

class Client(BaseModel):
    id: int
    name: str
    email: str

class HotelRoom(BaseModel):
    id: int
    room_number: int
    capacity: int

class HotelReservation(BaseModel):
    id: int
    client_id: int
    room_id: int
    check_in_date: str
    check_out_date: str



@app.post("/clients/")
def create_client(client: Client):
    clients.append(client)
    return client

@app.get("/clients/{client_id}")
def get_client(client_id: int):
    for client in clients:
        if client.id == client_id:
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@app.get("/clients/", response_model=List[Client])
def get_clients():
    return clients


@app.post("/hotel-rooms/")
def create_hotel_room(room: HotelRoom):
    hotel_rooms.append(room)
    return room

@app.get("/hotel-rooms/{room_id}")
def get_hotel_room(room_id: int):
    for room in hotel_rooms:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=404, detail="Hotel room not found")

@app.post("/hotel-reservations/")
def create_hotel_reservation(reservation: HotelReservation):
 
    if reservation.client_id not in [client.id for client in clients] or reservation.room_id not in [room.id for room in hotel_rooms]:
        raise HTTPException(status_code=404, detail="Client or hotel room not found")
    
    reservations.append(reservation)
    return reservation

@app.get("/hotel-reservations/{reservation_id}")
def get_hotel_reservation(reservation_id: int):
    for reservation in reservations:
        if reservation.id == reservation_id:
            return reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

@app.put("/hotel-reservations/{reservation_id}")
def update_hotel_reservation(reservation_id: int, reservation: HotelReservation):
    for i, r in enumerate(reservations):
        if r.id == reservation_id:
          
            reservations[i] = reservation
            return reservation
    raise HTTPException(status_code=404, detail="Reservation not found")

@app.delete("/hotel-reservations/{reservation_id}")
def delete_hotel_reservation(reservation_id: int):
    for i, reservation in enumerate(reservations):
        if reservation.id == reservation_id:
            del reservations[i]
            return {"message": "Reservation deleted"}
    raise HTTPException(status_code=404, detail="Reservation not found")


