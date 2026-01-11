from datetime import datetime
from sqlalchemy.orm import Session
from app.models.driver_status import DriverStatus
from app.models.trip import Trip
from app.schemas.driver import DriverUpdatePosition


class DriverService:
    def __init__(self, db: Session):
        self.db = db

    def set_online(self, driver_id: int, position: DriverUpdatePosition):
        driver = self.db.query(DriverStatus).filter_by(user_id=driver_id).first()
        if not driver:
            driver = DriverStatus(user_id=driver_id)
            self.db.add(driver)

        driver.is_online = True
        driver.x = position.x
        driver.y = position.y
        driver.went_online_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(driver)
        return driver

    def set_offline(self, driver_id: int):
        driver = self.db.query(DriverStatus).filter_by(user_id=driver_id).first()
        if driver:
            driver.is_online = False
            self.db.commit()
        return driver

    def get_available_drivers(self):
        """
        Список всех водителей online и не занятых.
        """
        return (
            self.db.query(DriverStatus)
            .filter_by(is_online=True)
            .all()
        )

    def get_driver_status(self, driver_id: int):
        return self.db.query(DriverStatus).filter_by(user_id=driver_id).first()
