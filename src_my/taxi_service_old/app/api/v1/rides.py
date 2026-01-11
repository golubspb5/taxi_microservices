from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.ride import RideCreate, RideOut, RideStatusUpdate
from app.services.trip_service import TripService
from fastapi.security import OAuth2PasswordBearer
import jwt

router = APIRouter(prefix="/rides", tags=["Rides"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


@router.post("/", response_model=RideOut)
def create_ride(
    ride_in: RideCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    service = TripService(db)
    ride = service.create_trip(
        passenger_id=user_id,
        xs=ride_in.xs,
        ys=ride_in.ys,
        xd=ride_in.xd,
        yd=ride_in.yd,
    )
    return ride


@router.put("/{ride_id}/status", response_model=RideOut)
def update_ride_status(
    ride_id: int,
    status_in: RideStatusUpdate,
    db: Session = Depends(get_db),
):
    service = TripService(db)
    ride = service.update_trip_status(ride_id, status_in.status)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride


@router.get("/history", response_model=list[RideOut])
def ride_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    service = TripService(db)
    trips = service.get_trip_history(user_id)
    return trips
