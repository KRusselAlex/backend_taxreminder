"""
WSGI config for backend_taxreminder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_taxreminder.settings')

# application = get_wsgi_application()
application = StaticFilesHandler(get_wsgi_application())
# application = DjangoWhiteNoise(application)


