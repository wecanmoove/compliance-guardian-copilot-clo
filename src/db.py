"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .config import settings
import os

# Use SQLite for local development if PostgreSQL is not available
if "postgresql" in settings.database_url:
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_size=10,
        max_overflow=20,
    )
else:
    # Fallback to SQLite for easy local testing
    db_path = "./compliance_guardian.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=settings.debug,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from .models import (
        ContractEntity,
        RiskFindingEntity,
        ConversationEntity,
        MessageEntity,
        IncidentEntity,
    )
    
    # Create all tables
    ContractEntity.__table__.metadata.create_all(bind=engine)
    RiskFindingEntity.__table__.metadata.create_all(bind=engine)
    ConversationEntity.__table__.metadata.create_all(bind=engine)
    MessageEntity.__table__.metadata.create_all(bind=engine)
    IncidentEntity.__table__.metadata.create_all(bind=engine)
