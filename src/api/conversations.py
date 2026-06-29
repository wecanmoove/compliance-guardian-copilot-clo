"""Conversations router - Copilot chat endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..db import get_db
from ..models.conversations import ConversationEntity, MessageEntity

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.post("/")
async def create_conversation(db: Session = Depends(get_db)):
    """Create new conversation."""
    conv = ConversationEntity(
        conversation_id=str(uuid.uuid4()),
        user_id="default_user",
        tenant_id="default_tenant",
        title="New Conversation"
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"conversation_id": conv.conversation_id}


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation with messages."""
    conv = db.query(ConversationEntity).filter(
        ConversationEntity.conversation_id == conversation_id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageEntity).filter(
        MessageEntity.conversation_id == conversation_id
    ).all()
    
    return {
        "conversation_id": conv.conversation_id,
        "messages": [{"role": m.role, "content": m.content} for m in messages]
    }


@router.post("/{conversation_id}/messages")
async def send_message(conversation_id: str, message: dict, db: Session = Depends(get_db)):
    """Send message in conversation."""
    conv = db.query(ConversationEntity).filter(
        ConversationEntity.conversation_id == conversation_id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message
    user_msg = MessageEntity(
        message_id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        role="user",
        content=message.get("content", "")
    )
    db.add(user_msg)
    db.commit()
    
    # Generate bot response (simplified - just echo back)
    bot_response = f"Received: {message.get('content', '')}. (Copilot integration in progress)"
    
    bot_msg = MessageEntity(
        message_id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        role="assistant",
        content=bot_response
    )
    db.add(bot_msg)
    db.commit()
    
    return {"role": "assistant", "content": bot_response}
