from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database.firebase import db

router = APIRouter()

class Client(BaseModel):
    id: int
    name: str
    email: str

@router.post("/", response_model=Client)
def create_client(client: Client):
    client_id = client.id
    client_data = client.dict()
    
    # Here we assume db.child('clients') refers to the clients collection
    db.child("clients").child(client_id).set(client_data)
    return client_data

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int):
    client_data = db.child("clients").child(client_id).get()
    if client_data.val() is not None:
        return client_data.val()
    else:
        raise HTTPException(status_code=404, detail="Client not found")

@router.get("/", response_model=List[Client])
def get_clients():
    clients_data = db.child("clients").get().val()
    if clients_data is not None:
        # Assuming `val` gives us a dictionary of clients
        return list(clients_data)
    else:
        return []

@router.delete("/{client_id}", response_model=dict)
def delete_client(client_id: int):
    client_data = db.child("clients").child(client_id).get()
    if client_data.val() is not None:
        db.child("clients").child(client_id).remove()
        return {"message": "Client deleted"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")
