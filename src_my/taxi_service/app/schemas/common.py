from pydantic import BaseModel
from typing import Any, Optional

class MessageResponse(BaseModel):
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[Any] = None
