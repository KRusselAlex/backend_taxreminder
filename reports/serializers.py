from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "clients", "file", "created_at"]
        read_only_fields = ["id", "created_at"]
