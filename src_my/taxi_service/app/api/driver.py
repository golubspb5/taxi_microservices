from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.driver import DriverPresenceUpdate
from app.services.driver_service import update_driver_presence, get_driver_status
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/driver", tags=["driver"])

@router.put("/me/presence")
def update_presence_route(presence: DriverPresenceUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    driver = update_driver_presence(db, current_user.id, presence)
    return driver

@router.get("/me/status")
def get_status_route(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    driver = get_driver_status(db, current_user.id)
    return driver
