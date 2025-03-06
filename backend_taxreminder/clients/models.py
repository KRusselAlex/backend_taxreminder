from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone_number = models.CharField(max_length=15, unique=True)
    date_tax = models.DateField(null=True, blank=True)
    type_clients= models.CharField(max_length=255,default="individual")




    def __str__(self):
        return self.full_name
