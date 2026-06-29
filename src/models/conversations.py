from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()


class ConversationEntity(Base):
    __tablename__ = "conversations"
    
    conversation_id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    tenant_id = Column(String(36))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MessageEntity(Base):
    __tablename__ = "messages"
    
    message_id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), ForeignKey("conversations.conversation_id"))
    role = Column(String(16))  # user, assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
