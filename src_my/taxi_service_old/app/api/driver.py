from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.driver import DriverPresence
from app.services import driver_service, security

router = APIRouter()

def get_current_user_id(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing header")
    token = authorization.split(" ",1)[1] if " " in authorization else authorization
    uid = security.decode_access_token(token)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token")
    return uid

@router.put("/drivers/me/presence")
def presence(payload: DriverPresence, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return driver_service.update_presence(db, user_id=user_id, status=payload.status, x=payload.x, y=payload.y)

@router.get("/drivers/me/trips")
def driver_trips(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return driver_service.get_driver_trips(db, driver_id=user_id)
