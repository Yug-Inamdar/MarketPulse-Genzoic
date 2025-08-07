@echo off
echo ====================================
echo   MarketPulse Docker Deployment
echo ====================================

echo.
echo [1/3] Building Docker image...
docker build -t marketpulse-backend .

echo.
echo [2/3] Starting backend container...
docker run -d ^
  --name marketpulse-backend ^
  -p 8000:8000 ^
  --env-file .env ^
  marketpulse-backend

echo.
echo [3/3] Waiting for service to start...
timeout /t 5 /nobreak > nul

echo.
echo Testing backend health...
curl -f http://localhost:8000/api/v1/health
if %errorlevel% == 0 (
    echo ✅ Backend is running successfully!
    echo.
    echo 📋 Available endpoints:
    echo   Backend API: http://localhost:8000
    echo   API Docs: http://localhost:8000/docs
    echo   Health Check: http://localhost:8000/api/v1/health
    echo.
    echo 🧪 Test the API:
    echo   curl "http://localhost:8000/api/v1/market-pulse?ticker=AAPL"
) else (
    echo ❌ Backend failed to start
    echo Checking container logs...
    docker logs marketpulse-backend
)

echo.
echo 🔧 Management commands:
echo   Stop: docker stop marketpulse-backend
echo   Remove: docker rm marketpulse-backend
echo   Logs: docker logs marketpulse-backend
pause