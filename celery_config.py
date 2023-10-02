from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hngx_s5.config.settings')

# Create a Celery instance with Django settings.
app = Celery('hngx_s5')



# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

from client import tasks

app.conf.broker_connection_retry_on_start = True
# Autodiscover tasks in all installed applications (optional).
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}').format(self.request)

