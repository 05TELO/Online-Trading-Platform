import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "run-every-3-hours": {
        "task": "online_trading_platform.tasks.increase_debt",
        "schedule": crontab(hour="*/3"),
    },
    'run-at-6:30-every-day': {
        'task': 'online_trading_platform.tasks.reduce_debt',
        'schedule': crontab(hour=6, minute=30),
    },
}

app.autodiscover_tasks()
