import os

# Create all directories
dirs = ['backend', 'frontend/css', 'frontend/js', 'frontend/pages', 'legal', 'logs']
for d in dirs:
    os.makedirs(d, exist_ok=True)

# backend/config.py
with open('backend/config.py', 'w') as f:
    f.write('''import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "epra-secret-2026")
    SQLALCHEMY_DATABASE_URI = "sqlite:///epra_exam.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-2026")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    COMPANY_NAME = "Safari Softwares"
    COMPANY_EMAIL = "safarisoftwares@gmail.com"
    COPYRIGHT_YEAR = 2026
''')

# backend/models.py
with open('backend/models.py', 'w') as f:
    f.write('''from flask_sqlalchemy import SQLAlchemy
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
''')

# backend/app.py
with open('backend/app.py', 'w') as f:
    f.write('''from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Question, ExamAttempt, UserProgress, WeakArea
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.config.from_object(Config)
CORS(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400
        if not data.get("accepted_terms") or not data.get("accepted_privacy"):
            return jsonify({"error": "Must accept Terms and Privacy Policy"}), 400
        user = User(username=data["username"], email=data["email"], full_name=data["full_name"],
                    phone=data.get("phone", ""), certification_class=data.get("certification_class", "Class C"),
                    experience_years=data.get("experience_years", 0), accepted_terms=True,
                    accepted_privacy=True, terms_accepted_date=datetime.utcnow())
        user.set_password(data["password"])
        db.session.add(user); db.session.commit()
        token = create_access_token(identity=user.id)
        return jsonify({"message": "Registered!", "access_token": token, "user": user.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401
        user.last_login = datetime.utcnow(); db.session.commit()
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token, "user": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/profile", methods=["GET"])
@jwt_required()
def profile():
    return jsonify(User.query.get(get_jwt_identity()).to_dict())

@app.route("/api/exam/start", methods=["POST"])
@jwt_required()
def start_exam():
    try:
        data = request.get_json()
        total = data.get("total_questions", 10)
        questions = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(total).all()
        if len(questions) == 0:
            return jsonify({"error": "No questions in database. Run seed_data.py first!"}), 400
        exam = ExamAttempt(user_id=get_jwt_identity(), exam_type="simulation", total_questions=len(questions),
                          ip_address=request.remote_addr, started_at=datetime.utcnow())
        db.session.add(exam); db.session.commit()
        return jsonify({"exam_id": exam.id, "questions": [q.to_dict() for q in questions],
                       "total_questions": len(questions), "time_limit_seconds": 3600, "pass_percentage": 70}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/exam/submit", methods=["POST"])
@jwt_required()
def submit_exam():
    try:
        data = request.get_json()
        exam = ExamAttempt.query.get(data["exam_id"])
        if not exam or exam.user_id != get_jwt_identity():
            return jsonify({"error": "Invalid exam"}), 400
        correct = 0
        answers = data.get("answers", {})
        for qid, ans in answers.items():
            q = Question.query.get(int(qid))
            if q:
                is_correct = (ans == q.correct_answer)
                if is_correct: correct += 1
                q.times_answered += 1
                if is_correct: q.times_correct += 1
        pct = round((correct / exam.total_questions * 100), 2)
        exam.correct_answers = correct
        exam.score_percentage = pct
        exam.time_taken_seconds = data.get("time_taken", 0)
        exam.passed = pct >= 70
        exam.completed_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"score": correct, "total": exam.total_questions, "percentage": pct, "passed": exam.passed}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/questions", methods=["GET"])
@jwt_required()
def get_questions():
    limit = request.args.get("limit", 20, type=int)
    include = request.args.get("include_answer", "true").lower() == "true"
    qs = Question.query.filter_by(is_active=True).order_by(db.func.random()).limit(limit).all()
    return jsonify({"questions": [q.to_dict(include_answer=include) for q in qs], "total": len(qs)})

@app.route("/api/progress/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    total = ExamAttempt.query.filter_by(user_id=uid).count()
    passed = ExamAttempt.query.filter_by(user_id=uid, passed=True).count()
    last = ExamAttempt.query.filter_by(user_id=uid).order_by(ExamAttempt.completed_at.desc()).first()
    return jsonify({"user": user.to_dict(), "overall_stats": {"total_exams": total,
                   "passed_exams": passed, "last_score": last.score_percentage if last else 0}})

@app.route("/terms")
def terms(): return send_from_directory("../legal", "terms-of-use.html")
@app.route("/privacy")
def privacy(): return send_from_directory("../legal", "privacy-policy.html")
@app.route("/copyright")
def copyright(): return send_from_directory("../legal", "copyright.html")
@app.route("/")
def index(): return send_from_directory("../frontend", "index.html")
@app.route("/<path:path>")
def static_files(path):
    p = os.path.join("../frontend", path)
    return send_from_directory("../frontend", path) if os.path.exists(p) else send_from_directory("../frontend", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
''')

