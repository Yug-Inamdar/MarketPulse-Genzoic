@echo off
echo =======================================
echo   MarketPulse Full Stack (Docker)
echo =======================================

echo.
echo [1/2] Starting backend with docker-compose...
docker-compose up -d backend

echo.
echo [2/2] Waiting for backend to be ready...
timeout /t 5 /nobreak > nul

echo.
echo Testing backend health...
curl -f http://localhost:8000/api/v1/health
if %errorlevel% == 0 (
    echo ✅ Backend is running successfully!
    echo.
    echo 📋 Services running:
    echo   Backend API: http://localhost:8000
    echo   API Documentation: http://localhost:8000/docs
    echo.
    echo 🚀 To start frontend too:
    echo   docker-compose --profile dev up -d
    echo.
    echo 🧪 Test the API:
    echo   curl "http://localhost:8000/api/v1/market-pulse?ticker=AAPL"
) else (
    echo ❌ Backend failed to start
    echo Checking logs...
    docker-compose logs backend
)

echo.
echo 🔧 Management commands:
echo   View logs: docker-compose logs backend
echo   Stop all: docker-compose down
echo   Restart: docker-compose restart backend
pause