from flask import Flask
from models import db, User, StaffProfile, Trek, Booking

app = Flask(__name__)

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
            password_hash="admin123",
            role="admin",
            phone="9999999999"
        )

        db.session.add(admin)
        db.session.commit()

  

if __name__ == "__main__":
    app.run(debug=True)