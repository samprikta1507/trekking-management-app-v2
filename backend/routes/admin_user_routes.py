from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, StaffProfile, Trek, Booking

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/api/admin/users", methods=["GET"])
@jwt_required()
def get_users():

    users = User.query.filter_by(role="user").all()

    user_list = []

    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_blacklisted": user.is_blacklisted
        })

    return jsonify(user_list), 200

@user_bp.route("/api/admin/toggle-blacklist/<int:user_id>", methods=["PUT"])
@jwt_required()
def toggle_blacklist(user_id):

    user = User.query.filter_by(id=user_id, role="user").first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_blacklisted = not user.is_blacklisted

    db.session.commit()

    return jsonify({
        "message": "Blacklist status updated",
        "is_blacklisted": user.is_blacklisted
    }), 200

@user_bp.route("/api/admin/bookings", methods=["GET"])
@jwt_required()
def get_all_bookings():

    bookings = Booking.query.all()

    booking_list = []

    for booking in bookings:

        booking_list.append({
            "booking_id": booking.id,
            "user_name": booking.user.name,
            "user_email": booking.user.email,
            "trek_name": booking.trek.trek_name,
            "booking_date": str(booking.booking_date),
            "status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify(booking_list), 200
