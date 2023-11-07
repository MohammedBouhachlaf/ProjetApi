from fastapi import FastAPI
from clients.routes import router as client_router
from hotel_rooms.routes import router as hotel_room_router
from hotel_reservations.routes import router as hotel_reservation_router
from authentification.auth import router as auth_router  # Importez le routeur d'authentification
import stripes.stripe
app = FastAPI()

# Inclure le routeur d'authentification
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Inclure les autres routeurs
app.include_router(client_router, prefix="/clients", tags=["clients"])
app.include_router(hotel_room_router, prefix="/hotel-rooms", tags=["hotel-rooms"])
app.include_router(hotel_reservation_router, prefix="/hotel-reservations", tags=["hotel-reservations"])
app.include_router(stripes.stripe.router)

# ... reste de votre code ...

