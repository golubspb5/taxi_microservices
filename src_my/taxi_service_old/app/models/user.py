from sqlalchemy import Column, BigInteger, String, Enum, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    passenger = "passenger"
    driver = "driver"


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.passenger)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # связи (lazy='joined' не ставлю — можно контролировать в запросах)
    driver_status = relationship("DriverStatus", back_populates="user", uselist=False, cascade="all,delete")
    trips_as_passenger = relationship("Trip", back_populates="passenger", foreign_keys="Trip.passenger_user_id")
    trips_as_driver = relationship("Trip", back_populates="driver", foreign_keys="Trip.driver_user_id")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>" 
