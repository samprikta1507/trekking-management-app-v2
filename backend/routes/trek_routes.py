from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Trek, StaffProfile
from datetime import datetime
from extensions import cache

trek_bp = Blueprint('trek_bp', __name__)

@trek_bp.route("/api/admin/treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def get_treks():
    print("WARNING: Fetching from SQLite Database!")

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
            "assigned_staff_id": trek.assigned_staff_id,
            "status": trek.status,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date),
            "price": trek.price
        })

    return jsonify(trek_list), 200

@trek_bp.route("/api/admin/create-trek", methods=["POST"])
@jwt_required()
def create_trek():

    data = request.get_json()

    staff = StaffProfile.query.get(data.get("assigned_staff_id"))

    if not staff:
        return jsonify({"message": "Assigned staff not found"}), 404

    new_trek = Trek(
        trek_name=data.get("trek_name"),
        location=data.get("location"),
        difficulty=data.get("difficulty"),
        duration_days=data.get("duration_days"),
        available_slots=data.get("available_slots"),
        assigned_staff_id=data.get("assigned_staff_id"),
        start_date=datetime.strptime(data.get("start_date"), "%Y-%m-%d").date(),
        end_date=datetime.strptime(data.get("end_date"), "%Y-%m-%d").date(),
        price=data.get("price")
    )

    db.session.add(new_trek)
    db.session.commit()

    return jsonify({"message": "Trek created successfully"}), 201

@trek_bp.route("/api/admin/update-trek/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek(trek_id):

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()

    staff = StaffProfile.query.get(data.get("assigned_staff_id"))

    if not staff:
        return jsonify({"message": "Assigned staff not found"}), 404

    trek.trek_name = data.get("trek_name")
    trek.location = data.get("location")
    trek.difficulty = data.get("difficulty")
    trek.duration_days = data.get("duration_days")
    trek.available_slots = data.get("available_slots")
    trek.assigned_staff_id = data.get("assigned_staff_id")

    trek.start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
    trek.end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()

    trek.price = data.get("price")
    trek.status = data.get("status")

    db.session.commit()

    return jsonify({"message": "Trek updated successfully"}), 200

@trek_bp.route("/api/admin/delete-trek/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek(trek_id):

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()

    return jsonify({"message": "Trek deleted successfully"}), 200