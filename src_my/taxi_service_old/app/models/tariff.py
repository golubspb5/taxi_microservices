from sqlalchemy import Column, BigInteger, Float, Integer
from app.database import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(BigInteger, primary_key=True, index=True)

    base_price = Column(Float, nullable=False, default=50.0)
    price_per_cell = Column(Float, nullable=False, default=5.0)

    # время за одну клетку движения водителя (сек)
    t_cell = Column(Integer, nullable=False, default=2)

    def __repr__(self):
        return (
            f"<Tariff base={self.base_price} "
            f"per_cell={self.price_per_cell} t_cell={self.t_cell}>"
        )
