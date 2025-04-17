from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def send_report_to_user(client, report):
    """
    Sends a tax report to the given user via email.
    """
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

            <p>Thank you for trusting us with your business. Attached is your tax report for this period.</p>

            <p>If you have any questions or require further assistance, feel free to reach out to us. We appreciate your continued partnership and look forward to working with you in the future.</p>

            <p>Best regards,<br>
            {sender_name}</p>
        </body>
    </html>
    """
    


    email = EmailMessage(
        subject="Your Tax Report",
        body=email_body,
        from_email=from_email,
        to=[client.email],
        connection=connection
    )

    email.content_subtype = "html"

    with open(report.file.path, "rb") as pdf_file:
        email.attach(report.file.name, pdf_file.read(), "application/pdf")
   

    # Send the email
    email.send()
