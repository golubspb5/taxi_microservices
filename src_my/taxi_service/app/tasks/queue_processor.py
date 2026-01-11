import asyncio
from sqlalchemy.orm import Session
from app.models.trip import Trip, TripStatus
from app.services.matching_service import assign_driver
from app.database import SessionLocal

CHECK_INTERVAL = 5  # сек

async def process_queue_loop():
    """
    Обработка очереди поездок, которые ждут свободного водителя.
    """
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        db: Session = SessionLocal()
        pending_trips = db.query(Trip).filter(Trip.status == TripStatus.PENDING).all()
        for trip in pending_trips:
            await assign_driver(db, trip)
        db.close()

if __name__ == "__main__":
    asyncio.run(process_queue_loop())
