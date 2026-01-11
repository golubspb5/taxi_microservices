from pydantic import BaseModel, conint
from enum import Enum
from typing import Optional

class DriverState(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"

class DriverPresenceUpdate(BaseModel):
    state: DriverState
    x: conint(ge=0)  # координата X >= 0
    y: conint(ge=0)  # координата Y >= 0

class DriverStatusOut(BaseModel):
    user_id: int
    state: DriverState
    x: int
    y: int

    class Config:
        orm_mode = True
