from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, Token
from app.database import get_db
from app.services import user_service

router = APIRouter()

@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, payload.email, payload.password, payload.role)
    return {"id": user.id, "email": user.email, "role": user.role.value}

@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = user_service.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
