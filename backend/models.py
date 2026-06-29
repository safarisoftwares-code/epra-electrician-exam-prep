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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    exam_attempts = db.relationship('ExamAttempt', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_premium(self):
        active_sub = Subscription.query.filter_by(
            user_id=self.id, 
            status='active'
        ).first()
        if active_sub and active_sub.end_date > datetime.utcnow():
            return True
        return False
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "certification_class": self.certification_class,
            "experience_years": self.experience_years,
            "is_premium": self.is_premium(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Question(db.Model):
    __tablename__ = "questions"
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), default="medium")
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)  # JSON string
    correct_answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    regulation_reference = db.Column(db.String(200))
    practical_tip = db.Column(db.Text)
    calculation_steps = db.Column(db.Text)
    epra_class = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    times_answered = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(100), default="Safari Softwares")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_answer=False):
        data = {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question_text": self.question_text,
            "options": json.loads(self.options) if isinstance(self.options, str) else self.options,
            "explanation": self.explanation,
            "regulation_reference": self.regulation_reference,
            "practical_tip": self.practical_tip,
            "calculation_steps": self.calculation_steps,
            "epra_class": self.epra_class,
            "image_url": self.image_url
        }
        if include_answer:
            data["correct_answer"] = self.correct_answer
        return data

class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_type = db.Column(db.String(50), default="practice")  # practice, simulation
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    score_percentage = db.Column(db.Float, default=0.0)
    time_taken_seconds = db.Column(db.Integer)
    passed = db.Column(db.Boolean, default=False)
    questions_data = db.Column(db.Text)  # JSON string of questions
    answers_given = db.Column(db.Text)    # JSON string of answers
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "exam_type": self.exam_type,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "score_percentage": self.score_percentage,
            "time_taken_seconds": self.time_taken_seconds,
            "passed": self.passed,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan = db.Column(db.String(50), default="free")  # free, premium
    activation_key = db.Column(db.String(100))
    status = db.Column(db.String(20), default="active")  # active, expired, cancelled
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan": self.plan,
            "activation_key": self.activation_key,
            "status": self.status,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.status == 'active' and self.end_date > datetime.utcnow()
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
    created_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "password": self.password if not self.is_used else "••••••",
            "plan": self.plan,
            "duration_days": self.duration_days,
            "is_used": self.is_used,
            "used_by": self.used_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "used_at": self.used_at.isoformat() if self.used_at else None
        }

class Payment(db.Model):
    __tablename__ = "payments"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    transaction_id = db.Column(db.String(100))
    amount = db.Column(db.Float, default=2500.00)
    phone = db.Column(db.String(20))
    payment_method = db.Column(db.String(50), default="mpesa")
    status = db.Column(db.String(20), default="pending")  # pending, verified, rejected
    verified_by = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "phone": self.phone,
            "payment_method": self.payment_method,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None
        }

class Admin(db.Model):
    __tablename__ = "admins"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(50), default="admin")  # admin, superadmin
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }