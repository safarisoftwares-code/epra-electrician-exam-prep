# ? EPRA Electrician Exam Preparation Platform

**Developed by Safari Softwares**  
*Empowering Kenyan Electricians Since 2024*  
?? safarisoftwares@gmail.com

## ?? About
Comprehensive exam preparation platform for EPRA electrician certification exams in Kenya.

## ?? Features
- ?? Full Exam Simulation (Timed, 40 questions)
- ?? 500+ Practice Questions with explanations
- ?? Progress Tracking & Analytics
- ?? Practical Field Scenarios
- ?? Mobile Responsive Design
- ???? Kenya Power & EPRA Standards

## ??? Quick Start
`ash
pip install -r backend/requirements.txt
python backend/app.py

C:\Users\HomePC\epra-electrician-exam-prep
explorer .
dir
mkdir backend -Force
mkdir frontend -Force
mkdir frontend\css -Force
mkdir frontend\js -Force
mkdir frontend\pages -Force
mkdir legal -Force
"Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.6.0" | Out-File -FilePath backend\requirements.txt
@"
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'epra-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///epra_exam.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    COMPANY_NAME = 'Safari Softwares'
    COMPANY_EMAIL = 'safarisoftwares@gmail.com'
    COPYRIGHT_YEAR = 2026
