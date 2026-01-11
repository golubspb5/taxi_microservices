from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.trip import Trip, TripStatus
from app.models.assignment import Assignment
from app.models.tariff import Tariff
from app.services.distance import manhattan_distance, estimate_eta, estimate_price


class TripService:
    def __init__(self, db: Session):
        self.db = db

    def create_trip(self, passenger_id: int, xs: int, ys: int, xd: int, yd: int) -> Trip:
        # Берём текущий тариф
        tariff = self.db.query(Tariff).first()
        if not tariff:
            tariff = Tariff(base_price=50.0, price_per_cell=5.0, t_cell=2)
            self.db.add(tariff)
            self.db.commit()
            self.db.refresh(tariff)

        distance = manhattan_distance(xs, ys, xd, yd)
        price = estimate_price(tariff.base_price, tariff.price_per_cell, distance)
        eta_trip = estimate_eta(distance, tariff.t_cell)

        trip = Trip(
            passenger_user_id=passenger_id,
            xs=xs,
            ys=ys,
            xd=xd,
            yd=yd,
            price=price,
            eta_trip=eta_trip,
            status=TripStatus.pending
        )
        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def assign_driver(self, trip: Trip, driver_id: int, timeout_sec: int = 30) -> Assignment:
        """
        Назначение водителя на поездку с таймаутом подтверждения
        """
        expires_at = datetime.utcnow() + timedelta(seconds=timeout_sec)
        assignment = Assignment(
            trip_id=trip.id,
            driver_user_id=driver_id,
            expires_at=expires_at,
            is_active=True
        )
        trip.driver_user_id = driver_id
        trip.status = TripStatus.driver_assigned
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def update_trip_status(self, trip_id: int, status: TripStatus) -> Trip:
        trip = self.db.query(Trip).filter_by(id=trip_id).first()
        if not trip:
            return None
        trip.status = status
        if status == TripStatus.completed and trip.driver_user_id is not None:
            # Координаты водителя обновляем на точку высадки
            from app.models.driver_status import DriverStatus
            driver = self.db.query(DriverStatus).filter_by(user_id=trip.driver_user_id).first()
            if driver:
                driver.x = trip.xd
                driver.y = trip.yd
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def get_trip_history(self, user_id: int):
        """
        История поездок пользователя (как пассажир или водитель)
        """
        trips_as_passenger = self.db.query(Trip).filter_by(passenger_user_id=user_id).all()
        trips_as_driver = self.db.query(Trip).filter_by(driver_user_id=user_id).all()
        return trips_as_passenger + trips_as_driver
