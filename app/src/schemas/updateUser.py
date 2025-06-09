from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.src.schemas.readUser import ReadUserResponse

class UpdateUserRequest(BaseModel):
    user_id: int 
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UpdateUserResponse(BaseModel):
    data: ReadUserResponse
    status_code: int