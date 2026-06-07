from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    hashed_password = generate_password_hash(password)

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(name=name,email=email,phone=phone,password_hash=hashed_password,role="user")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.is_blacklisted:
        return jsonify({"message": "Your account has been blacklisted"}), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid password"}), 401

    access_token = create_access_token(identity=user.email)

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "role": user.role,
        "email": user.email
    }), 200