# backend/seed_data.py
with open('backend/seed_data.py', 'w') as f:
    f.write('''from app import app, db
from models import Question
import json

questions = [
    {"category":"safety","difficulty":"medium","question_text":"Minimum IP rating for bathroom zone 1?","options":json.dumps(["IPX4","IPX5","IPX7","IP44"]),"correct_answer":"IPX4","explanation":"Zone 1 needs IPX4. Zone 0 needs IPX7.","regulation_reference":"BS 7671 Section 701","practical_tip":"Check the bathroom zone chart before installing!","epra_class":"Class C"},
    {"category":"safety","difficulty":"hard","question_text":"Max disconnection time for 230V final circuit <=32A on TN system?","options":json.dumps(["0.4s","5s","0.2s","1s"]),"correct_answer":"0.4s","explanation":"0.4 seconds for final circuits <=32A on TN.","regulation_reference":"BS 7671 Table 41.1","practical_tip":"Test RCDs with proper tester, not just the button!","epra_class":"Class C"},
    {"category":"installation","difficulty":"easy","question_text":"Minimum bending radius for PVC cables?","options":json.dumps(["4x dia","6x dia","8x dia","10x dia"]),"correct_answer":"6x dia","explanation":"PVC cables need 6x diameter bend radius.","regulation_reference":"BS 7671 522.8.3","practical_tip":"If tighter than your fist, it's too sharp!","epra_class":"Class C"},
    {"category":"calculations","difficulty":"hard","question_text":"Voltage drop: 2.5mm2 cable, 20A, 30m (mV/A/m=18)?","options":json.dumps(["10.8V","8.6V","12.4V","5.4V"]),"correct_answer":"10.8V","explanation":"Vd=(18x20x30)/1000=10.8V (4.5%)","regulation_reference":"BS 7671 App 4","calculation_steps":json.dumps(["Vd=(mV/A/m x I x L)/1000","=(18x20x30)/1000","=10.8V"]),"practical_tip":"Use the formula for accuracy!","epra_class":"Class C"},
    {"category":"testing","difficulty":"medium","question_text":"Correct initial verification test sequence?","options":json.dumps(["Continuity,IR,Polarity,EFLI,RCD","IR,Cont,RCD,Pol,EFLI","Pol,Cont,EFLI,IR,RCD","RCD,EFLI,Cont,IR,Pol"]),"correct_answer":"Continuity,IR,Polarity,EFLI,RCD","explanation":"CIPELR: First 3 DEAD, last 2 LIVE.","regulation_reference":"BS 7671 Part 6","practical_tip":"CIPELR = Continuity, Insulation, Polarity, Earth Loop, RCD!","epra_class":"Class C"},
    {"category":"kenya_power","difficulty":"easy","question_text":"Standard single-phase voltage from Kenya Power?","options":json.dumps(["240V","230V","220V","250V"]),"correct_answer":"240V","explanation":"Kenya Power: 240V/415V, 50Hz.","regulation_reference":"Kenya Power Standard","practical_tip":"Always measure on site - can be 220-250V!","epra_class":"Class C"},
    {"category":"earthing","difficulty":"hard","question_text":"Max Zs for 32A Type B MCB on TN at 230V?","options":json.dumps(["1.44ohm","1.15ohm","0.72ohm","2.30ohm"]),"correct_answer":"1.44ohm","explanation":"Zs=230/(32x5)=1.44ohm (design:1.15ohm)","regulation_reference":"BS 7671 Table 41.3","practical_tip":">1.15ohm on 32A? Investigate connections!","epra_class":"Class C"},
    {"category":"safety","difficulty":"medium","question_text":"RCD rating for socket-outlet protection?","options":json.dumps(["30mA","100mA","300mA","10mA"]),"correct_answer":"30mA","explanation":"30mA protects people. 100mA for fire, 300mA for equipment.","regulation_reference":"BS 7671 411.3.3","practical_tip":"30mA = Life Safety!","epra_class":"Class C"},
    {"category":"regulations","difficulty":"easy","question_text":"Certificate for new installations in Kenya?","options":json.dumps(["Completion Certificate","EPRA License","KP Form","Local Permit"]),"correct_answer":"Completion Certificate","explanation":"Required before Kenya Power connects supply.","regulation_reference":"Energy Act 2019","practical_tip":"Never energize without this certificate!","epra_class":"Class C"},
    {"category":"safety","difficulty":"easy","question_text":"Line conductor color in NEW installations?","options":json.dumps(["Brown","Red","Black","Blue"]),"correct_answer":"Brown","explanation":"New: Brown=Line, Blue=Neutral, G/Y=Earth.","regulation_reference":"BS 7671","practical_tip":"Red=old installation. Document it!","epra_class":"Class C"}
]

with app.app_context():
    db.create_all()
    Question.query.delete()
    for q in questions:
        db.session.add(Question(**q))
    db.session.commit()
    print(f"Seeded {len(questions)} questions!")

print("Database ready!")
''')

