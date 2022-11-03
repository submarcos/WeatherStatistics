from django.contrib import admin

from project.cumulus.models import Data


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        'real_datetime', 'temperature', 'humidity', 'windspeed', 'wind_direction', 'barometer', 'rain_per_hour'
    )
