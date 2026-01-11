from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.passenger import TripCreate, TripOut
from app.services.trip_service import create_trip, get_user_trips
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/passenger", tags=["passenger"])

@router.post("/trips", response_model=TripOut)
def create_trip_route(trip_in: TripCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    trip = create_trip(
        db,
        passenger_id=current_user.id,
        start=(trip_in.start_x, trip_in.start_y),
        end=(trip_in.end_x, trip_in.end_y),
        price=0  # цена позже через pricing_service
    )
    return trip

@router.get("/trips", response_model=list[TripOut])
def list_trips_route(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    trips = get_user_trips(db, current_user.id)
    return trips
