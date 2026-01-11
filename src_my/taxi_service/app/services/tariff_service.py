from sqlalchemy.orm import Session
from app.models.tariff import Tariff

def get_current_tariff(db: Session) -> Tariff:
    """
    Возвращает активный тариф. На практике может быть один тариф с id=1.
    """
    tariff = db.query(Tariff).first()
    if not tariff:
        # создаем дефолтный тариф, если нет
        tariff = Tariff(base_price=50.0, price_per_cell=5.0, t_cell=2)
        db.add(tariff)
        db.commit()
        db.refresh(tariff)
    return tariff
