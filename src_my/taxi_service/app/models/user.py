from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    PASSENGER = "passenger"
    DRIVER = "driver"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    driver_status = relationship("DriverStatus", back_populates="user", uselist=False)
    trips_as_passenger = relationship("Trip", back_populates="passenger", foreign_keys="Trip.passenger_id")
    trips_as_driver = relationship("Trip", back_populates="driver", foreign_keys="Trip.driver_id")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
