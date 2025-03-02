# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from django.utils import timezone
# from datetime import timedelta
# from clients.models import Client
# from celery import shared_task
# import json

# @shared_task
# def schedule_tax_reminders():
#     """
#     Check all clients and schedule tax reminders for t
#     hose whose tax is due in 1 month.
#     """
#     now = timezone.now()
#     reminder_date = now + timedelta(days=30)  # 1 month from now

#     clients_to_remind = Client.objects.filter(date_tax=reminder_date.date())  # Filter clients whose tax is due in 1 month

#     for client in clients_to_remind:
#         # Schedule the email reminder task
#         PeriodicTask.objects.create(
#             name=f"Email Reminder for {client.full_name}",
#             task="app_name.services.send_email_reminder",  # Your Celery task name
#             args=json.dumps([client.id]),
#             start_time=reminder_date,
#             one_off=True  # Ensure this task only runs once
#         )

#         # Schedule the SMS reminder task
#         PeriodicTask.objects.create(
#             name=f"SMS Reminder for {client.full_name}",
#             task="app_name.services.send_sms_reminder",  # Your Celery task name
#             args=json.dumps([client.id]),
#             start_time=reminder_date,
#             one_off=True  # Ensure this task only runs once
#         )
# tasks.py
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
def schedule_tax_reminders_for_today():
    """
    Schedule email and SMS reminders at 10:20 AM today for clients with today's tax date.
    """
    # Get today's date
    today = timezone.now().date()
    
    # Create a datetime for today at 10:20 AM
    reminder_time = datetime.combine(today, datetime.strptime("11:01", "%H:%M").time())
    reminder_time = timezone.make_aware(reminder_time)
    
    # Find clients whose tax date is today
    clients_to_remind = Client.objects.filter(date_tax=today)
    
    tasks_created = 0
    for client in clients_to_remind:
        # Create a clocked schedule for 10:20 AM
        clock_schedule = ClockedSchedule.objects.create(
            clocked_time=reminder_time
        )
        
        # Schedule the email reminder task
        PeriodicTask.objects.create(
            name=f"Email Reminder for {client.full_name} - {today}",
            task="backend_taxreminder.tasks.send_email_reminder",  # Update with your actual app name
            args=json.dumps([client.id]),
            clocked=clock_schedule,
            one_off=True  # Ensure this task only runs once
        )
        tasks_created += 1

        # Schedule the SMS reminder task
        clock_schedule_sms = ClockedSchedule.objects.create(
            clocked_time=reminder_time
        )
        
        PeriodicTask.objects.create(
            name=f"SMS Reminder for {client.full_name} - {today}",
            task="backend_taxreminder.tasks.send_sms_reminder",  # Update with your actual app name
            args=json.dumps([client.id]),
            clocked=clock_schedule_sms,
            one_off=True  # Ensure this task only runs once
        )
        tasks_created += 1

    return f"Scheduled {tasks_created} reminders for {clients_to_remind.count()} clients at 10:20 AM today"

# For immediate testing, you can add this function
@shared_task
def send_immediate_reminders():
    """
    Immediately send reminders to all clients with today's tax date without scheduling.
    For testing purposes.
    """
    today = timezone.now().date()
    clients_to_remind = Client.objects.filter(date_tax=today)
    
    results = []
    for client in clients_to_remind:
        # Send email and SMS immediately
        email_result = send_email_reminder(client.id)
        sms_result = send_sms_reminder(client.id)
        results.append(f"{client.full_name}: {email_result}, {sms_result}")
    
    return f"Sent immediate reminders to {len(results)} clients: {'; '.join(results)}"