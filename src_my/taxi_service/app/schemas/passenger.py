from pydantic import BaseModel, conint
from typing import Optional

class TripCreate(BaseModel):
    start_x: conint(ge=0)
    start_y: conint(ge=0)
    end_x: conint(ge=0)
    end_y: conint(ge=0)

class TripOut(BaseModel):
    trip_id: int
    status: str
    estimated_price: float
    eta_seconds: int

    class Config:
        orm_mode = True
