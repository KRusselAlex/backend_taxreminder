from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    Street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='Canada')
    email = models.EmailField(unique=True)
    telephone_number = models.CharField(max_length=15, unique=True)
    type_client= models.BooleanField(default=False)
    report_sent=models.BooleanField(default=False)
    date_report_sent=models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.full_name
