from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.trip import TripStatusUpdate
from app.services.trip_service import complete_trip, cancel_trip
from app.services.matching_service import assign_driver, find_nearest_driver
from app.core.deps import get_db, get_current_user
from app.models.trip import Trip

router = APIRouter(prefix="/trips", tags=["trips"])

@router.post("/{trip_id}/accept")
def accept_trip_route(trip_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        return {"error": "Trip not found"}
    driver = find_nearest_driver(db, trip)
    if not driver:
        return {"error": "No available driver"}
    assign_driver(db, trip, driver)
    return {"status": "accepted", "driver_id": driver.user_id}

@router.put("/{trip_id}/status")
def update_trip_status_route(trip_id: int, status_in: TripStatusUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    trip = complete_trip(db, trip_id) if status_in.status == "completed" else cancel_trip(db, trip_id, current_user.id)
    if not trip:
        return {"error": "Cannot update trip"}
    return {"status": "updated"}
