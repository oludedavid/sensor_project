from pydantic import BaseModel
from datetime import datetime
from typing import List

class ReadPostModel(BaseModel):
    post_id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True

class PostSingleResponse(BaseModel):
    data: ReadPostModel
    status_code: int

class PostListResponse(BaseModel):
    data: List[ReadPostModel]
    status_code: int