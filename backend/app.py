from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Question, ExamAttempt, Subscription, ActivationKey, Payment, Admin
from datetime import datetime, timedelta
import json, os, random, string

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

def generate_key():
    chars = string.ascii_uppercase + string.digits
    return "EPRA-" + ''.join(random.choices(chars, k=4)) + "-" + ''.join(random.choices(chars, k=4)) + "-" + ''.join(random.choices(chars, k=4))

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def seed_admin():
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin", email="safarisoftwares@gmail.com", full_name="Safari Softwares Admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Default admin created: admin / admin123")
    else:
        print("Admin already exists")

# ============ AUTH ROUTES ============
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    user = User(username=data['username'], email=data['email'], full_name=data['full_name'],
                certification_class=data.get('certification_class', 'Class C'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'user': user.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'user': user.to_dict()}), 200

# ============ QUESTIONS ============
@app.route('/api/questions', methods=['GET'])
@jwt_required()
def get_questions():
    qs = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(100).all()
    return jsonify({'questions': [q.to_dict(include_answer=True) for q in qs], 'total': len(qs)})

# ============ EXAM ============
@app.route('/api/exam/start', methods=['POST'])
@jwt_required()
def start_exam():
    uid = get_jwt_identity()
    qs = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(5).all()
    exam = ExamAttempt(user_id=int(uid), exam_type='simulation', total_questions=len(qs))
    db.session.add(exam)
    db.session.commit()
    return jsonify({'exam_id': exam.id, 'questions': [q.to_dict(include_answer=False) for q in qs], 'total_questions': len(qs)})

@app.route('/api/exam/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    data = request.get_json()
    exam = ExamAttempt.query.get(data['exam_id'])
    answers = data.get('answers', {})
    correct = 0
    for qid, ans in answers.items():
        q = Question.query.get(int(qid))
        if q and ans == q.correct_answer:
            correct += 1
    pct = round((correct / exam.total_questions * 100), 2) if exam.total_questions > 0 else 0
    exam.correct_answers = correct
    exam.score_percentage = pct
    exam.passed = pct >= 70
    exam.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'score': correct, 'total': exam.total_questions, 'percentage': pct, 'passed': exam.passed})

# ============ DASHBOARD ============
@app.route('/api/progress/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    uid = get_jwt_identity()
    user = db.session.get(User, int(uid))
    total = ExamAttempt.query.filter_by(user_id=int(uid)).count()
    passed = ExamAttempt.query.filter_by(user_id=int(uid), passed=True).count()
    return jsonify({'user': user.to_dict() if user else {'full_name': 'User'}, 'overall_stats': {'total_exams': total, 'passed_exams': passed, 'last_score': 0}})

# ============ PREMIUM ============
@app.route('/api/activate', methods=['POST'])
@jwt_required()
def activate_premium():
    data = request.get_json()
    uid = get_jwt_identity()
    key = ActivationKey.query.filter_by(key=data.get('key'), is_used=False).first()
    if not key:
        return jsonify({'error': 'Invalid or already used key'}), 400
    if key.password != data.get('password'):
        return jsonify({'error': 'Invalid password'}), 400
    key.is_used = True
    key.used_by = int(uid)
    key.used_at = datetime.utcnow()
    sub = Subscription(user_id=int(uid), plan='premium', activation_key=key.key, status='active',
                       start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=key.duration_days))
    db.session.add(sub)
    db.session.commit()
    return jsonify({'message': 'Premium activated!', 'subscription': sub.to_dict()})

@app.route('/api/premium/status', methods=['GET'])
@jwt_required()
def premium_status():
    uid = get_jwt_identity()
    sub = Subscription.query.filter_by(user_id=int(uid), status='active').first()
    is_premium = sub is not None and sub.end_date > datetime.utcnow()
    return jsonify({'is_premium': is_premium, 'plan': sub.plan if sub else 'free', 'expires': sub.end_date.isoformat() if sub else None})

@app.route('/api/payment/submit', methods=['POST'])
@jwt_required()
def submit_payment():
    data = request.get_json()
    uid = get_jwt_identity()
    payment = Payment(user_id=int(uid), transaction_id=data.get('transaction_id', ''), phone=data.get('phone', ''), notes=data.get('notes', ''))
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment submitted', 'payment': payment.to_dict()})

# ============ ADMIN ROUTES ============
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data.get('username')).first()
    if not admin or not admin.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity='admin_'+str(admin.id))
    return jsonify({'access_token': token, 'admin': admin.to_dict()})