# frontend/css/style.css
with open('frontend/css/style.css', 'w') as f:
    f.write('''*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#f5f5f5;color:#333}.navbar{background:#1a237e;color:#fff;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}.navbar a{color:#fff;text-decoration:none;margin:0 10px}.btn{padding:10px 24px;border-radius:8px;border:none;cursor:pointer;font-weight:600;text-decoration:none;display:inline-block}.btn-primary{background:#ff9800;color:#fff}.btn-primary:hover{background:#f57c00}.btn-outline{background:transparent;color:#fff;border:2px solid #fff}.hero{background:linear-gradient(135deg,#1a237e,#283593);color:#fff;padding:4rem 2rem;text-align:center}.hero h1{font-size:2.5rem;margin-bottom:1rem}.hero p{font-size:1.2rem;margin-bottom:2rem}.highlight{color:#ff9800}.features{padding:3rem 2rem;max-width:1200px;margin:0 auto}.features h2{text-align:center;margin-bottom:2rem;color:#1a237e}.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem}.feature-card{background:#fff;padding:1.5rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.1);text-align:center}.feature-card h3{color:#1a237e;margin:10px 0}.feature-icon{font-size:2.5rem}.footer{background:#1a237e;color:#fff;padding:2rem;text-align:center}.footer a{color:#ff9800}.exam-container{max-width:800px;margin:2rem auto;padding:1rem}.question-box{background:#fff;padding:2rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.1);margin:1rem 0}.option{padding:12px;margin:8px 0;border:2px solid #ddd;border-radius:8px;cursor:pointer}.option:hover{border-color:#1976d2;background:#e3f2fd}.option.selected{border-color:#ff9800;background:#fff3e0}.timer{font-size:1.5rem;color:#ff9800;text-align:center}.form-container{max-width:400px;margin:3rem auto;padding:2rem;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.1)}.form-container input,.form-container select{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:8px}.form-container button{width:100%;margin-top:15px}''')

