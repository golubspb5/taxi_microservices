from pydantic import BaseModel


class TariffBase(BaseModel):
    base_price: float
    price_per_cell: float
    t_cell: int


class TariffCreate(TariffBase):
    pass


class TariffUpdate(BaseModel):
    base_price: float | None = None
    price_per_cell: float | None = None
    t_cell: int | None = None


class TariffOut(TariffBase):
    id: int

    class Config:
        from_attributes = True
