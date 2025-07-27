from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db
import jwt
import datetime
from config import Config

auth_bp = Blueprint('auth_bp', __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ['full_name', 'email', 'phone', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'error': 'Phone already exists'}), 409

    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        role=data['role']
    )
    new_user.set_password(data['password'])  # 🔐 using your model's method

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f"User {data['full_name']} registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):  # 🔐 using your model method
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token})

# ✅ Debug print to confirm blueprint is loaded
print("✅ Auth blueprint loaded successfully")
