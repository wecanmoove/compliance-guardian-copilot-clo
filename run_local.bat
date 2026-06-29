@echo off
echo ================================================
echo Compliance Guardian Copilot - Local Startup
echo ================================================

REM Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create .env if not exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)

REM Create uploads directory
if not exist uploads mkdir uploads

REM Initialize database
echo Initializing database...
python -c "from src.db import init_db; init_db(); print('✓ Database ready')"

REM Start server
echo.
echo Starting FastAPI server...
echo    API: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
pause
