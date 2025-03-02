from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from .models import  Notification
from clients.models import Client
from celery import shared_task
from django.utils import timezone

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

@shared_task
def send_sms_reminder(client_id):
    """
    Send SMS reminder to the client about their upcoming tax due date.
    """
    client = Client.objects.get(id=client_id)
    client_twilio = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Send SMS to the client
    message = client_twilio.messages.create(
        body=f"Reminder: Your tax is due on {client.date_tax}.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=client.telephone_number
    )

    # Create a record for this notification in the database
    Notification.objects.create(client=client, notification_type='sms', status='sent')
