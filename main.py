from fastapi import FastAPI
from clients.routes import router as client_router
from hotel_rooms.routes import router as hotel_room_router
from hotel_reservations.routes import router as hotel_reservation_router

app = FastAPI()

app.include_router(client_router, prefix="/clients", tags=["clients"])
app.include_router(hotel_room_router, prefix="/hotel-rooms", tags=["hotel-rooms"])
app.include_router(hotel_reservation_router, prefix="/hotel-reservations", tags=["hotel-reservations"])
