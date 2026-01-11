from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class DriverState(str, enum.Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"

class DriverStatus(Base):
    __tablename__ = "driver_status"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    state = Column(Enum(DriverState), default=DriverState.OFFLINE, nullable=False)
    x = Column(Integer, default=0, nullable=False)
    y = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="driver_status")

    def __repr__(self):
        return f"<DriverStatus user_id={self.user_id} state={self.state} coords=({self.x},{self.y})>"
