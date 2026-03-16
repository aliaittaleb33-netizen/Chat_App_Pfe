from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title=" API Backend Utilisateur ")

# Modèle de données avec adresse fictive
class User(BaseModel):
    id: int
    name: str
    email: str
    address: str

# Base de données fictive en mémoire
users_db: List[User] = []

@app.get("/")
def read_root():
    print(" API démarrée à http://127.0.0.1:8000/")
    return {"message": " backend Python pour gestion utilisateurs"}

@app.get("/users", response_model=List[User])
def get_users():
    print(" Liste des utilisateurs consultée.")
    return users_db

@app.post("/users", response_model=User)
def create_user(user: User):
    for u in users_db:
        if u.id == user.id:
            print(" Tentative d’ajout avec un ID existant :", user.id)
            raise HTTPException(status_code=400, detail="ID déjà utilisé")
    users_db.append(user)
    print(" Utilisateur ajouté :", user)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, request: Request):
    client_ip = request.client.host
    for user in users_db:
        if user.id == user_id:
            print(f"🔎 Utilisateur {user_id} consulté depuis {client_ip}")
            return user
    print(f"❌ Utilisateur {user_id} introuvable (IP: {client_ip})")
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = updated_user
            print(" Utilisateur mis à jour :", updated_user)
            return updated_user
    raise HTTPException(status_code=404, detail="Utilisateur à modifier non trouvé")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            print("🗑️ Utilisateur supprimé :", user)
            return {"message": f"Utilisateur {user_id} supprimé"}
    raise HTTPException(status_code=404, detail="Utilisateur à supprimer non trouvé")

# Lancement manuel avec adresse affichée
if __name__ == "__main__":
    print(" Démarrage de l'API...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
