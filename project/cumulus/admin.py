from django.contrib import admin

from project.cumulus.models import Data, DailyData


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        "real_datetime",
        "temperature",
        "humidity",
        "wind_speed",
        "wind_direction",
        "barometer",
        "rain_per_hour",
    )
    list_filter = ("real_datetime",)


@admin.register(DailyData)
class DailyDataAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "max_temp",
        "min_temp",
        "avg_temp",
        "min_humidity",
        "max_humidity",
        "avg_humidity",
        "min_wind_speed",
        "max_wind_speed",
        "avg_wind_speed",
        "min_barometer",
        "max_barometer",
        "avg_barometer",
        "total_rainfall",
        "avg_wind_direction",
    )
    list_filter = ("date",)

    readonly_fields = (
        "date",
        "max_temp",
        "min_temp",
        "avg_temp",
        "min_humidity",
        "max_humidity",
        "avg_humidity",
        "min_wind_speed",
        "max_wind_speed",
        "avg_wind_speed",
        "min_barometer",
        "max_barometer",
        "avg_barometer",
        "total_rainfall",
        "avg_wind_direction",
    )

    def has_add_permission(self, request):
        return False
