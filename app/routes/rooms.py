from fastapi import APIRouter, Depends, HTTPException
from app.schemas.room import RoomCreate
from app.database import rooms_collection
from app.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/create")
def crear_habitacion(room: RoomCreate, user=Depends(get_current_user)):

    if user["role"] not in ["admin", "recepcionista"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    existing = rooms_collection.find_one({"numero": room.number})

    if existing:
        raise HTTPException(status_code=400, detail="Habitación ya existe")

    room_dict = room.dict()
    room_dict["status"] = "disponible"

    rooms_collection.insert_one(room_dict)

    return {"message": "Habitación creada"}


@router.get("/available")
def habitaciones_disponibles():

    rooms = list(rooms_collection.find({"status": "disponible"}, {"_id": 0}))

    return rooms