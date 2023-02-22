import os
from celery import Celery

"""
You have to provide a configuration for the Celery instance. Create a new file next
to the settings.py file of myshop and name it celery.py. This file will contain the
Celery configuration for your project. Add the following code to it:
"""
# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogue.settings')

app = Celery('catalogue')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()