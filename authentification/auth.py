from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from firebase_admin import auth

router = APIRouter()

# Dépendance pour gérer l'authentification OAuth2 avec le mot de passe et le bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Création d'une route pour l'inscription
@router.post("/signup")
def create_user(email: str, password: str):
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Création d'une route pour la connexion
@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = auth.get_user_by_email(form_data.username)
        # Vous devriez vérifier le mot de passe ici. FastAPI ne stocke ni ne vérifie les mots de passe.
        # À la place, vous utiliseriez le client Firebase pour obtenir un token côté client
        # puis l'envoyer ici pour l'échanger contre un token d'accès.
        # La vérification du mot de passe est généralement effectuée côté client.
        token = auth.create_custom_token(user.uid)
        return {"access_token": token, "token_type": "bearer"}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Middleware pour vérifier le token d'accès dans les requêtes
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Vérifiez le token avec Firebase Auth
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Exemple d'utilisation du middleware pour protéger une route
@router.get("/protected-route")
def protected_route(current_user: dict = Security(get_current_user)):
    return {"message": "Vous êtes authentifié", "user": current_user}
