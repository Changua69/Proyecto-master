from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import users_collection
from app.schemas.user import UserRegister
from app.auth.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
def register(user: UserRegister):

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    hashed_password = pwd_context.hash(user.password)

    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phone": user.phone,
        "role": "huesped"
    }

    users_collection.insert_one(user_dict)

    return {"message": f"Bienvenido {user.name} al Marea Dorada Resort"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    existing_user = users_collection.find_one({"email": form_data.username})

    if not existing_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not pwd_context.verify(form_data.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({
        "sub": existing_user["email"],
        "role": existing_user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": existing_user["role"]
    }