# frontend/js/app.js
with open('frontend/js/app.js', 'w') as f:
    f.write('''const API="http://localhost:5000/api";const token=localStorage.getItem("access_token");function logout(){localStorage.removeItem("access_token");window.location.href="../index.html"}function toggleMenu(){document.getElementById("navMenu").classList.toggle("active")}document.addEventListener("DOMContentLoaded",()=>{if(token){const e=document.getElementById("authButtons"),t=document.getElementById("userMenu");e&&(e.style.display="none");t&&(t.style.display="flex")}});console.log("EPRA Exam Prep - Safari Softwares (c) 2026");''')

# frontend/index.html
with open('frontend/index.html', 'w') as f:
    f.write('''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>EPRA Exam Prep - Safari Softwares</title><link rel="stylesheet" href="css/style.css"></head><body><nav class="navbar"><h2>EPRA Exam Prep</h2><div id="authButtons"><a href="pages/login.html" class="btn btn-outline">Login</a><a href="pages/register.html" class="btn btn-primary">Register</a></div><div id="userMenu" style="display:none"><a href="pages/dashboard.html">Dashboard</a><button onclick="logout()" class="btn btn-outline">Logout</button></div></nav><section class="hero"><h1>Master Your <span class="highlight">EPRA</span> Certification</h1><p>Practice exams for Class C, B, and A electricians | Safari Softwares (c) 2026</p><a href="pages/register.html" class="btn btn-primary" style="font-size:1.2rem;padding:15px 40px">Start Free Practice</a></section><section class="features"><h2>Why Choose Us?</h2><div class="features-grid"><div class="feature-card"><div class="feature-icon">P</div><h3>Full Exam Simulation</h3><p>Timed exams matching EPRA format</p></div><div class="feature-card"><div class="feature-icon">M</div><h3>Study Materials</h3><p>Detailed explanations & tips</p></div><div class="feature-card"><div class="feature-icon">K</div><h3>Kenya-Specific</h3><p>Kenya Power & EPRA standards</p></div></div></section><footer class="footer"><p>(c) 2026 Safari Softwares | <a href="mailto:safarisoftwares@gmail.com">safarisoftwares@gmail.com</a></p><p><a href="../legal/terms-of-use.html">Terms</a> | <a href="../legal/privacy-policy.html">Privacy</a> | <a href="../legal/copyright.html">Copyright</a></p></footer><script src="js/app.js"></script></body></html>''')

# frontend/pages/login.html
with open('frontend/pages/login.html', 'w') as f:
    f.write('''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Login - EPRA</title><link rel="stylesheet" href="../css/style.css"></head><body><nav class="navbar"><h2>EPRA Login</h2><a href="../index.html" class="btn btn-outline">Home</a></nav><div class="form-container"><h2 style="text-align:center;color:#1a237e">Login</h2><form id="f"><input type="email" id="email" placeholder="Email" required><input type="password" id="password" placeholder="Password" required><button type="submit" class="btn btn-primary">Login</button></form><p style="text-align:center;margin-top:15px">No account? <a href="register.html">Register</a></p><p id="msg" style="color:red;text-align:center"></p></div><script>document.getElementById("f").addEventListener("submit",async(e)=>{e.preventDefault();try{const r=await fetch("http://localhost:5000/api/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:document.getElementById("email").value,password:document.getElementById("password").value})});const d=await r.json();r.ok?(localStorage.setItem("access_token",d.access_token),window.location.href="dashboard.html"):document.getElementById("msg").textContent=d.error}catch(err){document.getElementById("msg").textContent="Server not running?"}});</script></body></html>''')

