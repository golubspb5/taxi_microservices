from pydantic import BaseModel
from enum import Enum
from typing import Optional


class RideStatus(str, Enum):
    CREATED = "created"              # Ожидает назначения водителя
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_CONFIRMED = "driver_confirmed"
    DRIVER_EN_ROUTE = "driver_en_route"
    PASSENGER_ONBOARD = "passenger_onboard"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RideBase(BaseModel):
    xs: int
    ys: int
    xd: int
    yd: int


class RideCreate(RideBase):
    passenger_id: int


class RideOut(RideBase):
    id: int
    passenger_id: int
    driver_id: Optional[int]
    status: RideStatus
    eta_to_pickup: Optional[int]
    eta_total: Optional[int]
    price: Optional[float]

    class Config:
        from_attributes = True


class RideStatusUpdate(BaseModel):
    status: RideStatus
