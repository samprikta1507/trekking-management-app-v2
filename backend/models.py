from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="user")

    phone = db.Column(db.String(15))

    is_active = db.Column(db.Boolean, default=True)

    is_blacklisted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = db.relationship("Booking",backref="user",lazy=True)

    staff_profile = db.relationship("StaffProfile",backref="user",uselist=False)


class StaffProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)

    experience_years = db.Column(db.Integer, default=0)

    specialization = db.Column(db.String(100))

    status = db.Column(db.String(20), default="Active")

    treks = db.relationship("Trek",backref="staff",lazy=True)


class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trek_name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)

    duration_days = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("staff_profile.id"), nullable=False)

    status = db.Column(db.String(20), default="Pending")

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    price = db.Column(db.Float, nullable=False)

    bookings = db.relationship("Booking",backref="trek",lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    trek_id = db.Column(db.Integer, db.ForeignKey("trek.id"), nullable=False)

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="Booked")

    payment_status = db.Column(db.String(20), default="Pending")