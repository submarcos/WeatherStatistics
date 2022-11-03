import os

from celery import Celery

app = Celery("project")

BROKER_URL = f'redis://{os.getenv("REDIS_HOST", "redis")}:{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "0")}'

app.conf.update(
    enable_utc=True,
    accept_content=['json'],
    broker_url=BROKER_URL,
    task_serializer='json',
    result_serializer='json',
    result_expires=5,
    result_backend='django-db',
    cache_backend='django-cache',
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
    result_extended=True,
    task_track_started=True,
)

app.autodiscover_tasks()
