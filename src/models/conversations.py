from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
import uuid

from ..db.base import Base

class ConversationEntity(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    tenant_id = Column(String(36), nullable=False, default="default")
    context = Column(Text, nullable=True)  # JSON storing doc_ids, obligation_ids, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MessageEntity(Base):
    __tablename__ = "messages"
    
    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    citations = Column(Text, nullable=True)  # JSON with sources
    confidence_score = Column(Integer, nullable=True)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)

class MessageModel(BaseModel):
    message_id: str = None
    conversation_id: str
    role: str
    content: str
    citations: List[Dict[str, Any]] = None
    confidence_score: int = None
    created_at: datetime = None
    
    class Config:
        from_attributes = True

class ConversationModel(BaseModel):
    conversation_id: str = None
    user_id: str
    context: Dict[str, Any] = None
    messages: List[MessageModel] = []
    created_at: datetime = None
    updated_at: datetime = None
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    query: str
    context: Dict[str, Any] = None  # doc_ids, obligation_ids, etc.
