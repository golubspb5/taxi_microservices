from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import trip_service, security

router = APIRouter()

def get_current_user_id(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing header")
    token = authorization.split(" ",1)[1] if " " in authorization else authorization
    uid = security.decode_access_token(token)
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token")
    return uid

@router.post("/trips/{trip_id}/accept")
def accept(trip_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return trip_service.accept_assignment(db, trip_id=trip_id, driver_id=user_id)

@router.put("/trips/{trip_id}/status")
def update_status(trip_id: int, status: dict, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return trip_service.update_status(db, trip_id=trip_id, user_id=user_id, status=status)
