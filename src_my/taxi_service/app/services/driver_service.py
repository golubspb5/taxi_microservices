from sqlalchemy.orm import Session
from datetime import datetime
from app.models.driver_status import DriverStatus
from app.schemas.driver import DriverPresenceUpdate

# Обновление статуса водителя
def update_driver_presence(db: Session, user_id: int, data: DriverPresenceUpdate) -> DriverStatus:
    driver = db.query(DriverStatus).filter(DriverStatus.user_id == user_id).first()
    if not driver:
        driver = DriverStatus(
            user_id=user_id,
            state=data.state,
            x=data.x,
            y=data.y,
            last_seen=datetime.utcnow()
        )
        db.add(driver)
    else:
        driver.state = data.state
        driver.x = data.x
        driver.y = data.y
        driver.last_seen = datetime.utcnow()
    
    db.commit()
    db.refresh(driver)
    return driver

# Получение статуса водителя
def get_driver_status(db: Session, user_id: int) -> DriverStatus | None:
    return db.query(DriverStatus).filter(DriverStatus.user_id == user_id).first()
