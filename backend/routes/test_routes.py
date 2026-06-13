from flask import Blueprint, jsonify
from tasks.test_tasks import test_task
from tasks.reminder_tasks import daily_trek_reminder

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