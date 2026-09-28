@echo off
setlocal
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python -m PyInstaller --clean --noconfirm --onefile --windowed --name iPhoneCalculator app.py
if errorlevel 1 exit /b 1
echo Build complete: %CD%\dist\iPhoneCalculator.exe
pause
