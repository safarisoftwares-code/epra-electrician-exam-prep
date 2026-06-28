import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "epra-secret-2026")
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/HomePC/epra-electrician-exam-prep/backend/instance/epra_exam.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-2026")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    COMPANY_NAME = "Safari Softwares"
    COMPANY_EMAIL = "safarisoftwares@gmail.com"
    COPYRIGHT_YEAR = 2026
