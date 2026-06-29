from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from ..db import get_db
from ..models.conversations import (
    ConversationEntity, ConversationModel, MessageEntity, 
    MessageModel, ChatRequest
)
from ..copilot.agent import ComplianceCopilot

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

copilot = ComplianceCopilot()

@router.post("", response_model=ConversationModel)
async def create_conversation(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    conversation = ConversationEntity(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.get("/{conversation_id}", response_model=ConversationModel)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get a conversation with messages"""
    conversation = db.query(ConversationEntity).filter(
        ConversationEntity.conversation_id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageEntity).filter(
        MessageEntity.conversation_id == conversation_id
    ).order_by(MessageEntity.created_at).all()
    
    conv_model = ConversationModel.from_orm(conversation)
    conv_model.messages = [MessageModel.from_orm(m) for m in messages]
    return conv_model

@router.post("/{conversation_id}/chat", response_model=MessageModel)
async def chat(
    conversation_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get copilot response"""
    conversation = db.query(ConversationEntity).filter(
        ConversationEntity.conversation_id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Store user message
    user_msg = MessageEntity(
        conversation_id=conversation_id,
        role="user",
        content=request.query
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    
    # Get copilot response
    try:
        response = await copilot.process_query(
            query=request.query,
            context=request.context or {},
            db=db
        )
        
        # Store assistant message
        assistant_msg = MessageEntity(
            conversation_id=conversation_id,
            role="assistant",
            content=response.get("answer", ""),
            citations=json.dumps(response.get("citations", [])),
            confidence_score=response.get("confidence_score", 0)
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)
        
        return assistant_msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copilot error: {str(e)}")
