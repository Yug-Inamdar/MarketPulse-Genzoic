@echo off
echo =================================
echo   MarketPulse Full Stack Startup
echo =================================

echo.
echo [1/3] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Installing React dependencies...
cd frontend
call npm install

echo.
echo [3/3] Starting servers...
echo Backend will run on: http://localhost:8000
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C to stop both servers
echo.

cd ..
start "MarketPulse Backend" python run_server.py
cd frontend
start "MarketPulse Frontend" npm start

echo Both servers are starting...
echo Backend API: http://localhost:8000/docs
echo Frontend UI: http://localhost:3000
pause