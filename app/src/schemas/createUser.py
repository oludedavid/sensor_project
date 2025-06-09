from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


