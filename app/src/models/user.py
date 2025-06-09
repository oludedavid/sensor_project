from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
from datetime import datetime
from app.src.connection.orm.ormDatabase import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    isActive = Column(Boolean, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )