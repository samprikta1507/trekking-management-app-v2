from flask import Flask, request, jsonify
from models import db, User, StaffProfile, Trek, Booking
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

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