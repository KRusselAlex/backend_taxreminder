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
    message = f"Dear {client.full_name}, your tax payment is due on . Please make the payment."
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
        body=f"Reminder: Your tax is due on .",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=client.telephone_number
    )
    
    print(message,"message twillo")

    # Create a record for this notification in the database
    Notification.objects.create(client=client, notification_type='sms', status='sent')
    return f"SMS sent to {client.telephone_number}"
