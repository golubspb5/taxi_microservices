from sqlalchemy import (
    Column, BigInteger, Integer, ForeignKey, String,
    TIMESTAMP, func, Enum, Float
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class TripStatus(str, enum.Enum):
    pending = "pending"                # заказ создан, ищем водителя
    driver_assigned = "driver_assigned" # водитель назначен, ждём подтверждения
    driver_confirmed = "driver_confirmed" # водитель подтвердил, едет к пассажиру
    passenger_onboard = "passenger_onboard" # пассажир сел
    in_progress = "in_progress"        # поездка началась
    completed = "completed"            # окончено
    cancelled = "cancelled"            # отменено пассажиром
    expired = "expired"                # просрочено (не нашли водителя)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(BigInteger, primary_key=True, index=True)

    passenger_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    driver_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    # координаты
    xs = Column(Integer, nullable=False)
    ys = Column(Integer, nullable=False)
    xd = Column(Integer, nullable=False)
    yd = Column(Integer, nullable=False)

    # расчетная информация
    eta_to_pickup = Column(Integer, nullable=True)     # сек
    eta_trip = Column(Integer, nullable=True)          # сек
    price = Column(Float, nullable=True)

    status = Column(Enum(TripStatus), nullable=False, default=TripStatus.pending)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    passenger = relationship("User", back_populates="trips_as_passenger", foreign_keys=[passenger_user_id])
    driver = relationship("User", back_populates="trips_as_driver", foreign_keys=[driver_user_id])

    assignment = relationship("Assignment", back_populates="trip", uselist=False)

    def __repr__(self):
        return f"<Trip id={self.id} status={self.status}>"
