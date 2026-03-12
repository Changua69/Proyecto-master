from pydantic import BaseModel
from datetime import date

class ReservationCreate(BaseModel):
    room_number: int
    guest_email: str
    check_in: date
    check_out: date