from celery import shared_task

from project.cumulus.data import get_realtime


@shared_task
def get_weather_data():
    get_realtime()
    return True
