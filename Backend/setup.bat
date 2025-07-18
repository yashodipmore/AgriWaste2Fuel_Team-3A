@echo off
echo Setting up AgriWaste2Fuel Backend Development Environment...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete! 
echo.
echo To start development:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the server: python main.py
echo 3. Open browser: http://localhost:8000/docs
echo.
pause
