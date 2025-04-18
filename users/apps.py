from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv

load_dotenv()

def create_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            username=os.getenv('DJANGO_ADMIN_USERNAME', 'admin'),
            email=os.getenv('DJANGO_ADMIN_EMAIL', 'admin@example.com'),
            password=os.getenv('DJANGO_ADMIN_PASSWORD', 'admin123')
        )

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.apps import apps
        if apps.ready:
            post_migrate.connect(create_admin_user, sender=self)
