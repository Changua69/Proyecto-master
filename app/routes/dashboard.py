from fastapi import APIRouter, Depends, HTTPException
from app.auth.jwt_handler import get_current_user
from app.database import users_collection, rooms_collection, reservations_collection

router = APIRouter()


@router.get("/huesped/dashboard", tags=["Huesped"])
def huesped_dashboard(user=Depends(get_current_user)):

    if user["role"] != "huesped":
        raise HTTPException(status_code=403)

    return {
        "message": "Bienvenido huésped",
        "email": user["sub"]
    }


@router.get("/recepcionista/dashboard", tags=["Recepcionista"])
def recepcionista_dashboard(user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403)

    return {
        "message": "Bienvenido recepcionista",
        "email": user["sub"]
    }
    
@router.get("/admin/dashboard", tags=["Admin"])
def admin_dashboard(user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    total_users = users_collection.count_documents({})
    total_rooms = rooms_collection.count_documents({})
    available_rooms = rooms_collection.count_documents({"status": "disponible"})
    total_reservations = reservations_collection.count_documents({})

    return {
        "usuarios_registrados": total_users,
        "habitaciones_totales": total_rooms,
        "habitaciones_disponibles": available_rooms,
        "reservas_totales": total_reservations
    }