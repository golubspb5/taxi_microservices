from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TripStatus(str, enum.Enum):
    PENDING = "pending"
    DRIVER_ASSIGNED = "driver_assigned"
    DRIVER_ARRIVED = "driver_arrived"
    PASSENGER_ONBOARD = "passenger_onboard"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_x = Column(Integer, nullable=False)
    start_y = Column(Integer, nullable=False)
    end_x = Column(Integer, nullable=False)
    end_y = Column(Integer, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    status = Column(Enum(TripStatus), default=TripStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    passenger = relationship("User", back_populates="trips_as_passenger", foreign_keys=[passenger_id])
    driver = relationship("User", back_populates="trips_as_driver", foreign_keys=[driver_id])

    def __repr__(self):
        return f"<Trip id={self.id} status={self.status} passenger={self.passenger_id} driver={self.driver_id}>"
