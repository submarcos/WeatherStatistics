from django.db import models


class Data(models.Model):
    real_datetime = models.DateTimeField(db_index=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_bearing_degrees = models.FloatField()
    rain_per_hour = models.FloatField()
    barometer = models.FloatField()
    wind_direction = models.CharField(max_length=3)
    wind_speed_beaufort = models.PositiveIntegerField()
    heat_index = models.FloatField()
    humidex = models.FloatField()
    uv_index = models.FloatField()

    class Meta:
        ordering = (
            '-real_datetime',
        )


class DailyData(models.Model):
    date = models.DateField(unique=True, db_index=True)
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    avg_temp = models.FloatField()
    min_humidity = models.FloatField()
    max_humidity = models.FloatField()
    avg_humidity = models.FloatField()
    min_barometer = models.FloatField()
    max_barometer = models.FloatField()
    avg_barometer = models.FloatField()
    min_wind_speed = models.FloatField()
    max_wind_speed = models.FloatField()
    avg_wind_speed = models.FloatField()
    total_rainfall = models.FloatField()
