from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Client(BaseModel):
    id: int
    name: str
    email: str

clients = []

@router.post("/")
def create_client(client: Client):
    clients.append(client)
    return client

@router.get("/{client_id}")
def get_client(client_id: int):
    for client in clients:
        if client.id == client_id:
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@router.get("/", response_model=List[Client])
def get_clients():
    return clients

@router.delete("/{client_id}", response_model=dict)
def delete_client(client_id: int):
    for i, client in enumerate(clients):
        if client.id == client_id:
            del clients[i]
            return {"message": "Client deleted"}
    raise HTTPException(status_code=404, detail="Client not found")
