from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timedelta

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    trip = relationship("Trip", backref="assignments")
    driver = relationship("User", backref="assignments")

    def __repr__(self):
        return f"<Assignment trip_id={self.trip_id} driver_id={self.driver_id} confirmed={self.confirmed}>"

    @staticmethod
    def create_expiry(timeout_seconds: int) -> datetime:
        """Вычислить время истечения подтверждения назначения"""
        return datetime.utcnow() + timedelta(seconds=timeout_seconds)
