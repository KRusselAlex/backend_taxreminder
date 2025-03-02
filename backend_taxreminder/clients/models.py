from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone_number = models.CharField(max_length=15, unique=True)
    date_tax = models.DateField(null=False, blank=False)



    def __str__(self):
        return self.full_name
