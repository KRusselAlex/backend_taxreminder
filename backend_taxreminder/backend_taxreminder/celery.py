import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_taxreminder.settings')

# Create the app
app = Celery('backend_taxreminder')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')


# # Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'add-every-2-hour':{
        'task':'notifications.tasks.send_reminder_weekly',
        'schedule': crontab(minute='0', hour='0'),
        
    }
}


# @app.task(bind=True)
# def print_hello(*args, **kwargs):
#     print("hello taksed donne")
