from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.models.trip import Trip, TripStatus
from app.models.driver_status import DriverStatus

def create_trip(db: Session, passenger_id: int, start: tuple[int, int], end: tuple[int, int], price: float) -> Trip:
    trip = Trip(
        passenger_user_id=passenger_id,
        start_x=start[0],
        start_y=start[1],
        end_x=end[0],
        end_y=end[1],
        price=price,
        status=TripStatus.PENDING,
        created_at=datetime.utcnow()
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

def cancel_trip(db: Session, trip_id: int, user_id: int) -> Optional[Trip]:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.passenger_user_id == user_id).first()
    if not trip or trip.status in [TripStatus.PASSENGER_ONBOARD, TripStatus.IN_PROGRESS, TripStatus.COMPLETED]:
        return None
    trip.status = TripStatus.CANCELLED
    db.commit()
    db.refresh(trip)
    return trip

def complete_trip(db: Session, trip_id: int) -> Optional[Trip]:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return None
    trip.status = TripStatus.COMPLETED

    if trip.driver_user_id:
        driver = db.query(DriverStatus).filter(DriverStatus.user_id == trip.driver_user_id).first()
        if driver:
            driver.x = trip.end_x
            driver.y = trip.end_y
            db.commit()
            db.refresh(driver)

    db.commit()
    db.refresh(trip)
    return trip

def get_user_trips(db: Session, user_id: int) -> List[Trip]:
    return db.query(Trip).filter(Trip.passenger_user_id == user_id).all()
