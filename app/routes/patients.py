from flask import Blueprint, request, jsonify
from app.models.patient import Patient
from app.extensions import db
from app.utils.auth import token_required

patients_bp = Blueprint('patients', __name__)

# ➕ Create a new patient
@patients_bp.route('/patients', methods=['POST'])
@token_required
def create_patient(current_user):
    data = request.get_json()

    new_patient = Patient(
        user_id=current_user.id,
        date_of_birth=data.get('date_of_birth'),
        address=data.get('address'),
        medical_history=data.get('medical_history')
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully'}), 201


# 📋 Get all patients
@patients_bp.route('/patients', methods=['GET'])
@token_required
def get_patients(current_user):
    patients = Patient.query.all()
    return jsonify([
        {
            'id': patient.id,
            'user_id': patient.user_id,
            'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            'address': patient.address,
            'medical_history': patient.medical_history
        } for patient in patients
    ])


# 🔄 Update a patient
@patients_bp.route('/patients/<int:id>', methods=['PUT'])
@token_required
def update_patient(current_user, id):
    patient = Patient.query.get_or_404(id)
    data = request.get_json()

    if patient.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    patient.date_of_birth = data.get('date_of_birth', patient.date_of_birth)
    patient.address = data.get('address', patient.address)
    patient.medical_history = data.get('medical_history', patient.medical_history)

    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'})


# ❌ Delete a patient
@patients_bp.route('/patients/<int:id>', methods=['DELETE'])
@token_required
def delete_patient(current_user, id):
    patient = Patient.query.get_or_404(id)

    if patient.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})


# 🔍 Search patients by address or medical history
@patients_bp.route('/patients/search', methods=['GET'])
@token_required
def search_patients(current_user):
    address = request.args.get('address')
    history = request.args.get('medical_history')

    query = Patient.query
    if address:
        query = query.filter(Patient.address.ilike(f"%{address}%"))
    if history:
        query = query.filter(Patient.medical_history.ilike(f"%{history}%"))

    results = query.all()
    return jsonify([
        {
            'id': patient.id,
            'user_id': patient.user_id,
            'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            'address': patient.address,
            'medical_history': patient.medical_history
        } for patient in results
    ])
