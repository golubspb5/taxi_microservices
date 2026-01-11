from pydantic import BaseModel
from enum import Enum

class TripStatus(str, Enum):
    PENDING = "pending"
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_ARRIVED = "driver_arrived"
    PASSENGER_ONBOARD = "passenger_onboard"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TripCreate(BaseModel):
    passenger_id: int
    pickup_location: str
    dropoff_location: str

class TripResponse(BaseModel):
    id: int
    passenger_id: int
    driver_id: int | None = None
    pickup_location: str
    dropoff_location: str
    status: TripStatus

    class Config:
        from_attributes = True  # заменяет старый orm_mode

class TripStatusUpdate(BaseModel):
    status: TripStatus

class TripAccept(BaseModel):
    driver_id: int
