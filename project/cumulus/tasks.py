from celery import shared_task
from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import Round, TruncDate
from django.views.generic.dates import timezone_today

from project.cumulus.data import get_realtime
from project.cumulus.models import DailyData, Data


@shared_task
def get_weather_data():
    get_realtime()
    return True


@shared_task
def compile_daily_data():
    # get day data not compiled
    data = (
        Data.objects.filter(daily_data__isnull=True)
        .exclude(real_datetime__date=timezone_today())
        .order_by("real_datetime")
    )
    days = (
        data.annotate(day=TruncDate("real_datetime"))
        .order_by("day")
        .values("day")
        .distinct("day")
    )

    for day in days:
        day_data = data.filter(real_datetime__date=day["day"])
        avg_wind_direction = (
            day_data.order_by("wind_direction")
            .values("wind_direction")
            .alias(count=Count("wind_direction"))
            .order_by("-count")
        )
        avg = str(avg_wind_direction.first()["wind_direction"])
        compiled_data = day_data.aggregate(
            min_temp=Min("temperature"),
            max_temp=Max("temperature"),
            avg_temp=Round(Avg("temperature"), 2),
            min_humidity=Min("humidity"),
            max_humidity=Max("humidity"),
            avg_humidity=Round(Avg("humidity"), 2),
            min_barometer=Min("barometer"),
            max_barometer=Max("barometer"),
            avg_barometer=Round(Avg("barometer"), 2),
            min_wind_speed=Min("wind_speed"),
            max_wind_speed=Max("wind_speed"),
            avg_wind_speed=Round(Avg("wind_speed"), 2),
            total_rainfall=Sum("rain_per_hour"),
        )

        daily_data_instance = DailyData.objects.create(
            date=day["day"], avg_wind_direction=avg, **compiled_data
        )
        day_data.update(daily_data=daily_data_instance)
    return True