@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    total_users = User.query.count()
    premium_users = Subscription.query.filter_by(status='active').count()
    pending_payments = Payment.query.filter_by(status='pending').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='verified').scalar() or 0
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    keys_available = ActivationKey.query.filter_by(is_used=False).count()
    return jsonify({'stats': {'total_users': total_users, 'premium_users': premium_users, 'pending_payments': pending_payments, 'total_revenue': total_revenue, 'keys_available': keys_available}, 'recent_payments': [p.to_dict() for p in recent_payments]})

@app.route('/api/admin/generate-key', methods=['POST'])
@jwt_required()
def generate_activation_key():
    data = request.get_json()
    count = data.get('count', 1)
    duration = data.get('duration_days', 365)
    keys = []
    for _ in range(count):
        key = ActivationKey(key=generate_key(), password=generate_password(), duration_days=duration)
        db.session.add(key)
        keys.append({'key': key.key, 'password': key.password})
    db.session.commit()
    return jsonify({'keys': keys})

@app.route('/api/admin/keys', methods=['GET'])
@jwt_required()
def view_keys():
    keys = ActivationKey.query.order_by(ActivationKey.created_at.desc()).limit(50).all()
    return jsonify([k.to_dict() for k in keys])

@app.route('/api/admin/payments', methods=['GET'])
@jwt_required()
def view_payments():
    status = request.args.get('status', 'all')
    query = Payment.query
    if status != 'all':
        query = query.filter_by(status=status)
    payments = query.order_by(Payment.created_at.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in payments])

@app.route('/api/admin/verify-payment', methods=['POST'])
@jwt_required()
def verify_payment():
    data = request.get_json()
    payment = Payment.query.get(data['payment_id'])
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    payment.status = 'verified'
    payment.verified_by = data.get('verified_by', 'admin')
    payment.verified_at = datetime.utcnow()
    key_str = generate_key()
    password = generate_password()
    key = ActivationKey(key=key_str, password=password, is_used=True, used_by=payment.user_id, used_at=datetime.utcnow())
    db.session.add(key)
    sub = Subscription(user_id=payment.user_id, plan='premium', activation_key=key_str, status='active',
                       start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=365))
    db.session.add(sub)
    db.session.commit()
    return jsonify({'message': 'Payment verified!', 'activation_key': key_str, 'password': password, 'subscription': sub.to_dict()})

@app.route('/api/admin/subscribers', methods=['GET'])
@jwt_required()
def view_subscribers():
    subs = db.session.query(Subscription, User).join(User, Subscription.user_id == User.id).order_by(Subscription.created_at.desc()).limit(50).all()
    result = []
    for sub, user in subs:
        item = sub.to_dict()
        item['user'] = user.to_dict()
        result.append(item)
    return jsonify(result)

@app.route('/api/admin/profile', methods=['GET', 'PUT'])
@jwt_required()
def admin_profile():
    uid = get_jwt_identity().replace('admin_', '')
    admin = db.session.get(Admin, int(uid))
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404
    if request.method == 'GET':
        return jsonify(admin.to_dict())
    data = request.get_json()
    if data.get('username'):
        admin.username = data['username']
    if data.get('email'):
        admin.email = data['email']
    if data.get('full_name'):
        admin.full_name = data['full_name']
    db.session.commit()
    return jsonify({'message': 'Profile updated', 'admin': admin.to_dict()})

@app.route('/api/admin/change-password', methods=['POST'])
@jwt_required()
def admin_change_password():
    uid = get_jwt_identity().replace('admin_', '')
    admin = db.session.get(Admin, int(uid))
    if not admin or not admin.check_password(request.get_json().get('current_password')):
        return jsonify({'error': 'Invalid current password'}), 400
    admin.set_password(request.get_json().get('new_password'))
    db.session.commit()
    return jsonify({'message': 'Password changed!'})

# ============ STATIC FILES ============
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/terms')
def terms():
    return send_from_directory('../legal', 'terms-of-use.html')

@app.route('/privacy')
def privacy():
    return send_from_directory('../legal', 'privacy-policy.html')

@app.route('/copyright')
def copyright():
    return send_from_directory('../legal', 'copyright.html')

@app.route('/<path:path>')
def static_files(path):
    p = os.path.join('../frontend', path)
    if os.path.exists(p):
        return send_from_directory('../frontend', path)
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)