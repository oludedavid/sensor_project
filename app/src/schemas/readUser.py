from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ReadUserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    hashed_password: str


class UserSingleResponse(BaseModel):
    data: ReadUserResponse
    status_code: int

class UserListResponse(BaseModel):
    data: List[ReadUserResponse]
    status_code: int