# frontend/pages/register.html
with open('frontend/pages/register.html', 'w') as f:
    f.write('''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Register - EPRA</title><link rel="stylesheet" href="../css/style.css"></head><body><nav class="navbar"><h2>Register</h2><a href="../index.html" class="btn btn-outline">Home</a></nav><div class="form-container"><h2 style="text-align:center;color:#1a237e">Create Account</h2><form id="f"><input type="text" id="username" placeholder="Username" required><input type="email" id="email" placeholder="Email" required><input type="text" id="full_name" placeholder="Full Name" required><input type="password" id="password" placeholder="Password" required><select id="cert"><option value="Class C">Class C (Domestic)</option><option value="Class B">Class B (Commercial)</option><option value="Class A">Class A (HV)</option></select><label><input type="checkbox" id="terms" required> Accept <a href="../../legal/terms-of-use.html" target="_blank">Terms</a></label><label><input type="checkbox" id="privacy" required> Accept <a href="../../legal/privacy-policy.html" target="_blank">Privacy</a></label><button type="submit" class="btn btn-primary">Register</button></form><p style="text-align:center;margin-top:15px">Have account? <a href="login.html">Login</a></p><p id="msg" style="color:red;text-align:center"></p></div><script>document.getElementById("f").addEventListener("submit",async(e)=>{e.preventDefault();try{const r=await fetch("http://localhost:5000/api/auth/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:document.getElementById("username").value,email:document.getElementById("email").value,full_name:document.getElementById("full_name").value,password:document.getElementById("password").value,certification_class:document.getElementById("cert").value,accepted_terms:document.getElementById("terms").checked,accepted_privacy:document.getElementById("privacy").checked})});const d=await r.json();r.ok?(localStorage.setItem("access_token",d.access_token),window.location.href="dashboard.html"):document.getElementById("msg").textContent=d.error}catch(err){document.getElementById("msg").textContent="Server not running?"}});</script></body></html>''')

# frontend/pages/dashboard.html
with open('frontend/pages/dashboard.html', 'w') as f:
    f.write('''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Dashboard - EPRA</title><link rel="stylesheet" href="../css/style.css"></head><body><nav class="navbar"><h2>Dashboard</h2><div><a href="exam.html" class="btn btn-primary">Take Exam</a><a href="study.html" class="btn btn-outline">Study</a><button onclick="logout()" class="btn btn-outline">Logout</button></div></nav><div style="max-width:800px;margin:2rem auto;padding:1rem"><h1 style="color:#1a237e">Welcome, <span id="name">Electrician</span>!</h1><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-top:2rem"><div class="feature-card" onclick="location.href='exam.html'" style="cursor:pointer"><h3>Start Exam</h3><p>10 Questions - Timed</p></div><div class="feature-card" onclick="location.href='study.html'" style="cursor:pointer"><h3>Study Mode</h3><p>Learn with answers</p></div></div><div id="stats" style="margin-top:2rem"></div></div><script src="../js/app.js"></script><script>const t=localStorage.getItem("access_token");if(!t)location.href="login.html";fetch("http://localhost:5000/api/progress/dashboard",{headers:{"Authorization":"Bearer "+t}}).then(r=>r.json()).then(d=>{document.getElementById("name").textContent=d.user.full_name;document.getElementById("stats").innerHTML="<h3>Your Stats</h3><p>Exams Taken: "+d.overall_stats.total_exams+" | Passed: "+d.overall_stats.passed_exams+" | Last Score: "+(d.overall_stats.last_score||0)+"%</p>"}).catch(()=>{});</script></body></html>''')

