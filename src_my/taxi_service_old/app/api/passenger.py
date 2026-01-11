from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trip import TripCreate, TripResponse
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

@router.post("/trips", response_model=TripResponse)
def create_trip(payload: TripCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    resp = trip_service.create_trip(db, passenger_user_id=user_id, **payload.dict())
    return resp

@router.get("/me/trips")
def my_trips(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return trip_service.get_user_trips(db, user_id)
