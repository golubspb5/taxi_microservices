from sqlalchemy.orm import Session
from typing import Optional
from app.models.driver_status import DriverStatus
from app.models.trip import Trip, TripStatus
from app.services.distance import manhattan_distance
from datetime import datetime, timedelta

ASSIGNMENT_TIMEOUT = 30  # секунд, таймаут на подтверждение водителем

def find_nearest_driver(db: Session, trip: Trip) -> Optional[DriverStatus]:
    """
    Находит ближайшего свободного водителя по Манхэттенскому расстоянию.
    Если несколько водителей на одинаковом расстоянии — выбирается по минимальному user_id.
    """
    drivers = db.query(DriverStatus).filter(DriverStatus.state == "online").all()
    if not drivers:
        return None

    min_dist = None
    candidate = None
    for driver in drivers:
        # проверка, что у водителя нет активной поездки
        active_trip = db.query(Trip).filter(
            Trip.driver_user_id == driver.user_id,
            Trip.status.in_([
                TripStatus.DRIVER_ASSIGNED,
                TripStatus.DRIVER_ARRIVED,
                TripStatus.PASSENGER_ONBOARD,
                TripStatus.IN_PROGRESS
            ])
        ).first()
        if active_trip:
            continue

        dist = manhattan_distance(
            (trip.start_x, trip.start_y),
            (driver.x, driver.y)
        )

        if (min_dist is None) or (dist < min_dist) or (dist == min_dist and driver.user_id < candidate.user_id):
            min_dist = dist
            candidate = driver

    return candidate

def assign_driver(db: Session, trip: Trip, driver: DriverStatus):
    """
    Назначает водителя на поездку и ставит статус DRIVER_ASSIGNED.
    """
    trip.driver_user_id = driver.user_id
    trip.status = TripStatus.DRIVER_ASSIGNED
    trip.assigned_at = datetime.utcnow()
    db.commit()
    db.refresh(trip)
    return trip

def check_assignment_timeouts(db: Session):
    """
    Проверяет все назначения, у которых истек таймаут на подтверждение водителем.
    """
    now = datetime.utcnow()
    trips = db.query(Trip).filter(
        Trip.status == TripStatus.DRIVER_ASSIGNED,
        Trip.assigned_at != None
    ).all()
    for trip in trips:
        elapsed = (now - trip.assigned_at).total_seconds()
        if elapsed > ASSIGNMENT_TIMEOUT:
            trip.status = TripStatus.PENDING
            trip.driver_user_id = None
            trip.assigned_at = None
            db.commit()
