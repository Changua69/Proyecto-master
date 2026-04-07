from fastapi import APIRouter, Depends, HTTPException
from app.schemas.reservation import ReservationCreate
from app.database import reservations_collection, rooms_collection
from app.auth.jwt_handler import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/reservations", tags=["Reservations"])


# CREAR RESERVA (con validación de fechas)
@router.post("/create")
def crear_reserva(reservation: ReservationCreate, user=Depends(get_current_user)):

    # Validar fechas
    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail="Fechas inválidas")

    # Convertir fechas (ANTES de usarlas)
    check_in_dt = datetime.combine(reservation.check_in, datetime.min.time())
    check_out_dt = datetime.combine(reservation.check_out, datetime.min.time())

    room = rooms_collection.find_one({"number": reservation.room_number})

    if not room:
        raise HTTPException(status_code=404, detail="Habitación no existe")

    # Validar disponibilidad por fechas
    existing_reservation = reservations_collection.find_one({
        "room_number": reservation.room_number,
        "check_out": {"$gt": check_in_dt},
        "check_in": {"$lt": check_out_dt}
    })

    if existing_reservation:
        raise HTTPException(status_code=400, detail="Habitación no disponible en esas fechas")

    reservation_dict = reservation.dict()

    reservation_dict["check_in"] = check_in_dt
    reservation_dict["check_out"] = check_out_dt

    reservations_collection.insert_one(reservation_dict)

    rooms_collection.update_one(
        {"number": reservation.room_number},
        {"$set": {"status": "ocupada"}}
    )

    return {"message": "Reserva creada"}


# LISTAR RESERVAS
@router.get("/")
def listar_reservas(user=Depends(get_current_user)):

    reservas = list(reservations_collection.find())

    for r in reservas:
        r["_id"] = str(r["_id"])

    return reservas


# CANCELAR RESERVA
@router.delete("/{id}")
def cancelar_reserva(id: str, user=Depends(get_current_user)):

    reserva = reservations_collection.find_one({"_id": ObjectId(id)})

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # liberar habitación
    rooms_collection.update_one(
        {"number": reserva["room_number"]},
        {"$set": {"status": "disponible"}}
    )

    reservations_collection.delete_one({"_id": ObjectId(id)})

    return {"message": "Reserva cancelada"}


# MODIFICAR RESERVA
@router.put("/{id}")
def modificar_reserva(id: str, reservation: ReservationCreate, user=Depends(get_current_user)):

    if reservation.check_out <= reservation.check_in:
        raise HTTPException(status_code=400, detail="Fechas inválidas")

    # 🔥 Convertir fechas
    check_in_dt = datetime.combine(reservation.check_in, datetime.min.time())
    check_out_dt = datetime.combine(reservation.check_out, datetime.min.time())

    # 🔥 Validar solapamiento (excluyendo la misma reserva)
    existing_reservation = reservations_collection.find_one({
        "room_number": reservation.room_number,
        "check_out": {"$gt": check_in_dt},
        "check_in": {"$lt": check_out_dt},
        "_id": {"$ne": ObjectId(id)}
    })

    if existing_reservation:
        raise HTTPException(status_code=400, detail="Habitación no disponible en esas fechas")

    result = reservations_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "room_number": reservation.room_number,
            "guest_email": reservation.guest_email,
            "check_in": check_in_dt,
            "check_out": check_out_dt
        }}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    return {"message": "Reserva actualizada"}


# CHECK-IN
@router.put("/checkin/{room_number}")
def checkin(room_number: int, user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403, detail="No autorizado")

    rooms_collection.update_one(
        {"number": room_number},
        {"$set": {"status": "ocupada"}}
    )

    return {
        "message": "Check-in realizado",
        "habitacion": room_number,
        "hora": datetime.now()
    }

# CHECK-OUT
@router.put("/checkout/{room_number}")
def checkout(room_number: int, user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403, detail="No autorizado")

    rooms_collection.update_one(
        {"number": room_number},
        {"$set": {"status": "disponible"}}
    )

    return {
        "message": "Check-out realizado",
        "habitacion": room_number,
        "hora": datetime.now()
    }

@router.get("/recepcionista/reservas-hoy")
def reservas_hoy(user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403, detail="No autorizado")

    today = datetime.now().date()

    reservas = list(reservations_collection.find({
        "check_in": {"$lte": datetime.combine(today, datetime.max.time())},
        "check_out": {"$gte": datetime.combine(today, datetime.min.time())}
    }))

    for r in reservas:
        r["_id"] = str(r["_id"])

    return reservas

@router.get("/recepcionista/historial")
def historial_reservas(user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403, detail="No autorizado")

    reservas = list(reservations_collection.find())

    for r in reservas:
        r["_id"] = str(r["_id"])

    return reservas