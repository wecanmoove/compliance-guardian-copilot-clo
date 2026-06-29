from sqlalchemy import Column, String, DateTime, Boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

from ..db.base import Base

class UserEntity(Base):
    __tablename__ = "users"
    
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    role = Column(String(50), nullable=False, default="user")  # admin, manager, user
    is_active = Column(Boolean, default=True)
    tenant_id = Column(String(36), nullable=False, default="default")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserModel(BaseModel):
    user_id: str = None
    email: str
    full_name: str = None
    role: str = "user"
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = None
    role: str = "user"

class UserLogin(BaseModel):
    email: str
    password: str
