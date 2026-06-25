from flask import Flask, request, jsonify
from models import db, User, StaffProfile, Trek, Booking
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from extensions import cache

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.trek_routes import trek_bp
from routes.admin_user_routes import user_bp
from routes.user_routes import user_dashboard_bp
from routes.staff_routes import staff_bp
from routes.test_routes import test_bp
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my-secret-key"

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1 
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache.init_app(app)
CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(trek_bp)
app.register_blueprint(user_bp)
app.register_blueprint(user_dashboard_bp)
app.register_blueprint(staff_bp,url_prefix="/api/staff")
app.register_blueprint(test_bp)

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