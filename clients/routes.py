from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database.firebase import db
from authentification.auth  import get_current_user  # Assurez-vous que ce chemin d'importation est correct

router = APIRouter()

class Client(BaseModel):
    id: int
    name: str
    email: str


# Ajoutez la dépendance à la route pour créer un client
@router.post("/", response_model=Client)
def create_client(client: Client, user_data: dict = Depends(get_current_user)):
    client_id = client.id
    client_data = client.dict()
    
    # Ici, utilisez le token ID de l'utilisateur pour effectuer les opérations avec Firebase
    db.child("clients").child(client_id).set(client_data, user_data['idToken'])
    return client_data

# Et ainsi de suite pour chaque route où vous voulez appliquer l'authentification
@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, user_data: dict = Depends(get_current_user)):
    client_data = db.child("clients").child(client_id).get(user_data['idToken']).val()
    if client_data:
        return client_data
    else:
        raise HTTPException(status_code=404, detail="Client not found")

@router.get("/", response_model=List[Client])
def get_clients(user_data: dict = Depends(get_current_user)):
    clients_data = db.child("clients").get(user_data['idToken']).val()
    if clients_data:
        return list(clients_data.values)
    else:
        return []

@router.delete("/{client_id}", response_model=dict)
def delete_client(client_id: int, user_data: dict = Depends(get_current_user)):
    client_data = db.child("clients").child(client_id).get(user_data['idToken']).val()
    if client_data:
        db.child("clients").child(client_id).remove(user_data['idToken'])
        return {"message": "Client deleted"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")
