from sqlalchemy.orm import Session
from app.models.trip import Trip, TripStatus

def get_driver_stats(db: Session, driver_user_id: int) -> dict:
    """
    Возвращает статистику водителя: количество завершенных поездок, отмен, среднее время подачи.
    """
    total_completed = db.query(Trip).filter(
        Trip.driver_user_id == driver_user_id,
        Trip.status == TripStatus.COMPLETED
    ).count()

    total_cancelled = db.query(Trip).filter(
        Trip.driver_user_id == driver_user_id,
        Trip.status == TripStatus.CANCELLED
    ).count()

    assigned_trips = db.query(Trip).filter(
        Trip.driver_user_id == driver_user_id,
        Trip.status == TripStatus.DRIVER_ASSIGNED
    ).all()

    avg_wait_time = 0
    if assigned_trips:
        total_seconds = sum(
            (trip.assigned_at - trip.created_at).total_seconds() for trip in assigned_trips
        )
        avg_wait_time = total_seconds / len(assigned_trips)

    return {
        "completed": total_completed,
        "cancelled": total_cancelled,
        "average_wait_seconds": avg_wait_time
    }

def get_passenger_stats(db: Session, passenger_user_id: int) -> dict:
    """
    Статистика пассажира: количество поездок, отмены, среднее время ожидания.
    """
    total_completed = db.query(Trip).filter(
        Trip.passenger_user_id == passenger_user_id,
        Trip.status == TripStatus.COMPLETED
    ).count()

    total_cancelled = db.query(Trip).filter(
        Trip.passenger_user_id == passenger_user_id,
        Trip.status == TripStatus.CANCELLED
    ).count()

    return {
        "completed": total_completed,
        "cancelled": total_cancelled
    }
