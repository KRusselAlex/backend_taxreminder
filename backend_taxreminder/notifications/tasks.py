from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.utils import timezone
from datetime import timedelta, datetime
from clients.models import Client
from celery import shared_task
from .models import Notification
from django.core.mail import send_mail
from twilio.rest import Client as TwilioClient
from django.conf import settings
import json

@shared_task
def send_email_reminder(client_id):
    """
    Send email reminder to the client about their upcoming tax due date.
    """
    client = Client.objects.get(id=client_id)
    subject = "Tax Payment Reminder"
    message = f"Dear {client.full_name}, your tax payment is due on {client.date_tax}. Please make the payment."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [client.email])
    
    # Create a record for this notification in the database
    Notification.objects.create(client=client, notification_type='email', status='sent')
    return f"Email sent to {client.email}"

@shared_task
def send_sms_reminder(client_id):
    """
    Send SMS reminder to the client about their upcoming tax due date.
    """
    client = Client.objects.get(id=client_id)
    client_twilio = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Send SMS to the client
    message = client_twilio.messages.create(
        body=f"Reminder: Your tax is due on {client.date_tax}.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=client.telephone_number
    )
    
    # Create a record for this notification in the database
    Notification.objects.create(client=client, notification_type='sms', status='sent')
    return f"SMS sent to {client.telephone_number}"


@shared_task
def send_reminder_weekly(*args, **kwargs):
    """
    Send email and SMS reminders for clients whose tax date (month and day) is one week away from today.
    """
    try:
        today = timezone.now().date()
        today_month_day = today.replace(year=2000)  # Set the year to a dummy value (2000) to ignore the year
        reminder_date = today + timedelta(days=7)  # Calculate one week from today
        reminder_month_day = reminder_date.replace(year=2000)  # Set year to ignore it for comparison

        # Find clients whose tax date (month and day) is exactly one week from today
        clients_to_remind = Client.objects.filter(date_tax__month=reminder_month_day.month,
                                                  date_tax__day=reminder_month_day.day)
        
        tasks_triggered = 0
        for client in clients_to_remind:
            send_email_reminder.delay(client.id)  # Trigger email reminder task asynchronously
            send_sms_reminder.delay(client.id)  # Trigger SMS reminder task asynchronously
            tasks_triggered += 2  # One for email, one for SMS

        return f"Triggered {tasks_triggered} reminders for {clients_to_remind.count()} clients for the day {reminder_month_day.day} and month. {reminder_month_day.month}"
    
    except Exception as e:
        print(e)
