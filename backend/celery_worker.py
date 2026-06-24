from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "trekking_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.beat_schedule = {
    'send-daily-trek-reminders': {
        'task': 'tasks.reminder_tasks.daily_trek_reminder',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9:00 AM
    },
    'send-monthly-activity-report': {
        'task': 'tasks.reminder_tasks.monthly_activity_report',
        # Schedule it for the 1st day of every month at 8:00 AM
        'schedule': crontab(day_of_month='1', hour=8, minute=0),
    },
}
celery.conf.timezone = 'Asia/Kolkata'

import tasks.test_tasks
import tasks.reminder_tasks