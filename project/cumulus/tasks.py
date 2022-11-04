from celery import shared_task
from django.db.models import Min, Max, Avg, Sum, Count
from django.db.models.functions import TruncDate
from django.views.generic.dates import timezone_today

from project.cumulus.data import get_realtime
from project.cumulus.models import Data, DailyData


@shared_task
def get_weather_data():
    get_realtime()
    return True


@shared_task
def compile_daily_data():
    # get day data not compiled
    data = Data.objects.filter(daily_data__isnull=True).exclude(real_datetime__day=timezone_today()).order_by("real_datetime")
    days = data.annotate(day=TruncDate("real_datetime")).values("day").distinct()

    for day in days:
        day_data = data.filter(real_datetime__date=day["day"])
        avg_wind_direction = (
            day_data.order_by("wind_direction")
            .values("wind_direction")
            .alias(count=Count("wind_direction"))
            .order_by("-count")
        )
        avg = str(avg_wind_direction[0]["wind_direction"])
        compiled_data = day_data.aggregate(
            min_temp=Min("temperature"),
            max_temp=Max("temperature"),
            avg_temp=Avg("temperature"),
            min_humidity=Min("humidity"),
            max_humidity=Max("humidity"),
            avg_humidity=Avg("humidity"),
            min_barometer=Min("barometer"),
            max_barometer=Max("barometer"),
            avg_barometer=Avg("barometer"),
            min_wind_speed=Min("wind_speed"),
            max_wind_speed=Max("wind_speed"),
            avg_wind_speed=Avg("wind_speed"),
            total_rainfall=Sum("rain_per_hour"),
        )

        daily_data_instance = DailyData.objects.create(
            date=day["day"], avg_wind_direction=avg, **compiled_data
        )
        day_data.update(daily_data=daily_data_instance)
    return True
