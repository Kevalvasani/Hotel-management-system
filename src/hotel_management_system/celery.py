from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_management_system.settings")

app = Celery("hotel_management_system")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "send_rating_reminder": {
        "task": "booking.tasks.send_rating_reminder",
        "schedule": crontab(hour=12, minute=0),
        # 'schedule': timedelta(days=1, hours=21, minutes=50),  # 9:50 PM every day
    }
}

# celery -A hotel_management_system worker -l info
# celery -A hotel_management_system beat -l info