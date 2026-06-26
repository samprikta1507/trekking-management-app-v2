from flask import Blueprint, jsonify
from tasks.test_tasks import test_task
from tasks.reminder_tasks import daily_trek_reminder, monthly_activity_report

from flask_mail import Message
from extensions import mail

test_bp = Blueprint("test_bp", __name__)

@test_bp.route("/api/test-task")
def run_test_task():

    test_task.delay()

    return jsonify({
        "message": "Task sent successfully"
    })


@test_bp.route("/api/test-reminder")
def run_reminder():

    daily_trek_reminder.delay()

    return jsonify({
        "message": "Reminder task sent"
    })

@test_bp.route("/api/test-report")
def run_report():
    monthly_activity_report.delay()
    return jsonify({"message": "Report task sent"})

@test_bp.route('/api/test-email', methods=['GET'])
def send_test_email():

    msg = Message(
        subject="Success! My First MailHog Email",
        sender="admin@trek.com",
        recipients=["samprikta@example.com"],
        body="Hello everything is working perfectly."
    )
    
    mail.send(msg)
    
    return jsonify({"message": "Email fired into MailHog!"}), 200