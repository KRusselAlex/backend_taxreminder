from django.db import models
from clients.models import Client

class Report(models.Model):
    clients = models.ForeignKey(Client, on_delete=models.CASCADE)
    file = models.FileField(upload_to='static/reports/')
    created_at = models.DateTimeField(auto_now_add=True)
