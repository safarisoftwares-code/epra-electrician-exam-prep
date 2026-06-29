import os
from datetime import timedelta

class Config:
    # Get the absolute path of the backend directory
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # Security keys
    SECRET_KEY = os.environ.get("SECRET_KEY", "epra-exam-prep-secret-key-2026")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "epra-jwt-secret-key-2026")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database - SQLite in instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///' + os.path.join(BASEDIR, 'instance', 'epra_exam.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Company info
    COMPANY_NAME = "Safari Softwares"
    COMPANY_EMAIL = "safarisoftwares@gmail.com"
    COPYRIGHT_YEAR = 2026
    COMPANY_PHONE = "+254700000000"
    
    # Exam settings
    EXAM_PASS_PERCENTAGE = 70
    FREE_QUESTIONS_LIMIT = 5
    PREMIUM_QUESTIONS_LIMIT = 100
    PREMIUM_PRICE_KES = 2500
    PREMIUM_DURATION_DAYS = 365