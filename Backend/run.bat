@echo off
echo Starting AgriWaste2Fuel Backend Server...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
python main.py
