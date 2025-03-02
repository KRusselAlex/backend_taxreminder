# /home/kouawou/womga/impots_project/backend_taxreminder/backend_taxreminder/celery.py
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_taxreminder.settings')

# Create the app
app = Celery('backend_taxreminder')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

