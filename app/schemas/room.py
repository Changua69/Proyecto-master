from pydantic import BaseModel
from typing import List


class RoomCreate(BaseModel):
    number: int
    type: str
    price: float
    description: str
    services: List[str]
    image: str