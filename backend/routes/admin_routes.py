from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, StaffProfile, Trek
from datetime import datetime
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route("/api/admin/staff", methods=["GET"])
@jwt_required()
def get_staff():

    staff_members = User.query.filter_by(role="staff").all()

    staff_list = []

    for staff in staff_members:
        staff_profile = StaffProfile.query.filter_by(user_id=staff.id).first()

        staff_list.append({
            "id": staff.id,
            "staff_profile_id": staff_profile.id,
            "name": staff.name,
            "email": staff.email,
            "phone": staff.phone,
            "experience_years": staff_profile.experience_years if staff_profile else 0,
            "specialization": staff_profile.specialization if staff_profile else ""
        })

    return jsonify(staff_list), 200

@admin_bp.route("/api/admin/create-staff", methods=["POST"])
@jwt_required()
def create_staff():

    data = request.get_json()

    existing_user = User.query.filter_by(email=data.get("email")).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(
        data.get("password")
    )
    
    staff_user = User(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        password_hash=hashed_password,
        role="staff"
    )

    db.session.add(staff_user)
    db.session.commit()

    staff_profile = StaffProfile(
        user_id=staff_user.id,
        experience_years=data.get("experience_years"),
        specialization=data.get("specialization")
    )

    db.session.add(staff_profile)
    db.session.commit()

    return jsonify({"message": "Staff created successfully"}), 201

@admin_bp.route("/api/admin/delete-staff/<int:staff_id>", methods=["DELETE"])
@jwt_required()
def delete_staff(staff_id):

    staff_user = User.query.filter_by(id=staff_id, role="staff").first()

    if not staff_user:
        return jsonify({"message": "Staff not found"}), 404

    staff_profile = StaffProfile.query.filter_by(user_id=staff_user.id).first()

    if staff_profile:
        db.session.delete(staff_profile)

    db.session.delete(staff_user)
    db.session.commit()

    return jsonify({"message": "Staff deleted successfully"}), 200

@admin_bp.route("/api/admin/update-staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def update_staff(staff_id):

    staff_user = User.query.filter_by(id=staff_id, role="staff").first()

    if not staff_user:
        return jsonify({"message": "Staff not found"}), 404

    data = request.get_json()

    staff_user.name = data.get("name")
    staff_user.email = data.get("email")
    staff_user.phone = data.get("phone")

    staff_profile = StaffProfile.query.filter_by(user_id=staff_user.id).first()

    if staff_profile:
        staff_profile.experience_years = data.get("experience_years")
        staff_profile.specialization = data.get("specialization")

    db.session.commit()

    return jsonify({"message": "Staff updated successfully"}), 200