from django.contrib import admin

from project.cumulus.models import Data


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        'real_datetime', 'temperature', 'humidity', 'wind_speed', 'wind_direction', 'barometer', 'rain_per_hour'
    )
    list_filter = ('real_datetime', )
