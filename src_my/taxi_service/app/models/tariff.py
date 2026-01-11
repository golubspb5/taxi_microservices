from sqlalchemy import Column, Integer, Float, BigInteger
from app.database import Base

class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(BigInteger, primary_key=True, index=True)
    base_price = Column(Float, nullable=False, default=50.0)
    price_per_cell = Column(Float, nullable=False, default=5.0)
    t_cell = Column(Integer, nullable=False, default=2)  # время в секундах на одну клетку

    def __repr__(self):
        return f"<Tariff base={self.base_price} per_cell={self.price_per_cell} t_cell={self.t_cell}>"
