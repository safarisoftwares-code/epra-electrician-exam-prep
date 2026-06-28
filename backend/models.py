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

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan = db.Column(db.String(50), default="free")  # free, premium
    activation_key = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default="inactive")  # active, expired, inactive
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id, "plan": self.plan,
            "activation_key": self.activation_key, "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }

class ActivationKey(db.Model):
    __tablename__ = "activation_keys"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.String(50), default="premium")
    duration_days = db.Column(db.Integer, default=365)
    is_used = db.Column(db.Boolean, default=False)
    used_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by = db.Column(db.String(100), default="admin")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id, "key": self.key, "plan": self.plan,
            "duration_days": self.duration_days, "is_used": self.is_used,
            "used_by": self.used_by, "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    transaction_id = db.Column(db.String(100))
    amount = db.Column(db.Float, default=2500.00)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default="pending")  # pending, verified, rejected
    verified_by = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id, "transaction_id": self.transaction_id,
            "amount": self.amount, "phone": self.phone, "status": self.status,
            "notes": self.notes, "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default="admin")  # admin, superadmin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "full_name": self.full_name, "role": self.role}

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
