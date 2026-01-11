from sqlalchemy.orm import Session
from app.models.tariff import Tariff
from app.schemas.tariff import TariffUpdate


class TariffService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_tariff(self) -> Tariff:
        tariff = self.db.query(Tariff).first()
        if not tariff:
            # Создаём дефолтный тариф
            tariff = Tariff(base_price=50.0, price_per_cell=5.0, t_cell=2)
            self.db.add(tariff)
            self.db.commit()
            self.db.refresh(tariff)
        return tariff

    def update_tariff(self, data: TariffUpdate) -> Tariff:
        tariff = self.get_current_tariff()
        if data.base_price is not None:
            tariff.base_price = data.base_price
        if data.price_per_cell is not None:
            tariff.price_per_cell = data.price_per_cell
        if data.t_cell is not None:
            tariff.t_cell = data.t_cell
        self.db.commit()
        self.db.refresh(tariff)
        return tariff
