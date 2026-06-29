from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from .config import settings
from .db import init_db
from .api import contracts, conversations

init_db()
os.makedirs(settings.storage_path, exist_ok=True)

app = FastAPI(title="Compliance Guardian Copilot", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "app.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(contracts.router)
app.include_router(conversations.router)
