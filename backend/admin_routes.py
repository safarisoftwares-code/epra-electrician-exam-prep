from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Admin, User, Subscription, ActivationKey, Payment
from datetime import datetime, timedelta
import random, string, os

admin_bp = Blueprint('admin', __name__)

def generate_key():
    chars = string.ascii_uppercase + string.digits
    return "EPRA-" + ''.join(random.choices(chars, k=4)) + "-" + ''.join(random.choices(chars, k=4)) + "-" + ''.join(random.choices(chars, k=4))

def generate_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=12))

# Admin Auth
@admin_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data.get('username')).first()
    if not admin or not admin.check_password(data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity="admin_"+str(admin.id))
    return jsonify({"access_token": token, "admin": admin.to_dict()})

# Dashboard Stats
@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    total_users = User.query.count()
    premium_users = Subscription.query.filter_by(status="active").count()
    pending_payments = Payment.query.filter_by(status="pending").count()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status="verified").scalar() or 0
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    keys_available = ActivationKey.query.filter_by(is_used=False).count()
    
    return jsonify({
        "stats": {
            "total_users": total_users,
            "premium_users": premium_users,
            "pending_payments": pending_payments,
            "total_revenue": total_revenue,
            "keys_available": keys_available
        },
        "recent_payments": [p.to_dict() for p in recent_payments]
    })

# Generate Activation Key
@admin_bp.route('/api/admin/generate-key', methods=['POST'])
@jwt_required()
def generate_activation_key():
    data = request.get_json()
    count = data.get('count', 1)
    duration = data.get('duration_days', 365)
    keys = []
    for _ in range(count):
        key = ActivationKey(
            key=generate_key(),
            password=generate_password(),
            duration_days=duration
        )
        db.session.add(key)
        keys.append({"key": key.key, "password": key.password})
    db.session.commit()
    return jsonify({"keys": keys, "message": f"Generated {count} key(s)"})

# View All Keys
@admin_bp.route('/api/admin/keys', methods=['GET'])
@jwt_required()
def view_keys():
    keys = ActivationKey.query.order_by(ActivationKey.created_at.desc()).limit(50).all()
    return jsonify([k.to_dict() for k in keys])

# Verify Payment
@admin_bp.route('/api/admin/verify-payment', methods=['POST'])
@jwt_required()
def verify_payment():
    data = request.get_json()
    payment = Payment.query.get(data['payment_id'])
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    
    payment.status = "verified"
    payment.verified_by = data.get('verified_by', 'admin')
    payment.verified_at = datetime.utcnow()
    
    # Generate activation key for user
    key_str = generate_key()
    password = generate_password()
    key = ActivationKey(
        key=key_str,
        password=password,
        is_used=True,
        used_by=payment.user_id,
        used_at=datetime.utcnow()
    )
    db.session.add(key)
    
    # Create subscription
    sub = Subscription(
        user_id=payment.user_id,
        plan="premium",
        activation_key=key_str,
        status="active",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=365)
    )
    db.session.add(sub)
    db.session.commit()
    
    return jsonify({
        "message": "Payment verified!",
        "activation_key": key_str,
        "password": password,
        "subscription": sub.to_dict()
    })

# View Payments
@admin_bp.route('/api/admin/payments', methods=['GET'])
@jwt_required()
def view_payments():
    status = request.args.get('status', 'all')
    query = Payment.query
    if status != 'all':
        query = query.filter_by(status=status)
    payments = query.order_by(Payment.created_at.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in payments])

# View Subscribers
@admin_bp.route('/api/admin/subscribers', methods=['GET'])
@jwt_required()
def view_subscribers():
    subs = db.session.query(Subscription, User).join(User, Subscription.user_id == User.id).order_by(Subscription.created_at.desc()).limit(50).all()
    result = []
    for sub, user in subs:
        item = sub.to_dict()
        item['user'] = user.to_dict()
        result.append(item)
    return jsonify(result)

# Serve Admin Panel
@admin_bp.route('/admin')
def admin_panel():
    return send_from_directory('../frontend/pages/admin', 'login.html')

@admin_bp.route('/admin/<path:path>')
def admin_static(path):
    return send_from_directory('../frontend/pages/admin', path)

# Change Admin Password
@admin_bp.route('/api/admin/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    uid = get_jwt_identity().replace("admin_", "")
    admin = db.session.get(Admin, int(uid))
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    if not admin.check_password(data.get('current_password')):
        return jsonify({"error": "Current password is incorrect"}), 400
    admin.set_password(data.get('new_password'))
    db.session.commit()
    return jsonify({"message": "Password changed successfully"})


# Update Admin Profile
@admin_bp.route('/api/admin/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    uid = get_jwt_identity().replace("admin_", "")
    admin = db.session.get(Admin, int(uid))
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    if data.get('username'):
        existing = Admin.query.filter_by(username=data['username']).first()
        if existing and existing.id != admin.id:
            return jsonify({"error": "Username already taken"}), 400
        admin.username = data['username']
    if data.get('email'):
        admin.email = data['email']
    if data.get('full_name'):
        admin.full_name = data['full_name']
    db.session.commit()
    return jsonify({"message": "Profile updated", "admin": admin.to_dict()})


# Get Admin Profile
@admin_bp.route('/api/admin/profile', methods=['GET'])
@jwt_required()
def get_profile():
    uid = get_jwt_identity().replace("admin_", "")
    admin = db.session.get(Admin, int(uid))
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    return jsonify(admin.to_dict())

@app.route('/api/admin/deactivate-key', methods=['POST'])
@jwt_required()
def deactivate_key():
    data = request.get_json()
    key = ActivationKey.query.filter_by(key=data.get('key')).first()
    if not key:
        return jsonify({'error': 'Key not found'}), 404
    key.is_used = True  # Mark as used/deactivated
    # Also deactivate subscription if exists
    sub = Subscription.query.filter_by(activation_key=key.key, status='active').first()
    if sub:
        sub.status = 'expired'
    db.session.commit()
    return jsonify({'message': 'Key deactivated successfully'})

    return send_from_directory('../frontend/pages/admin', path)