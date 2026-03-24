from fastapi import APIRouter, Depends, HTTPException
from app.auth.jwt_handler import get_current_user
from app.database import users_collection, rooms_collection, reservations_collection

router = APIRouter()


# 👤 DASHBOARD HUÉSPED
@router.get("/huesped/dashboard", tags=["Huesped"])
def huesped_dashboard(user=Depends(get_current_user)):

    if user["role"] != "huesped":
        raise HTTPException(status_code=403, detail="No autorizado")

    reservas = list(reservations_collection.find({"guest_email": user["sub"]}))

    for r in reservas:
        r["_id"] = str(r["_id"])

    return {
        "mensaje": "Bienvenido huésped",
        "email": user["sub"],
        "mis_reservas": reservas
    }


# 🧑‍💼 DASHBOARD RECEPCIONISTA
@router.get("/recepcionista/dashboard", tags=["Recepcionista"])
def recepcionista_dashboard(user=Depends(get_current_user)):

    if user["role"] != "recepcionista":
        raise HTTPException(status_code=403, detail="No autorizado")

    reservas = list(reservations_collection.find())
    habitaciones_disponibles = list(rooms_collection.find({"status": "disponible"}))

    for r in reservas:
        r["_id"] = str(r["_id"])

    for h in habitaciones_disponibles:
        h["_id"] = str(h["_id"])

    return {
        "mensaje": "Panel recepcionista",
        "total_reservas": len(reservas),
        "habitaciones_disponibles": habitaciones_disponibles,
        "reservas": reservas
    }


# 👑 DASHBOARD ADMIN
@router.get("/admin/dashboard", tags=["Admin"])
def admin_dashboard(user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    total_users = users_collection.count_documents({})
    total_rooms = rooms_collection.count_documents({})
    available_rooms = rooms_collection.count_documents({"status": "disponible"})
    total_reservations = reservations_collection.count_documents({})

    # 💰 Calcular ingresos
    total_ingresos = 0
    reservas = reservations_collection.find()

    for r in reservas:
        room = rooms_collection.find_one({"number": r["room_number"]})
        if room:
            dias = (r["check_out"] - r["check_in"]).days
            total_ingresos += dias * room["price"]

    # 📊 Ocupación (%)
    ocupacion = 0
    if total_rooms > 0:
        ocupacion = ((total_rooms - available_rooms) / total_rooms) * 100

    return {
        "usuarios_registrados": total_users,
        "habitaciones_totales": total_rooms,
        "habitaciones_disponibles": available_rooms,
        "reservas_totales": total_reservations,
        "ingresos_totales": total_ingresos,
        "ocupacion_porcentaje": round(ocupacion, 2)
    }