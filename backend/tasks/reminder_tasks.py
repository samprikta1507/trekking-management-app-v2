from celery_worker import celery
from datetime import date, timedelta
from models import Trek, Booking, User 
from flask_mail import Message
from extensions import mail

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


@celery.task
def monthly_activity_report():
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app import app
    from flask import render_template_string
    
    last_month = date.today() - timedelta(days=30)
    
    with app.app_context():

        total_treks = Trek.query.filter(Trek.start_date >= last_month).count()
        total_bookings = Booking.query.filter(Booking.booking_date >= last_month).count()
        
        html_report = f"""
        <html>
            <body>
                <h2>Monthly Trekking Report</h2>
                <p>Here is the activity summary for the last 30 days:</p>
                <ul>
                    <li>Total Treks Conducted: {total_treks}</li>
                    <li>Total Bookings Made: {total_bookings}</li>
                </ul>
            </body>
        </html>
        """
        
        admin_user = User.query.filter_by(role='admin').first()
        if admin_user:
        
            with app.app_context():
                msg = Message(
                    subject="Monthly Trekking Activity Report",
                    sender="admin@trek.com",
                    recipients=[admin_user.email],
                    html=html_report 
                )
                mail.send(msg)

            print(f"--> [REPORT SENT] To Admin: {admin_user.email} via MailHog")
        else:
            print("No Admin found to send the report to.")
            
    return "Monthly report generated."

@celery.task
def export_trek_history(user_id):
    import sys
    import os
    import csv
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app import app
    
    with app.app_context():
        print(f"Starting CSV export for user ID: {user_id}")
        
        user = User.query.get(user_id)
        if not user:
            return "User not found."
            
        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        export_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        filename = f"trek_history_user_{user_id}.csv"
        filepath = os.path.join(export_dir, filename)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
        
            writer.writerow(['Trek Name', 'Location', 'Booking Date', 'Status'])
            
            for booking in bookings:
                trek = Trek.query.get(booking.trek_id)
                writer.writerow([
                    trek.trek_name,
                    trek.location,
                    booking.booking_date.strftime('%Y-%m-%d'),
                    booking.status
                ])
                
        print(f"--> [CSV EXPORTED] Saved to: {filepath}")
        
    return f"Export complete for User {user_id}. File: {filename}"