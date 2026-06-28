from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Question, ExamAttempt
from datetime import datetime
import json, os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

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

@app.route('/api/questions', methods=['GET'])
@jwt_required()
def get_questions():
    qs = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(100).all()
    result = [q.to_dict(include_answer=True) for q in qs]
    return jsonify({'questions': result, 'total': len(result)})

@app.route('/api/exam/start', methods=['POST'])
@jwt_required()
def start_exam():
    uid = get_jwt_identity()
    qs = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(5).all()
    exam = ExamAttempt(user_id=int(uid), exam_type='simulation', total_questions=len(qs))
    db.session.add(exam)
    db.session.commit()
    result = [q.to_dict(include_answer=False) for q in qs]
    return jsonify({'exam_id': exam.id, 'questions': result, 'total_questions': len(result)})

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
    pct = round((correct / exam.total_questions * 100), 2)
    exam.correct_answers = correct
    exam.score_percentage = pct
    exam.passed = pct >= 70
    exam.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'score': correct, 'total': exam.total_questions, 'percentage': pct, 'passed': exam.passed})

@app.route('/api/progress/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    uid = get_jwt_identity()
    user = db.session.get(User, int(uid))
    total = ExamAttempt.query.filter_by(user_id=int(uid)).count()
    passed = ExamAttempt.query.filter_by(user_id=int(uid), passed=True).count()
    return jsonify({'user': user.to_dict() if user else {'full_name':'User'}, 'overall_stats': {'total_exams': total, 'passed_exams': passed, 'last_score': 0}})

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