# frontend/pages/exam.html  
with open('frontend/pages/exam.html', 'w') as f:
    f.write('''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Exam - EPRA</title><link rel="stylesheet" href="../css/style.css"></head><body><nav class="navbar"><h2>Exam Mode</h2><a href="dashboard.html" class="btn btn-outline">Back</a></nav><div class="exam-container"><h2 style="text-align:center">EPRA Exam Simulation</h2><div class="timer">Time: <span id="timer">60:00</span></div><button id="startBtn" class="btn btn-primary" style="display:block;margin:20px auto">Start Exam</button><div id="qArea" style="display:none"></div><button id="submitBtn" class="btn btn-primary" style="display:none;margin:20px auto">Submit Exam</button></div><script src="../js/app.js"></script><script>let qs=[],ci=0,ans={},tl=3600,ti,eid;const t=localStorage.getItem("access_token");if(!t)location.href="login.html";document.getElementById("startBtn").addEventListener("click",async()=>{try{const r=await fetch("http://localhost:5000/api/exam/start",{method:"POST",headers:{"Authorization":"Bearer "+t,"Content-Type":"application/json"},body:JSON.stringify({total_questions:5})});const d=await r.json();if(!r.ok){alert(d.error);return}qs=d.questions;eid=d.exam_id;document.getElementById("startBtn").style.display="none";document.getElementById("submitBtn").style.display="block";showQ();ti=setInterval(()=>{tl--;document.getElementById("timer").textContent=Math.floor(tl/60)+":"+(tl%60<10?"0":"")+tl%60;if(tl<=0)submitE()},1000)}catch(e){alert("Server not running?")}});function showQ(){if(ci>=qs.length){submitE();return}const q=qs[ci];let h='<div class="question-box"><h3>Q'+(ci+1)+"/"+qs.length+'</h3><p style="font-size:1.2rem;margin:20px 0">'+q.question_text+'</p>';q.options.forEach((o,i)=>{h+='<div class="option'+(ans[q.id]===o?" selected":"")+'" onclick="sel(\\''+q.id+'\\',\\''+o.replace(/'/g,"\\\\'")+'\\')">'+(i+1)+". "+o+'</div>'});h+='</div><div style="display:flex;gap:10px;justify-content:center">';if(ci>0)h+='<button class="btn btn-outline" onclick="ci--;showQ()">Previous</button>';h+='<button class="btn btn-primary" onclick="ci++;showQ()">'+(ci<qs.length-1?"Next":"Finish")+"</button></div>";document.getElementById("qArea").innerHTML=h;document.getElementById("qArea").style.display="block"}function sel(id,o){ans[id]=o;showQ()}async function submitE(){clearInterval(ti);const r=await fetch("http://localhost:5000/api/exam/submit",{method:"POST",headers:{"Authorization":"Bearer "+t,"Content-Type":"application/json"},body:JSON.stringify({exam_id:eid,answers:ans,time_taken:3600-tl})});const d=await r.json();document.getElementById("qArea").innerHTML='<div class="question-box" style="text-align:center"><h2>Exam Complete!</h2><p style="font-size:3rem;color:'+(d.passed?"green":"red")+'">'+d.percentage+"%</p><p>"+d.score+"/"+d.total+" correct</p><p>"+(d.passed?"PASSED!":"Keep practicing!")+'</p><a href="dashboard.html" class="btn btn-primary">Back to Dashboard</a></div>';document.getElementById("submitBtn").style.display="none"}</script></body></html>''')

