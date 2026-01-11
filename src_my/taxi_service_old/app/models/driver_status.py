from sqlalchemy import Column, BigInteger, Integer, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base


class DriverStatus(Base):
    __tablename__ = "driver_status"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    is_online = Column(Boolean, nullable=False, default=False)

    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)

    # используется для tie-break при выборе ближайшего водителя
    went_online_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="driver_status")

    def __repr__(self):
        return f"<DriverStatus user_id={self.user_id} online={self.is_online} coords=({self.x},{self.y})>"
