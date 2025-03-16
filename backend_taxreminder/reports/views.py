from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .permissions import CustomIsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Report
from .serializers import ReportSerializer
from .services import send_report_to_user
from clients.models import Client
from .utils.responses import format_response  # Import response formatter

class ReportListCreateView(generics.ListCreateAPIView):
    """
    API to list all reports and send a new report via email.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [CustomIsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all reports that have been sent.",
        responses={200: ReportSerializer(many=True),  401: "Unauthorized"
           }
    )
    def get(self, request, *args, **kwargs):
        reports = self.get_queryset()
        serializer = self.get_serializer(reports, many=True)
        return format_response(
            data=serializer.data,
            message="Reports retrieved successfully",
            status_code=status.HTTP_200_OK,
            success=True
        )

    @swagger_auto_schema(
        operation_description="Upload a new report and send it via email.",
        request_body=ReportSerializer,
        responses={201: "Report sent successfully", 400: "Invalid data",  401: "Unauthorized",
            404: "reports not found"}
    )
    def post(self, request, *args, **kwargs):
        client_id = request.data.get("clients")  # Get client ID from request data
        client = get_object_or_404(Client, id=client_id)  # Look up the client from the database
        
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            report = serializer.save(clients=client)  # Assign the client to the report

            # Send email with report attachment
            send_report_to_user(client, report)

            return format_response(
                data=serializer.data,
                message="Report sent successfully",
                status_code=status.HTTP_201_CREATED,
                success=True
            )

        return format_response(
            errors=serializer.errors,
            message="Failed to send report",
            status_code=status.HTTP_400_BAD_REQUEST,
            success=False
        )

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API to retrieve, update, or delete a specific report.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [CustomIsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific report by ID.",
        responses={200: ReportSerializer(), 404: "Report not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
        except:
            return format_response(
                errors={'detail': 'Report not found'},
                message="Report not found",
                status_code=status.HTTP_404_NOT_FOUND,
                success=False
            )
        return format_response(
            data=response.data,
            message="Report retrieved successfully",
            status_code=status.HTTP_200_OK,
            success=True
        )

    @swagger_auto_schema(
        operation_description="Update an existing report.",
        request_body=ReportSerializer,
        responses={200: "Report updated successfully", 400: "Invalid data", 404: "Report not found"}
    )
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
        except:
            return format_response(
                errors={'detail': 'Report not found'},
                message="Report not found",
                status_code=status.HTTP_404_NOT_FOUND,
                success=False
            )
        return format_response(
            data=response.data,
            message="Report updated successfully",
            status_code=status.HTTP_200_OK,
            success=True
        )

    @swagger_auto_schema(
        operation_description="Delete a specific report by ID.",
        responses={204: "Report deleted successfully", 404: "Report not found"}
    )
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
        except:
            return format_response(
                errors={'detail': 'Report not found'},
                message="Report not found",
                status_code=status.HTTP_404_NOT_FOUND,
                success=False
            )
        return format_response(
            message="Report deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
            success=True
        )
