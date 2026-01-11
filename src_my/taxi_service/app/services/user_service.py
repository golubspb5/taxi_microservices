from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, password: str, role: str = "passenger") -> User:
        hashed = hash_password(password)
        user = User(email=email, hashed_password=hashed, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
