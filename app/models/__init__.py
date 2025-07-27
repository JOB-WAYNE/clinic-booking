from app.extensions import db  # ✅ Use centralized db instance
from .user import User
from .doctor import Doctor
from .appointment import Appointment

__all__ = ['User', 'Doctor', 'Appointment']
