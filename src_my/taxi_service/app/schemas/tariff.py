from pydantic import BaseModel

class TariffOut(BaseModel):
    id: int
    base_price: float
    price_per_cell: float
    t_cell: int

    class Config:
        orm_mode = True
