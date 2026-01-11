from pydantic import BaseModel


class DriverBase(BaseModel):
    name: str


class DriverCreate(DriverBase):
    pass


class DriverUpdatePosition(BaseModel):
    x: int
    y: int


class DriverOut(DriverBase):
    id: int
    x: int
    y: int
    is_busy: bool

    class Config:
        from_attributes = True
