from celery import Celery

celery = Celery(
    "trekking_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

import tasks.test_tasks
import tasks.reminder_tasks