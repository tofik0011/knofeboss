import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unine_engine.settings')

app = Celery('unine_engine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'spam': {
        'task': 'apps.email_notifications.tasks.my_task',
        'schedule': crontab(minute='*/1')
    }
}
