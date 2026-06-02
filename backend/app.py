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

    current_user = get_jwt_identity()

    return jsonify({
        "message": "Welcome Admin",
        "user": current_user
    })

@app.route("/api/user/dashboard")
@jwt_required()
def user_dashboard():

    current_user = get_jwt_identity()

    return jsonify({
        "message": "Welcome User",
        "user": current_user
    })



if __name__ == "__main__":
    app.run(debug=True)