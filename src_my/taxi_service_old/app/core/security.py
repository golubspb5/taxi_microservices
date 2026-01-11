from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

def create_access_token(subject: int, expires_delta: timedelta | None = None):
    expire = datetime.utcnow() + (expires_delta or settings.access_token_expires())
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return int(payload.get("sub"))
    except Exception:
        return None
