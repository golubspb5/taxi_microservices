from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.driver import DriverUpdatePosition, DriverOut
from app.services.driver_service import DriverService
from fastapi.security import OAuth2PasswordBearer
import jwt

router = APIRouter(prefix="/drivers", tags=["Drivers"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"


def get_current_driver_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        driver_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return driver_id


@router.put("/me/presence", response_model=DriverOut)
def update_presence(
    position: DriverUpdatePosition,
    driver_id: int = Depends(get_current_driver_id),
    db: Session = Depends(get_db),
):
    service = DriverService(db)
    driver = service.set_online(driver_id, position)
    return driver


@router.put("/me/offline", response_model=DriverOut)
def go_offline(
    driver_id: int = Depends(get_current_driver_id),
    db: Session = Depends(get_db),
):
    service = DriverService(db)
    driver = service.set_offline(driver_id)
    return driver


@router.get("/", response_model=list[DriverOut])
def list_available_drivers(db: Session = Depends(get_db)):
    service = DriverService(db)
    return service.get_available_drivers()
