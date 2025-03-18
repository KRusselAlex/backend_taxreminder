from rest_framework import serializers
from .models import Client
from rest_framework.validators import UniqueValidator

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'full_name', 'email', 'telephone_number','report_sent', 'type_client']
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=Client.objects.all())]},
            'telephone_number': {'validators': [UniqueValidator(queryset=Client.objects.all())]},
        }
        
    def create(self, validated_data):
        if isinstance(validated_data, list):  # If the request contains multiple objects
            return Client.objects.bulk_create([Client(**item) for item in validated_data])
        return super().create(validated_data)
