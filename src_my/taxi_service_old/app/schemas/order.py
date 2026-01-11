from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    from_x: int
    from_y: int
    to_x: int
    to_y: int


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    user_id: int
    status: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True
