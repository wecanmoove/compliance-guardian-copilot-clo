"""Compliance Guardian Copilot - FastAPI Application."""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid

from .config import settings
from .db import init_db, get_db
from .api import contracts, conversations

# Initialize database on startup
init_db()

# Create uploads directory
os.makedirs(settings.storage_path, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="Compliance Guardian Copilot",
    description="AI-powered compliance & contract risk intelligence",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "Compliance Guardian Copilot",
        "version": "0.1.0",
        "status": "running",
        "environment": settings.environment,
    }


@app.get("/health")
def health():
    """Health check for monitoring."""
    return {"status": "ok"}


# Include routers
app.include_router(contracts.router)
app.include_router(conversations.router)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
