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


# app.conf.beat_schedule = {
#     'add-every-2-hour':{
#         'task':'notifications.tasks.send_reminder_weekly',
#         'schedule': crontab(minute='0', hour='0'),
        
#     }
# }

app.conf.beat_schedule = {
    # Reminder tasks for salaried clients
    'send-salaried-reminders': {
        'task': 'notifications.tasks.send_salaried_reminders',
        'schedule': crontab(minute=0, hour=12, day_of_month=31, month_of_year=12),  # 31 December
    },
    'send-salaried-relances': {
        'task': 'notifications.tasks.send_salaried_relances',
        'schedule': crontab(minute=0, hour=12, day_of_month=31, month_of_year=1),  # 31 January
    },
      'send-salaried-february-relances': {
        'task': 'notifications.tasks.send_salaried_final_relances',
        'schedule': crontab(minute=0, hour=12, day_of_month=28, month_of_year=2),  # february relances
    },

    'send-salaried-final-relances': {
        'task': 'notifications.tasks.send_salaried_final_relances',
        'schedule': crontab(minute=0, hour=12, day_of_month='10,20,25,31', month_of_year=3),  # March relances
    },

    # Reminder tasks for companies
       'send-company-reminders-january': {
        'task': 'notifications.tasks.send_company_reminders',
        'schedule': crontab(minute=0, hour=12, day_of_month="1,15", month_of_year=1),  # 1er et 15 janvier
    },

    # Rappels pour les déclarations des mois de janvier, février et mars
    'send-company-reminders-april': {
        'task': 'notifications.tasks.send_company_reminders',
        'schedule': crontab(minute=0, hour=12, day_of_month="1,15", month_of_year=4),  # 1er et 15 avril
    },

    # Rappels pour les déclarations des mois d'avril, mai et juin
    'send-company-reminders-july': {
        'task': 'notifications.tasks.send_company_reminders',
        'schedule': crontab(minute=0, hour=12, day_of_month="1,15", month_of_year=7),  # 1er et 15 juillet
    },

    # Rappels pour les déclarations des mois juillet, août et septembre
    'send-company-reminders-october': {
        'task': 'notifications.tasks.send_company_reminders',
        'schedule': crontab(minute=0, hour=12, day_of_month="1,15", month_of_year=10),  # 1er et 15 october
    },

    # Reset report_sent for salaried clients on 31st December
    'reset-salaried-report-sent': {
        'task': 'notifications.tasks.reset_report_sent_salaried',
        'schedule': crontab(minute=0, hour=12, day_of_month=31, month_of_year=12),  # 31 December
    },
  
    # Réinitialisation du flag report_sent pour les entreprises
    'reset-report-sent-company': {
        'task': 'notifications.tasks.reset_report_sent_company',
        'schedule': crontab(minute=0, hour=12),  # Cette tâche s'exécute chaque jour à minuit
    }
}

# @app.task(bind=True)
# def print_hello(*args, **kwargs):
#     print("hello taksed donne")
