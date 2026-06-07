from flask import Flask, request, jsonify
from models import db, User, StaffProfile, Trek, Booking
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my-secret-key"

CORS(app)

db.init_app(app)

jwt = JWTManager(app)

def admin_required():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return None

    if user.role != "admin":
        return None

    return user

def user_required():

    current_user_email = get_jwt_identity()

    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return None

    if user.role != "user":
        return None

    return user

@app.route("/")
def home():
    return "Trekking Management App Backend Running"

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@trek.com",
            password_hash=generate_password_hash("admin123"),
            role="admin",
            phone="9999999999"
        )

        db.session.add(admin)
        db.session.commit()

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    hashed_password = generate_password_hash(password)

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400

    new_user = User(name=name,email=email,phone=phone,password_hash=hashed_password,role="user")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201  

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404
    
    if user.is_blacklisted:
        return jsonify({
            "message": "Your account has been blacklisted"
        }), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({
            "message": "Invalid password"
        }), 401
    
    access_token = create_access_token(identity=user.email)

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "role": user.role,
        "email": user.email
    }), 200

@app.route("/api/admin/dashboard")
@jwt_required()
def admin_dashboard():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    return jsonify({
        "message": "Welcome Admin",
        "user": admin.email
    }), 200

@app.route("/api/admin/create-staff", methods=["POST"])
@jwt_required()
def create_staff():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    experience_years = data.get("experience_years")
    specialization = data.get("specialization")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        }), 400
    
    staff_user = User(name=name,email=email,phone=phone,password_hash=generate_password_hash(password),role="staff")

    db.session.add(staff_user)
    db.session.commit()

    staff_profile = StaffProfile(user_id=staff_user.id,experience_years=experience_years,specialization=specialization)

    db.session.add(staff_profile)
    db.session.commit()

    return jsonify({
        "message": "Staff created successfully"
    }), 201

@app.route("/api/admin/staff", methods=["GET"])
@jwt_required()
def get_staff():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

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

@app.route("/api/admin/delete-staff/<int:staff_id>", methods=["DELETE"])
@jwt_required()
def delete_staff(staff_id):

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_user = User.query.filter_by(id=staff_id,role="staff").first()

    if not staff_user:
        return jsonify({
            "message": "Staff not found"
        }), 404

    staff_profile = StaffProfile.query.filter_by(user_id=staff_user.id).first()

    if staff_profile:
        db.session.delete(staff_profile)

    db.session.delete(staff_user)

    db.session.commit()

    return jsonify({
        "message": "Staff deleted successfully"
    }), 200

@app.route("/api/admin/update-staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def update_staff(staff_id):

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    staff_user = User.query.filter_by(id=staff_id,role="staff").first()

    if not staff_user:
        return jsonify({
            "message": "Staff not found"
        }), 404

    data = request.get_json()

    staff_user.name = data.get("name")
    staff_user.email = data.get("email")
    staff_user.phone = data.get("phone")

    staff_profile = StaffProfile.query.filter_by(user_id=staff_user.id).first()

    if staff_profile:

        staff_profile.experience_years = data.get(
            "experience_years"
        )

        staff_profile.specialization = data.get(
            "specialization"
        )

    db.session.commit()

    return jsonify({
        "message": "Staff updated successfully"
    }), 200

@app.route("/api/admin/create-trek", methods=["POST"])
@jwt_required()
def create_trek():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    data = request.get_json()

    staff = StaffProfile.query.get(data.get("assigned_staff_id"))

    if not staff:
        return jsonify({
            "message": "Assigned staff not found"
        }), 404

    new_trek = Trek(trek_name=data.get("trek_name"),location=data.get("location"),difficulty=data.get("difficulty"),duration_days=data.get("duration_days"),available_slots=data.get("available_slots"),assigned_staff_id=data.get("assigned_staff_id"),start_date=datetime.strptime(data.get("start_date"),"%Y-%m-%d").date(),end_date=datetime.strptime(data.get("end_date"),"%Y-%m-%d").date(),price=data.get("price"))

    db.session.add(new_trek)
    db.session.commit()

    return jsonify({
        "message": "Trek created successfully"
    }), 201

@app.route("/api/admin/treks", methods=["GET"])
@jwt_required()
def get_treks():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

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

@app.route("/api/admin/update-trek/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek(trek_id):

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404
    
    data = request.get_json()
    staff = StaffProfile.query.get(data.get("assigned_staff_id"))

    if not staff:
        return jsonify({
            "message": "Assigned staff not found"
        }), 404
    
    trek.trek_name = data.get("trek_name")
    trek.location = data.get("location")
    trek.difficulty = data.get("difficulty")
    trek.duration_days = data.get("duration_days")
    trek.available_slots = data.get("available_slots")
    trek.assigned_staff_id = data.get("assigned_staff_id")

    trek.start_date = datetime.strptime(data.get("start_date"),"%Y-%m-%d").date()

    trek.end_date = datetime.strptime(data.get("end_date"),"%Y-%m-%d").date()

    trek.price = data.get("price")

    trek.status = data.get("status")

    db.session.commit()

    return jsonify({
        "message": "Trek updated successfully"
    }), 200

@app.route("/api/admin/delete-trek/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek(trek_id):

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    trek = Trek.query.get(trek_id)

    if not trek:
        return jsonify({
            "message": "Trek not found"
        }), 404
    
    db.session.delete(trek)
    
    db.session.commit()
    
    return jsonify({
        "message": "Trek deleted successfully"
    }), 200

@app.route("/api/admin/users", methods=["GET"])
@jwt_required()
def get_users():

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

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

@app.route("/api/admin/toggle-blacklist/<int:user_id>", methods=["PUT"])
@jwt_required()
def toggle_blacklist(user_id):

    admin = admin_required()

    if not admin:
        return jsonify({
            "message": "Access Denied"
        }), 403

    user = User.query.filter_by(id=user_id,role="user").first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    user.is_blacklisted = not user.is_blacklisted

    db.session.commit()

    return jsonify({
        "message": "Blacklist status updated",
        "is_blacklisted": user.is_blacklisted
    }), 200

@app.route("/api/user/dashboard")
@jwt_required()
def user_dashboard():

    user = user_required()

    if not user:
        return jsonify({
            "message": "Access Denied"
        }), 403

    return jsonify({
        "message": "Welcome User",
        "user": user.email
    }), 200


if __name__ == "__main__":
    app.run(debug=True)