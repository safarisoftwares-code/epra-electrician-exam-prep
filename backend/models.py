from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    certification_class = db.Column(db.String(50), default="Class C")
    experience_years = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    accepted_terms = db.Column(db.Boolean, default=False)
    accepted_privacy = db.Column(db.Boolean, default=False)
    terms_accepted_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email,
                "full_name": self.full_name, "phone": self.phone,
                "certification_class": self.certification_class,
                "experience_years": self.experience_years}

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), default="medium")
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    regulation_reference = db.Column(db.String(200))
    practical_tip = db.Column(db.Text)
    calculation_steps = db.Column(db.Text)
    epra_class = db.Column(db.String(50))
    times_answered = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(100), default="Safari Softwares")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_answer=False):
        data = {"id": self.id, "category": self.category, "difficulty": self.difficulty,
                "question_text": self.question_text, "options": json.loads(self.options),
                "explanation": self.explanation, "regulation_reference": self.regulation_reference,
                "practical_tip": self.practical_tip}
        if include_answer:
            data["correct_answer"] = self.correct_answer
        return data

class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_type = db.Column(db.String(50), default="practice")
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    score_percentage = db.Column(db.Float)
    time_taken_seconds = db.Column(db.Integer)
    passed = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(50))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    total_attempted = db.Column(db.Integer, default=0)
    total_correct = db.Column(db.Integer, default=0)

class WeakArea(db.Model):
    __tablename__ = "weak_areas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    incorrect_count = db.Column(db.Integer, default=0)

class UserSession(db.Model):
    __tablename__ = "user_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
