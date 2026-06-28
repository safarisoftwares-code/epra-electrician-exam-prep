@echo off
echo =========================================
echo EPRA Exam Prep - Setup Script
echo Safari Softwares (c) 2026
echo =========================================
echo.

echo Creating directories...
mkdir backend 2>nul
mkdir frontend\css 2>nul
mkdir frontend\js 2>nul
mkdir frontend\pages 2>nul
mkdir legal 2>nul

echo Installing Python packages...
pip install Flask Flask-CORS Flask-SQLAlchemy Flask-Bcrypt Flask-JWT-Extended

echo.
echo Setup complete!
echo.
echo Next: Run 'python backend\app.py'
pause
