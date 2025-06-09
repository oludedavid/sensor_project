from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from datetime import datetime
from app.src.connection.orm.ormDatabase import Base

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
