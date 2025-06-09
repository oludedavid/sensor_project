from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserLoginResponse(BaseModel):
   access_token: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


