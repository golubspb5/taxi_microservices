from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User, RoleEnum
from app.core.security import create_access_token

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(p: str):
    return pwd.hash(p)

def verify_password(plain, hashed):
    return pwd.verify(plain, hashed)

def create_user(db: Session, email: str, password: str, role: str = "passenger"):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    user = User(email=email, hashed_password=get_password_hash(password), role=RoleEnum(role))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    u = db.query(User).filter(User.email == email).first()
    if not u:
        return None
    if not verify_password(password, u.hashed_password):
        return None
    return u

def create_access_token(user_id: int):
    return create_access_token(subject=user_id)
