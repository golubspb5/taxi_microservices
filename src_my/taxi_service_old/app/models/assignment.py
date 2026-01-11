from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(BigInteger, primary_key=True, index=True)

    trip_id = Column(BigInteger, ForeignKey("trips.id"), nullable=False, unique=True)
    driver_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    trip = relationship("Trip", back_populates="assignment")
    driver = relationship("User")

    def __repr__(self):
        return (
            f"<Assignment trip_id={self.trip_id} "
            f"driver_id={self.driver_user_id} active={self.is_active}>"
        )
