from flask import Flask, request, jsonify
from models import db, User, StaffProfile, Trek, Booking
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

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

if __name__ == "__main__":
    app.run(debug=True)