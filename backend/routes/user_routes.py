from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Trek, Booking, User, db

user_dashboard_bp = Blueprint("user_dashboard_bp",__name__)


@user_dashboard_bp.route("/api/user/treks", methods=["GET"])
@jwt_required()
def get_available_treks():

    treks = Trek.query.all()

    trek_list = []

    for trek in treks:

        trek_list.append({
            "id": trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration_days": trek.duration_days,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "price": trek.price
        })

    return jsonify(trek_list), 200

@user_dashboard_bp.route("/api/user/book-trek/<int:trek_id>", methods=["POST"])
@jwt_required()
def book_trek(trek_id):

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404

    existing_booking = Booking.query.filter(Booking.user_id == user.id,Booking.trek_id == trek.id,Booking.status == "Booked").first()
    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek"
        }), 400

    if trek.status != "Open":
        return jsonify({
            "message": "Booking is allowed only for Open treks"
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available"
        }), 400

    booking = Booking(user_id=user.id,trek_id=trek.id)

    db.session.add(booking)

    trek.available_slots -= 1

    if trek.available_slots == 0:
        trek.status = "Closed"

    db.session.commit()

    return jsonify({
        "message": "Trek booked successfully"
    }), 201
    
@user_dashboard_bp.route("/api/user/my-bookings", methods=["GET"])
@jwt_required()
def get_my_bookings():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    bookings = Booking.query.filter_by(user_id=user.id).all()

    booking_list = []

    for booking in bookings:

        booking_list.append({
            "id": booking.id,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "start_date": str(booking.trek.start_date),
            "end_date": str(booking.trek.end_date),
            "booking_date": str(booking.booking_date),
            "status": booking.status,
            "payment_status": booking.payment_status
        })

    return jsonify(booking_list), 200

@user_dashboard_bp.route("/api/user/cancel-booking/<int:booking_id>", methods=["PUT"])
@jwt_required()
def cancel_booking(booking_id):

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({
            "message": "Booking not found"
        }), 404

    if booking.user_id != user.id:
        return jsonify({
            "message": "Access denied"
        }), 403

    if booking.status == "Cancelled":
        return jsonify({
            "message": "Booking already cancelled"
        }), 400

    booking.status = "Cancelled"

    booking.trek.available_slots += 1

    if booking.trek.status == "Closed":
        booking.trek.status = "Open"

    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully"
    }), 200

@user_dashboard_bp.route("/api/user/profile", methods=["GET"])
@jwt_required()
def get_profile():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }), 200

@user_dashboard_bp.route("/api/user/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    data = request.get_json()

    user.name = data.get("name")
    user.phone = data.get("phone")

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200