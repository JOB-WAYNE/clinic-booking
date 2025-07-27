from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from app.utils.auth import token_required

users_bp = Blueprint('users', __name__, url_prefix='/users')


# ✅ Register a new user
@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    required_fields = ['full_name', 'email', 'phone', 'password', 'role']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(phone=data['phone']).first():
        return jsonify({'error': 'User with this email or phone already exists'}), 400

    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        role=data['role']
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# ✅ Get all users (admin only)
@users_bp.route('/', methods=['GET'])  # <- FIXED: trailing slash
@token_required
def get_users(current_user):
    if current_user.role != 'admin':
        return jsonify({'error': 'Access denied'}), 403

    users = User.query.all()
    return jsonify([
        {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role
        } for user in users
    ])


# ✅ Update a user by ID
@users_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.role = data.get('role', user.role)
    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role
        }
    })


# ✅ Delete a user by ID
@users_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
