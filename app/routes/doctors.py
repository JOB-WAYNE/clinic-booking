from flask import Blueprint, request, jsonify
from app.models.doctor import Doctor
from app.models.user import User
from app.extensions import db
from app.utils.auth import admin_required, token_required  # ✅

doctors_bp = Blueprint('doctors', __name__)

# ➕ Create a new doctor (admin only)
@doctors_bp.route('/doctors', methods=['POST'])
@admin_required
def create_doctor(current_user):
    data = request.get_json()
    new_doctor = Doctor(
        user_id=current_user.id,
        name=data['name'],
        specialty=data['specialty'],
        email=data['email'],
        bio=data.get('bio'),
        availability=data.get('availability')
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor created successfully'}), 201


# 📋 Get all doctors (public)
@doctors_bp.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([
        {
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'email': doctor.email,
            'bio': doctor.bio,
            'availability': doctor.availability
        } for doctor in doctors
    ])


# 🔄 Update a doctor (only the owner can update)
@doctors_bp.route('/doctors/<int:id>', methods=['PUT'])
@token_required
def update_doctor(current_user, id):
    doctor = Doctor.query.get_or_404(id)

    if doctor.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    doctor.name = data.get('name', doctor.name)
    doctor.specialty = data.get('specialty', doctor.specialty)
    doctor.email = data.get('email', doctor.email)
    doctor.bio = data.get('bio', doctor.bio)
    doctor.availability = data.get('availability', doctor.availability)

    db.session.commit()
    return jsonify({'message': 'Doctor updated successfully'})


# ❌ Delete a doctor (only the owner can delete)
@doctors_bp.route('/doctors/<int:id>', methods=['DELETE'])
@token_required
def delete_doctor(current_user, id):
    doctor = Doctor.query.get_or_404(id)

    if doctor.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'})


# 🔍 Search doctors by name or specialty (public)
@doctors_bp.route('/doctors/search', methods=['GET'])
def search_doctors():
    name = request.args.get('name')
    specialty = request.args.get('specialty')

    query = Doctor.query
    if name:
        query = query.filter(Doctor.name.ilike(f"%{name}%"))
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))

    results = query.all()
    return jsonify([
        {
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'email': doctor.email,
            'bio': doctor.bio,
            'availability': doctor.availability
        } for doctor in results
    ])
