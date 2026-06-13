from celery_worker import celery
from datetime import date, timedelta

@celery.task
def daily_trek_reminder():

    tomorrow = date.today() + timedelta(days=1)

    print(f"Checking treks for {tomorrow}")

    return "Reminder Job Completed"