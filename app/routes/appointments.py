from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.appointment import Appointment
from app.extensions import db
from app.utils.auth import token_required

appointments_bp = Blueprint('appointments', __name__)

# 🛠️ Create an appointment
@appointments_bp.route('/appointments', methods=['POST'])
@token_required
def create_appointment(current_user):
    data = request.get_json()

    try:
        new_appointment = Appointment(
            patient_id=current_user.id,
            patient_name=data['patient_name'],
            doctor_id=data['doctor_id'],
            scheduled_time=datetime.strptime(data['scheduled_time'], '%Y-%m-%dT%H:%M:%S')
        )
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({'message': 'Appointment created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# 📋 Get all appointments for current user
@appointments_bp.route('/appointments', methods=['GET'])
@token_required
def get_appointments(current_user):
    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return jsonify([
        {
            'id': a.id,
            'patient_name': a.patient_name,
            'doctor_id': a.doctor_id,
            'scheduled_time': a.scheduled_time.strftime('%Y-%m-%dT%H:%M:%S')
        } for a in appointments
    ])


# 🔄 Update an appointment
@appointments_bp.route('/appointments/<int:id>', methods=['PUT'])
@token_required
def update_appointment(current_user, id):
    appointment = Appointment.query.get_or_404(id)

    if appointment.patient_id != current_user.id:
        return jsonify({'error': 'Unauthorized access to this appointment'}), 403

    data = request.get_json()
    appointment.patient_name = data.get('patient_name', appointment.patient_name)
    appointment.doctor_id = data.get('doctor_id', appointment.doctor_id)

    if 'scheduled_time' in data:
        appointment.scheduled_time = datetime.strptime(data['scheduled_time'], '%Y-%m-%dT%H:%M:%S')

    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'})


# ❌ Delete an appointment
@appointments_bp.route('/appointments/<int:id>', methods=['DELETE'])
@token_required
def delete_appointment(current_user, id):
    appointment = Appointment.query.get_or_404(id)

    if appointment.patient_id != current_user.id:
        return jsonify({'error': 'Unauthorized access to this appointment'}), 403

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment deleted successfully'})


# 🔍 Search appointments by date (for current user)
@appointments_bp.route('/appointments/search', methods=['GET'])
@token_required
def search_appointments(current_user):
    date_str = request.args.get('date')  # Format: YYYY-MM-DD

    if not date_str:
        return jsonify({'error': 'Missing date query parameter'}), 400

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        results = Appointment.query.filter(
            db.func.date(Appointment.scheduled_time) == date_obj,
            Appointment.patient_id == current_user.id
        ).all()

        return jsonify([
            {
                'id': a.id,
                'patient_name': a.patient_name,
                'doctor_id': a.doctor_id,
                'scheduled_time': a.scheduled_time.strftime('%Y-%m-%dT%H:%M:%S')
            } for a in results
        ])

    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
