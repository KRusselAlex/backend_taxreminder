from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from .permissions import CustomIsAuthenticated
from .services import send_email_reminder, send_sms_reminder  # Assuming these functions exist in a service file
from clients.models import Client
from .utils.responses import format_response  # Import response formatter


class NotificationCreateView(generics.CreateAPIView):
    """
    API to send a notification via email and SMS.
    """

    permission_classes = [CustomIsAuthenticated]

    @swagger_auto_schema(
        operation_description="Send a notification via email and SMS.",
        responses={
            201: "Notification sent successfully",
            400: "Invalid data",
            401: "Unauthorized",
            404: "Client not found"
        }
    )
    def post(self, request, *args, **kwargs):
        print("jenvoi")
        try:
            data = request.data
            client_id = data.get("client_id")


            if not client_id:
                return format_response(success=False, message="client_id is required", status_code=status.HTTP_400_BAD_REQUEST)

            client = get_object_or_404(Client, id=client_id)


            # Send email notification
            send_email_reminder(client.id)
            
            # Send SMS notification
            send_sms_reminder(client.id)

            
            return format_response(success=True, message="Notification sent successfully", status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return format_response(
                success=False,
                message="An error occurred while sending notifications.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=str(e)
            )
