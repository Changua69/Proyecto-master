from fastapi import APIRouter, Depends, HTTPException
from app.schemas.room import RoomCreate
from app.database import rooms_collection
from app.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# CREAR
@router.post("/create")
def crear_habitacion(room: RoomCreate, user=Depends(get_current_user)):

    if user["role"] not in ["admin", "recepcionista"]:
        raise HTTPException(status_code=403, detail="No autorizado")

    existing = rooms_collection.find_one({"number": room.number})

    if existing:
        raise HTTPException(status_code=400, detail="Habitación ya existe")

    room_dict = room.dict()
    room_dict["status"] = "disponible"

    rooms_collection.insert_one(room_dict)

    return {"message": "Habitación creada"}


# LISTAR TODAS
@router.get("/")
def listar_habitaciones():

    rooms = list(rooms_collection.find())

    for room in rooms:
        room["_id"] = str(room["_id"])

    return rooms


# DISPONIBLES
@router.get("/available")
def habitaciones_disponibles():

    rooms = list(rooms_collection.find({"status": "disponible"}))

    for room in rooms:
        room["_id"] = str(room["_id"])

    return rooms


# ACTUALIZAR
@router.put("/{number}")
def actualizar_habitacion(number: int, room: RoomCreate, user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    result = rooms_collection.update_one(
        {"number": number},
        {"$set": room.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    return {"message": "Habitación actualizada"}


# ELIMINAR
@router.delete("/{number}")
def eliminar_habitacion(number: int, user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    result = rooms_collection.delete_one({"number": number})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    return {"message": "Habitación eliminada"}

@router.get("/search")
def buscar_habitaciones(type: str = None):

    query = {"status": "disponible"}

    if type:
        query["type"] = type

    rooms = list(rooms_collection.find(query))

    for room in rooms:
        room["_id"] = str(room["_id"])

    return rooms

@router.get("/{number}")
def obtener_habitacion(number: int):

    room = rooms_collection.find_one({"number": number})

    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    room["_id"] = str(room["_id"])

    return room