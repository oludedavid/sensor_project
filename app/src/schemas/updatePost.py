from datetime import datetime, timezone
from typing import Union
from pydantic import BaseModel

class UpdatePostRequest(BaseModel):
    post_id: int
    title: str
    content: str

    class Config:
        orm_mode = True