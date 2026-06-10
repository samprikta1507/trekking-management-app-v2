from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, StaffProfile, Trek, Booking

staff_bp = Blueprint("staff_bp", __name__)

@staff_bp.route("/my-treks", methods=["GET"])
@jwt_required()
def get_my_treks():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    staff_profile = StaffProfile.query.filter_by(user_id=user.id).first()

    if not staff_profile:
        return jsonify({
            "message": "Staff profile not found"
        }), 404

    treks = Trek.query.filter_by(assigned_staff_id=staff_profile.id).all()

    result = []

    for trek in treks:

        result.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "registered_trekkers": len(trek.bookings)
        })

    return jsonify(result), 200


@staff_bp.route("/update-status/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_status(trek_id):

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user or user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    staff_profile = StaffProfile.query.filter_by(user_id=user.id).first()

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    # Ownership check
    if trek.assigned_staff_id != staff_profile.id:
        return jsonify({
            "message": "You can only manage your assigned treks"
        }), 403

    data = request.get_json()

    allowed_statuses = [
        "Open",
        "Closed",
        "Started",
        "Ongoing",
        "Completed"
    ]

    new_status = data.get("status")

    if new_status not in allowed_statuses:
        return jsonify({
            "message": "Invalid status"
        }), 400

    trek.status = new_status

    db.session.commit()

    return jsonify({
        "message": "Status updated successfully"
    }), 200

@staff_bp.route("/participants/<int:trek_id>", methods=["GET"])
@jwt_required()
def get_participants(trek_id):

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user or user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    staff_profile = StaffProfile.query.filter_by(user_id=user.id).first()

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    # Ownership check
    if trek.assigned_staff_id != staff_profile.id:
        return jsonify({
            "message": "You can only view your assigned treks"
        }), 403

    participants = []

    for booking in trek.bookings:

        participants.append({
            "booking_id": booking.id,
            "user_name": booking.user.name,
            "email": booking.user.email,
            "booking_status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify(participants), 200