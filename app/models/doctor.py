from datetime import datetime
from app.extensions import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # 👈 Add this
    email = db.Column(db.String(100), nullable=False)  # 👈 And this
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    availability = db.Column(db.String(100))  # e.g., "Mon-Fri 9am-5pm"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('doctor_profile', uselist=False))
