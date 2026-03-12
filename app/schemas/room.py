from pydantic import BaseModel


class RoomCreate(BaseModel):
    number: int
    type: str
    price: float