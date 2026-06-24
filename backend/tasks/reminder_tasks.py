from celery_worker import celery
from datetime import date, timedelta
from models import Trek, Booking, User 

@celery.task
def daily_trek_reminder():
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from app import app  
    
    tomorrow = date.today() + timedelta(days=1)
    
    with app.app_context():
        upcoming_treks = Trek.query.filter_by(start_date=tomorrow).all()
        
        if not upcoming_treks:
            print(f"Checking for {tomorrow}: No treks scheduled.")
            return "No reminders needed today."

        for trek in upcoming_treks:
            print(f"Processing reminders for Trek: {trek.trek_name}")
            
            bookings = Booking.query.filter_by(trek_id=trek.id, status="Booked").all()
            
            for booking in bookings:
                user = User.query.get(booking.user_id)
                if user:
                    print(f"--> [EMAIL SENT] To: {user.email} | Subject: Reminder! '{trek.trek_name}' starts tomorrow!")

    return "Daily reminders processed successfully!"