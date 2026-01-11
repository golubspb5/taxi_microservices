import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.models.trip import Trip, TripStatus
from app.database import SessionLocal

TIMEOUT_SECONDS = 30  # таймаут подтверждения водителя

async def check_assignments_loop():
    """
    Периодическая проверка назначений на таймаут.
    Если водитель не подтвердил назначение — снимаем блокировку и переводим заказ в очередь.
    """
    while True:
        await asyncio.sleep(5)  # проверка каждые 5 секунд
        db: Session = SessionLocal()
        now = datetime.utcnow()
        expired_assignments = db.query(Assignment).filter(
            Assignment.created_at + timedelta(seconds=TIMEOUT_SECONDS) < now,
            Assignment.status == "pending"
        ).all()

        for assign in expired_assignments:
            trip = db.query(Trip).filter(Trip.id == assign.trip_id).first()
            if trip:
                trip.status = TripStatus.PENDING
            assign.status = "timeout"
            db.commit()
        db.close()

if __name__ == "__main__":
    asyncio.run(check_assignments_loop())
