from flask import jsonify
from .users import users_bp
from .doctors import doctors_bp
from .appointments import appointments_bp
from .auth import auth_bp
from app.models.patient import Patient
from .patients import patients_bp



def register_routes(app):
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Clinic Appointment Booking API 🚀"})

    app.register_blueprint(users_bp)         # ✅ Don't repeat url_prefix
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patients_bp)
