from clients.models import Client
from .models import Notification
from django.core.mail import EmailMessage, get_connection
from twilio.rest import Client as TwilioClient
from django.conf import settings




def send_email_reminder(client_id):
    """
    Send email reminder to the client about their upcoming tax due date.
    """
    client = Client.objects.get(id=client_id)
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=True
    )

    sender_name = "Madame Toumno"
    from_email = f"{sender_name} <{settings.DEFAULT_FROM_EMAIL}>"
    email_body =  f"""
    <html>
        <body>
            <p>Dear {client.first_name} {client.last_name},</p>

           <p>This is just a friendly message to remind yo pay your tax due date</p>

            <p>Best regards,<br>
            {sender_name}</p>
        </body>
    </html>
    """
    


    email = EmailMessage(
        subject="Your Tax Payment Reminder",
        body=email_body,
        from_email=from_email,
        to=[client.email],
        connection=connection
    )

    email.content_subtype = "html"


    # Send the email
    email.send()

def send_sms_reminder(client_id):
    """
    Send SMS reminder to the client about their upcoming tax due date.
    """
    client = Client.objects.get(id=client_id)
    client_twilio = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # Send SMS to the client
    message = client_twilio.messages.create(
        body=f"Dear {client.last_name}, just to remind you to pay your tax before due date. From Madame Toumno",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=client.telephone_number
    )
    
    # Create a record for this notification in the database
    Notification.objects.create(client=client, notification_type='sms', status='sent')
    return f"SMS sent to {client.telephone_number}"
