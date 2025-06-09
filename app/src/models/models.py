from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.src.connection.orm.ormDatabase import Base
import bcrypt
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

class RoleEnum(PyEnum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="False")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )

    #realationships User to Posts 1 to many: a user can make many post, a post can only have one user
    posts = relationship("Post", back_populates='owner', uselist=True, cascade="all, delete")
    dashboard = relationship("Dashboard", back_populates="owner", uselist=False)
    role = relationship("Role", back_populates="role_owners")

    def hash_password(self, password: str):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())#returns as a byte
        self.hashed_password = hashed.decode('utf-8')#removes byte to ensure it is stored a str

    def validate_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))#it encodes back to bytes and compare


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    owner = relationship("User", back_populates="posts", uselist=False)
    comments = relationship('Comment', back_populates='post')



class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    post = relationship('Post', back_populates='comments', uselist=False)

class Dashboard(Base):
    __tablename__ = "dashboards"
    dashboard_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    owner = relationship("User", back_populates="dashboard") 


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, nullable=False, primary_key=True)
    role_name = Column(String, nullable=False, index=True)
    role_owners = relationship("User", back_populates="role", uselist=True)