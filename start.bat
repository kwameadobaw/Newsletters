@echo off
echo ========================================
echo Byte-Sized Brilliance Newsletter Website
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Starting the newsletter website...
echo.
echo Website will be available at: http://localhost:5000
echo Admin panel: http://localhost:5000/admin
echo Admin credentials: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python start.py

pause 