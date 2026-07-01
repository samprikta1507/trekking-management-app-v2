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
        'schedule': crontab(hour=9, minute=0),
    },
    'send-monthly-activity-report': {
        'task': 'tasks.reminder_tasks.monthly_activity_report',
        'schedule': crontab(day_of_month='1', hour=8, minute=0),
    },
}
celery.conf.timezone = 'Asia/Kolkata'

import tasks.test_tasks
import tasks.reminder_tasks