# frontend/pages/study.html
with open('frontend/pages/study.html', 'w') as f:
    f.write('''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Study - EPRA</title><link rel="stylesheet" href="../css/style.css"></head><body><nav class="navbar"><h2>Study Mode</h2><a href="dashboard.html" class="btn btn-outline">Back</a></nav><div class="exam-container"><h2 style="text-align:center;color:#1a237e">Study Materials</h2><div id="content"></div></div><script src="../js/app.js"></script><script>const t=localStorage.getItem("access_token");if(!t)location.href="login.html";fetch("http://localhost:5000/api/questions?limit=20&include_answer=true",{headers:{"Authorization":"Bearer "+t}}).then(r=>r.json()).then(d=>{let h="";d.questions.forEach((q,i)=>{h+='<div class="question-box"><h3>Q'+(i+1)+": "+q.question_text+'</h3><p><b>Category:</b> '+q.category+'</p><p><b>Regulation:</b> '+q.regulation_reference+'</p><button class="btn btn-primary" onclick="document.getElementById(\\'a'+i+'\\').style.display=\\'block\\'">Show Answer</button><div id="a'+i+'" style="display:none;margin-top:10px;padding:10px;background:#e8f5e9;border-radius:8px"><p>Answer: <b>'+q.correct_answer+'</b></p><p>'+q.explanation+'</p>'+(q.practical_tip?"<p>Tip: "+q.practical_tip+"</p>":"")+"</div></div>"});document.getElementById("content").innerHTML=h}).catch(()=>{document.getElementById("content").innerHTML='<p style="text-align:center">Could not load questions. Run seed_data.py first!</p>'});</script></body></html>''')

# legal files
with open('legal/terms-of-use.html', 'w') as f:
    f.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Terms of Use - Safari Softwares</title><style>body{font-family:Arial;max-width:800px;margin:20px auto;padding:20px}h1{color:#1976d2}h2{border-bottom:2px solid #ff9800}</style></head><body><h1>TERMS OF USE</h1><p><em>Last Updated: January 1, 2026</em></p><h2>1. Acceptance</h2><p>By using this platform, you agree to these terms. The Service is owned by <strong>Safari Softwares</strong>.</p><h2>2. Service Description</h2><p>EPRA exam preparation tool. <strong>Not affiliated with EPRA.</strong></p><h2>3. Intellectual Property</h2><p>All content (c) 2026 Safari Softwares. All rights reserved.</p><h2>4. Disclaimer</h2><p>No guarantee of exam success. Service provided "AS IS".</p><h2>5. Contact</h2><p>Email: safarisoftwares@gmail.com</p><hr><p>(c) 2026 Safari Softwares</p></body></html>')

with open('legal/privacy-policy.html', 'w') as f:
    f.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Privacy Policy - Safari Softwares</title><style>body{font-family:Arial;max-width:800px;margin:20px auto;padding:20px}h1{color:#1976d2}h2{border-bottom:2px solid #ff9800}</style></head><body><h1>PRIVACY POLICY</h1><p><em>Last Updated: January 1, 2026</em></p><h2>1. Data Collection</h2><p>We collect account info and exam progress data.</p><h2>2. Data Use</h2><p>To provide and improve the service.</p><h2>3. No Selling</h2><p><strong>We DO NOT sell your data.</strong></p><h2>4. Your Rights</h2><p>Access, correct, delete your data per Kenya Data Protection Act 2019.</p><h2>5. Contact</h2><p>Email: safarisoftwares@gmail.com</p><hr><p>(c) 2026 Safari Softwares</p></body></html>')

with open('legal/copyright.html', 'w') as f:
    f.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Copyright - Safari Softwares</title><style>body{font-family:Arial;max-width:800px;margin:20px auto;padding:20px}h1{color:#1976d2}h2{border-bottom:2px solid #ff9800}</style></head><body><h1>COPYRIGHT NOTICE</h1><h2>Safari Softwares</h2><p>Email: safarisoftwares@gmail.com</p><p>(c) 2024-2026 Safari Softwares. All Rights Reserved.</p><h2>Protected Works</h2><p>Software code, question database, UI design, brand assets.</p><h2>Legal Framework</h2><p>Copyright Act Cap 130, Laws of Kenya. Berne Convention.</p><h2>Prohibited</h2><p>Copying, reproducing, reverse engineering, selling content.</p><hr><p>(c) 2026 Safari Softwares. All rights reserved worldwide.</p></body></html>')

print("ALL FILES CREATED SUCCESSFULLY!")
print("Next: pip install -r backend/requirements.txt")
print("Then: python backend/seed_data.py")
print("Then: python backend/app.py")
