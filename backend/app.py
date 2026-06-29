import sys
import os

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from config import Config
from models import db, bcrypt, User, Question, ExamAttempt, Subscription, ActivationKey, Payment, Admin
from datetime import datetime, timedelta
import json
import random
import string

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Create instance directory if it doesn't exist
instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_dir, exist_ok=True)

# Create all database tables
with app.app_context():
    db.create_all()

# Helper functions
def generate_key():
    """Generate activation key format: EPRA-XXXX-XXXX-XXXX"""
    chars = string.ascii_uppercase + string.digits
    return "EPRA-" + '-'.join([
        ''.join(random.choices(chars, k=4)),
        ''.join(random.choices(chars, k=4)),
        ''.join(random.choices(chars, k=4))
    ])

def generate_password():
    """Generate 12-character random password"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def is_premium_user(user_id):
    """Check if user has active premium subscription"""
    sub = Subscription.query.filter_by(
        user_id=user_id,
        status='active'
    ).first()
    return sub is not None and sub.end_date > datetime.utcnow()

# ==============================
# STUDENT AUTHENTICATION ROUTES
# ==============================

@app.route('/api/auth/register', methods=['POST'])
def student_register():
    """Register a new student"""
    try:
        data = request.get_json()
        
        required_fields = ['username', 'email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone', ''),
            certification_class=data.get('certification_class', 'Class C'),
            experience_years=data.get('experience_years', 0)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=f"user_{user.id}")
        
        return jsonify({
            'access_token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def student_login():
    """Student login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        token = create_access_token(identity=f"user_{user.id}")
        
        return jsonify({
            'access_token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# STUDENT DASHBOARD ROUTES
# ==============================

@app.route('/api/student/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    """Get student dashboard data"""
    try:
        identity = get_jwt_identity()
        
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        user = db.session.get(User, user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        total_exams = ExamAttempt.query.filter_by(user_id=user_id).count()
        passed_exams = ExamAttempt.query.filter_by(user_id=user_id, passed=True).count()
        
        recent_exams = ExamAttempt.query.filter_by(user_id=user_id)\
            .order_by(ExamAttempt.started_at.desc()).limit(5).all()
        
        exam_history = [exam.to_dict() for exam in recent_exams]
        
        subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        premium_status = {
            'is_premium': False,
            'plan': 'free',
            'expires': None,
            'days_remaining': 0
        }
        
        if subscription and subscription.end_date > datetime.utcnow():
            days_remaining = (subscription.end_date - datetime.utcnow()).days
            premium_status = {
                'is_premium': True,
                'plan': subscription.plan,
                'expires': subscription.end_date.isoformat(),
                'days_remaining': max(0, days_remaining)
            }
        
        average_score = 0
        if total_exams > 0:
            all_scores = ExamAttempt.query.filter_by(user_id=user_id).all()
            average_score = round(sum(exam.score_percentage for exam in all_scores) / total_exams, 2)
        
        return jsonify({
            'user': user.to_dict(),
            'stats': {
                'total_exams': total_exams,
                'passed_exams': passed_exams,
                'average_score': average_score,
                'pass_rate': round((passed_exams / total_exams * 100), 2) if total_exams > 0 else 0
            },
            'premium': premium_status,
            'recent_exams': exam_history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# EXAM ROUTES
# ==============================

@app.route('/api/exam/questions', methods=['GET'])
@jwt_required()
def get_exam_questions():
    """Get questions for exam"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        premium = is_premium_user(user_id)
        
        limit = 100 if premium else 5
        
        questions = Question.query.filter_by(is_active=True)\
            .order_by(db.func.random()).limit(limit).all()
        
        return jsonify({
            'questions': [q.to_dict(include_answer=False) for q in questions],
            'total': len(questions),
            'is_premium': premium
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exam/start', methods=['POST'])
@jwt_required()
def start_exam():
    """Start a new exam session"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        premium = is_premium_user(user_id)
        
        limit = 100 if premium else 5
        questions = Question.query.filter_by(is_active=True)\
            .order_by(db.func.random()).limit(limit).all()
        
        if not questions:
            return jsonify({'error': 'No questions available'}), 404
        
        exam = ExamAttempt(
            user_id=user_id,
            exam_type='practice',
            total_questions=len(questions),
            questions_data=json.dumps([q.id for q in questions])
        )
        db.session.add(exam)
        db.session.commit()
        
        return jsonify({
            'exam_id': exam.id,
            'questions': [q.to_dict(include_answer=False) for q in questions],
            'total_questions': len(questions),
            'is_premium': premium
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exam/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    """Submit exam answers"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        data = request.get_json()
        
        exam = ExamAttempt.query.get(data.get('exam_id'))
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if exam.completed_at:
            return jsonify({'error': 'Exam already submitted'}), 400
        
        answers = data.get('answers', {})
        correct_count = 0
        
        for question_id, answer in answers.items():
            question = Question.query.get(int(question_id))
            if question and answer == question.correct_answer:
                correct_count += 1
                question.times_correct += 1
            if question:
                question.times_answered += 1
        
        percentage = round((correct_count / exam.total_questions * 100), 2) if exam.total_questions > 0 else 0
        
        exam.correct_answers = correct_count
        exam.score_percentage = percentage
        exam.passed = percentage >= 70
        exam.answers_given = json.dumps(answers)
        exam.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'exam_id': exam.id,
            'score': correct_count,
            'total': exam.total_questions,
            'percentage': percentage,
            'passed': exam.passed,
            'message': 'Congratulations! You passed!' if exam.passed else 'Keep practicing! You need 70% to pass.'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exam/review/<int:exam_id>', methods=['GET'])
@jwt_required()
def review_exam(exam_id):
    """Get detailed exam review with marking scheme"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        exam = ExamAttempt.query.get(exam_id)
        
        if not exam:
            return jsonify({'error': 'Exam not found'}), 404
        
        if exam.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        question_ids = json.loads(exam.questions_data) if exam.questions_data else []
        answers_given = json.loads(exam.answers_given) if exam.answers_given else {}
        
        questions_review = []
        for qid in question_ids:
            question = Question.query.get(qid)
            if question:
                user_answer = answers_given.get(str(qid), 'Not answered')
                is_correct = user_answer == question.correct_answer
                
                questions_review.append({
                    'id': question.id,
                    'question_text': question.question_text,
                    'options': json.loads(question.options) if isinstance(question.options, str) else question.options,
                    'correct_answer': question.correct_answer,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'explanation': question.explanation,
                    'regulation_reference': question.regulation_reference,
                    'practical_tip': question.practical_tip,
                    'category': question.category,
                    'difficulty': question.difficulty
                })
        
        return jsonify({
            'exam': exam.to_dict(),
            'questions': questions_review,
            'total_questions': len(questions_review),
            'answered_questions': len([q for q in questions_review if q['user_answer'] != 'Not answered'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exam/history', methods=['GET'])
@jwt_required()
def exam_history():
    """Get student exam history"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        
        exams = ExamAttempt.query.filter_by(user_id=user_id)\
            .order_by(ExamAttempt.started_at.desc()).limit(20).all()
        
        return jsonify({
            'exams': [exam.to_dict() for exam in exams]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exam/history/clear', methods=['DELETE'])
@jwt_required()
def clear_exam_history():
    """Clear all exam history for the student"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        
        deleted = ExamAttempt.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully cleared {deleted} exam records',
            'deleted_count': deleted
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# STUDY MODE ROUTES
# ==============================

@app.route('/api/study/questions', methods=['GET'])
@jwt_required()
def get_study_questions():
    """Get questions for study mode (with answers)"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        premium = is_premium_user(user_id)
        
        limit = 100 if premium else 5
        
        questions = Question.query.filter_by(is_active=True)\
            .order_by(db.func.random()).limit(limit).all()
        
        return jsonify({
            'questions': [q.to_dict(include_answer=True) for q in questions],
            'total': len(questions),
            'is_premium': premium
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# PREMIUM/UPGRADE ROUTES
# ==============================

@app.route('/api/premium/activate', methods=['POST'])
@jwt_required()
def activate_premium():
    """Activate premium using key and password"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        data = request.get_json()
        
        key = data.get('key', '').strip()
        password = data.get('password', '').strip()
        
        if not key or not password:
            return jsonify({'error': 'Key and password are required'}), 400
        
        activation_key = ActivationKey.query.filter_by(key=key, is_used=False).first()
        
        if not activation_key:
            return jsonify({'error': 'Invalid or already used activation key'}), 400
        
        if activation_key.password != password:
            return jsonify({'error': 'Invalid password for this key'}), 400
        
        existing_sub = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if existing_sub and existing_sub.end_date > datetime.utcnow():
            return jsonify({'error': 'You already have an active premium subscription'}), 400
        
        activation_key.is_used = True
        activation_key.used_by = user_id
        activation_key.used_at = datetime.utcnow()
        
        if existing_sub:
            existing_sub.status = 'expired'
        
        subscription = Subscription(
            user_id=user_id,
            plan='premium',
            activation_key=key,
            status='active',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=activation_key.duration_days)
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'message': 'Premium activated successfully!',
            'subscription': subscription.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/premium/status', methods=['GET'])
@jwt_required()
def premium_status():
    """Check premium status"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        subscription = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        is_premium = subscription is not None and subscription.end_date > datetime.utcnow()
        
        if is_premium:
            days_remaining = (subscription.end_date - datetime.utcnow()).days
            return jsonify({
                'is_premium': True,
                'plan': subscription.plan,
                'expires': subscription.end_date.isoformat(),
                'days_remaining': max(0, days_remaining),
                'activated_on': subscription.start_date.isoformat() if subscription.start_date else None
            }), 200
        else:
            return jsonify({
                'is_premium': False,
                'plan': 'free',
                'expires': None,
                'days_remaining': 0
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/premium/payment', methods=['POST'])
@jwt_required()
def submit_payment():
    """Submit payment for premium"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('user_'):
            return jsonify({'error': 'Invalid token type'}), 403
        
        user_id = int(identity.replace('user_', ''))
        data = request.get_json()
        
        transaction_id = data.get('transaction_id', '')
        phone = data.get('phone', '')
        
        if not transaction_id:
            return jsonify({'error': 'M-Pesa transaction ID is required'}), 400
        
        existing = Payment.query.filter_by(transaction_id=transaction_id).first()
        if existing:
            return jsonify({'error': 'This transaction has already been submitted'}), 400
        
        payment = Payment(
            user_id=user_id,
            transaction_id=transaction_id,
            phone=phone,
            amount=data.get('amount', 2500.00),
            payment_method=data.get('payment_method', 'mpesa'),
            notes=data.get('notes', '')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment submitted successfully! Awaiting verification.',
            'payment': payment.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN AUTHENTICATION ROUTES
# ==============================

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        admin = Admin.query.filter_by(username=data['username']).first()
        
        if not admin or not admin.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not admin.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        token = create_access_token(identity=f"admin_{admin.id}")
        
        return jsonify({
            'access_token': token,
            'admin': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN DASHBOARD ROUTES
# ==============================

@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Get admin dashboard statistics"""
    try:
        identity = get_jwt_identity()
        
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        premium_users = Subscription.query.filter_by(status='active').filter(
            Subscription.end_date > datetime.utcnow()
        ).count()
        
        pending_payments = Payment.query.filter_by(status='pending').count()
        verified_payments = Payment.query.filter_by(status='verified').count()
        
        total_revenue = db.session.query(db.func.sum(Payment.amount))\
            .filter_by(status='verified').scalar() or 0
        
        total_questions = Question.query.count()
        active_questions = Question.query.filter_by(is_active=True).count()
        
        available_keys = ActivationKey.query.filter_by(is_used=False).count()
        used_keys = ActivationKey.query.filter_by(is_used=True).count()
        
        total_exams = ExamAttempt.query.count()
        
        recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'premium_users': premium_users,
                'pending_payments': pending_payments,
                'verified_payments': verified_payments,
                'total_revenue': total_revenue,
                'total_questions': total_questions,
                'active_questions': active_questions,
                'available_keys': available_keys,
                'used_keys': used_keys,
                'total_exams': total_exams
            },
            'recent_payments': [p.to_dict() for p in recent_payments],
            'recent_users': [u.to_dict() for u in recent_users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN KEY MANAGEMENT ROUTES
# ==============================

@app.route('/api/admin/keys/generate', methods=['POST'])
@jwt_required()
def admin_generate_keys():
    """Generate activation keys"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        admin_id = int(identity.replace('admin_', ''))
        data = request.get_json()
        
        count = min(data.get('count', 1), 100)
        duration_days = data.get('duration_days', 365)
        
        generated_keys = []
        for _ in range(count):
            key = ActivationKey(
                key=generate_key(),
                password=generate_password(),
                duration_days=duration_days,
                created_by=admin_id
            )
            db.session.add(key)
            generated_keys.append({
                'key': key.key,
                'password': key.password
            })
        
        db.session.commit()
        
        return jsonify({
            'message': f'{count} key(s) generated successfully',
            'keys': generated_keys
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/keys', methods=['GET'])
@jwt_required()
def admin_view_keys():
    """View all activation keys"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        status_filter = request.args.get('status', 'all')
        
        query = ActivationKey.query
        
        if status_filter == 'available':
            query = query.filter_by(is_used=False)
        elif status_filter == 'used':
            query = query.filter_by(is_used=True)
        
        keys = query.order_by(ActivationKey.created_at.desc()).limit(100).all()
        
        return jsonify([k.to_dict() for k in keys]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/keys/deactivate', methods=['POST'])
@jwt_required()
def admin_deactivate_key():
    """Deactivate an activation key"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        key = ActivationKey.query.filter_by(key=data.get('key')).first()
        
        if not key:
            return jsonify({'error': 'Key not found'}), 404
        
        key.is_used = True
        
        sub = Subscription.query.filter_by(activation_key=key.key, status='active').first()
        if sub:
            sub.status = 'expired'
        
        db.session.commit()
        
        return jsonify({'message': 'Key deactivated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN PAYMENT MANAGEMENT ROUTES
# ==============================

@app.route('/api/admin/payments', methods=['GET'])
@jwt_required()
def admin_view_payments():
    """View all payments"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        status_filter = request.args.get('status', 'all')
        
        query = Payment.query
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        payments = query.order_by(Payment.created_at.desc()).limit(100).all()
        
        return jsonify([p.to_dict() for p in payments]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/payments/verify', methods=['POST'])
@jwt_required()
def admin_verify_payment():
    """Verify a payment and generate activation key"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        admin_id = int(identity.replace('admin_', ''))
        data = request.get_json()
        
        payment = Payment.query.get(data.get('payment_id'))
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        if payment.status != 'pending':
            return jsonify({'error': 'Payment is not pending'}), 400
        
        payment.status = 'verified'
        payment.verified_by = admin_id
        payment.verified_at = datetime.utcnow()
        
        new_key = generate_key()
        new_password = generate_password()
        
        activation_key = ActivationKey(
            key=new_key,
            password=new_password,
            is_used=True,
            used_by=payment.user_id,
            used_at=datetime.utcnow(),
            created_by=admin_id
        )
        db.session.add(activation_key)
        
        subscription = Subscription(
            user_id=payment.user_id,
            plan='premium',
            activation_key=new_key,
            status='active',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=365)
        )
        db.session.add(subscription)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment verified successfully',
            'activation_key': new_key,
            'password': new_password,
            'payment': payment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN USER/SUBSCRIBER MANAGEMENT
# ==============================

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def admin_view_users():
    """View all users"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        users = User.query.order_by(User.created_at.desc()).limit(100).all()
        
        return jsonify([u.to_dict() for u in users]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/subscribers', methods=['GET'])
@jwt_required()
def admin_view_subscribers():
    """View all premium subscribers"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        subscribers = db.session.query(Subscription, User)\
            .join(User, Subscription.user_id == User.id)\
            .order_by(Subscription.created_at.desc()).limit(100).all()
        
        result = []
        for sub, user in subscribers:
            item = sub.to_dict()
            item['user'] = user.to_dict()
            result.append(item)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# ADMIN PROFILE/SETTINGS ROUTES
# ==============================

@app.route('/api/admin/profile', methods=['GET'])
@jwt_required()
def admin_profile():
    """Get admin profile"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        admin_id = int(identity.replace('admin_', ''))
        admin = db.session.get(Admin, admin_id)
        
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        return jsonify(admin.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/change-password', methods=['POST'])
@jwt_required()
def admin_change_password():
    """Change admin password"""
    try:
        identity = get_jwt_identity()
        if not identity.startswith('admin_'):
            return jsonify({'error': 'Admin access required'}), 403
        
        admin_id = int(identity.replace('admin_', ''))
        admin = db.session.get(Admin, admin_id)
        
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        data = request.get_json()
        
        if not admin.check_password(data.get('current_password')):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        admin.set_password(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==============================
# STATIC FILE SERVING
# ==============================

@app.route('/favicon.ico')
def favicon():
    """Serve favicon - returns empty response"""
    return '', 204

@app.route('/')
def serve_index():
    """Serve main index page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    if '?' in path:
        path = path.split('?')[0]
    
    full_path = os.path.join(app.static_folder, path)
    
    if os.path.isfile(full_path):
        return send_from_directory(app.static_folder, path)
    
    if not path.endswith('.html'):
        html_path = path + '.html'
        full_html_path = os.path.join(app.static_folder, html_path)
        if os.path.isfile(full_html_path):
            return send_from_directory(app.static_folder, html_path)
    
    return send_from_directory(app.static_folder, 'index.html')

# ==============================
# APPLICATION STARTUP
# ==============================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)