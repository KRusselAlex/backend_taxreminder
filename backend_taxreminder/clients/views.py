from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from .permissions import CustomIsAuthenticated
from .serializers import ClientSerializer
from .models import Client
from .utils.responses import format_response  # Import the format_response function

class ClientCreateView(generics.ListCreateAPIView):
    """
    Register a new client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [CustomIsAuthenticated]

    @swagger_auto_schema(
        operation_description="Register a new client with full name, email, and telephone number.",
        request_body=ClientSerializer,
        responses={
            201: "Client created successfully",
            400: "Invalid input",
            401: "Unauthorized",
        }
    )
    def post(self, request, *args, **kwargs):
        # Use the serializer to validate and handle errors
        multiple = isinstance(request.data, list)  # Check if the request contains a list
        serializer = ClientSerializer(data=request.data, many=multiple)

        if serializer.is_valid():
            # If the serializer is valid, create the client
            serializer.save()
            return format_response(
                data=serializer.data,
                message="Client created successfully",
                status_code=status.HTTP_201_CREATED,
                success=True
            )
        # If invalid, return the error messages directly from the serializer
        return format_response(
            errors=serializer.errors,
            message="Client registration failed",
            status_code=status.HTTP_400_BAD_REQUEST,
            success=False  # Indicating failure
        )
        
    @swagger_auto_schema(
        operation_description="Retrieve a list of all clients. Requires authentication.",
        responses={
            200: ClientSerializer(many=True),
            401: "Unauthorized",
        }
    )
    
    def get(self, request, *args, **kwargs):
        clients = self.get_queryset()
        serializer = self.get_serializer(clients, many=True)
        return format_response(
            data = serializer.data ,
            message="Client list retrieved successfully",
            status_code=status.HTTP_200_OK,
            success=True
        )


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [CustomIsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific client by ID. Requires authentication.",
        responses={
            200: ClientSerializer(),
            401: "Unauthorized",
            404: "Client not found",
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
        except:
            return format_response(
            errors={'detail': 'Client not found'},
            message="Client not found",
            status_code=status.HTTP_404_NOT_FOUND,
            success=False  # Indicating failure
        )
        
        if response.status_code == 200:
            return format_response(
                data=response.data,
                message="Client details retrieved",
                status_code=status.HTTP_200_OK,
                success=True
            )
        

    @swagger_auto_schema(
        operation_description="Update client details by ID. Requires authentication.",
        request_body=ClientSerializer,
        responses={
            200: "Client updated successfully",
            400: "Invalid input",
            401: "Unauthorized",
            404: "Client not found",
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print("request",request.data)
        try:
            response = super().update(request, *args, **kwargs)
        except Exception as error:  
            return format_response(
                errors={'detail': str(error)},  # Ensure error is converted to string for clarity
                message="There is an error",
                status_code=status.HTTP_404_NOT_FOUND,
                success=False  # Indicating failure
                )
        if response.status_code == 200:
             return format_response(
                 data=response.data,
                 message="Client updated successfully",
                 status_code=status.HTTP_200_OK,
                 success=True
             )

    @swagger_auto_schema(
        operation_description="Delete a specific client by ID. Requires authentication.",
        responses={
            204: "Client deleted successfully",
            401: "Unauthorized",
            404: "Client not found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
        except Http404: 
            return format_response(
                errors={'detail': 'Client not found'},
                message="Client not found",
                status_code=status.HTTP_404_NOT_FOUND,
                success=False
            )

        if response.status_code == 204:
            return format_response(
                message="Client deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT,
                success=True
            )

        return response