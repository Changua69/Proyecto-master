from fastapi import APIRouter, Depends, HTTPException
from app.schemas.reservation import ReservationCreate
from app.database import reservations_collection, rooms_collection
from app.auth.jwt_handler import get_current_user
from datetime import datetime

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/create")
def crear_reserva(reservation: ReservationCreate, user=Depends(get_current_user)):

    room = rooms_collection.find_one({"number": reservation.room_number})

    if not room:
        raise HTTPException(status_code=404, detail="Habitación no existe")

    if room.get("status") != "disponible":
        raise HTTPException(status_code=400, detail="Habitación ocupada")

    reservation_dict = reservation.dict()

    # Convertir date → datetime
    reservation_dict["check_in"] = datetime.combine(
        reservation.check_in, datetime.min.time()
    )
    reservation_dict["check_out"] = datetime.combine(
        reservation.check_out, datetime.min.time()
    )

    reservations_collection.insert_one(reservation_dict)

    rooms_collection.update_one(
        {"number": reservation.room_number},
        {"$set": {"status": "ocupada"}}
    )

    return {"message": "Reserva creada"}