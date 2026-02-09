@echo off
echo.
echo ================================================
echo   BIKINIS BY TELLY - Website Startup
echo ================================================
echo.
echo Starting the Bikinis By Telly e-commerce website...
echo.

cd /d "f:\her company\website"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Starting Flask server...
echo.
echo ================================================
echo   Website will be available at:
echo   http://localhost:5000
echo.
echo   Press Ctrl+C to stop the server
echo ================================================
echo.

python app.py

pause
