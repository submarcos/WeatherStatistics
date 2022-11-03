import datetime
from zoneinfo import ZoneInfo

import requests

from project.cumulus.models import Data

# https://cumuluswiki.org/a/Realtime.txt
MAPPING = {
    0: "date",
    1: "time",
    2: "outside_temperature",
    3: "relative_humidity",
    4: "dew_point",
    5: "wind_speed_average",
    6: "latest_wind_speed_reading",
    7: "wind_bearing_degrees",
    8: "current_rain_rate_per_hour",
    9: "rain_today",
    10: "barometer_sea_level_pressure",
    11: "wind_direction_compass",
    12: "wind_speed_beaufort",
    13: "wind_unit",
    14: "temperature_unit",
    15: "pressure_unit",
    16: "rain_unit",
    17: "wind_run_today",
    18: "pressure_trend_three_hours",
    19: "monthly_rainfall",
    20: "yearly_rainfall",
    21: "yesterday_rainfall",
    22: "inside_temperature",
    23: "inside_humidity",
    24: "windchill",
    25: "temperature_trend_three_hours",
    26: "today_high_temp",
    27: "time_today_high_temp",
    28: "today_low_temp",
    29: "time_today_low_temp",
    30: "today_high_wind_speed",
    31: "time_today_high_wind_speed",
    32: "today_high_wind_gust",
    33: "time_today_high_wind_gust",
    34: "today_high_pressure",
    35: "time_today_high_pressure",
    36: "today_low_pressure",
    37: "time_today_low_pressure",
    38: "cumulus_version",
    39: "cumulus_build_number",
    40: "10_minutes_high_gust",
    41: "heat_index",
    42: "humidex",
    43: "UV_index",
    44: "evapotranspiration_today",
    45: "solar_radiation_W_M2",
    46: "10_minutes_average_wind_bearing_degrees",
    47: "last_hour_rainfall",
    48: "forecast_number",
    49: "is_daylight",
    50: "sensor_contact_lost",
    51: "average_wind_direction",
    52: "cloud_base",
    53: "cloud_base_unit",
    54: "apparent_temperature",
    55: "sunshine_hours",
    56: "current_solar_max_radiation",
    57: "is_it_sunny",
    58: "feels_like"
}

REALTIME_URL = "http://weather.oadf.fr/realtime.txt"
TIMEZONE = "Europe/Paris"


def remap(data):
    """ map data as dict """
    final_dict = {}
    for i in range(len(data)):
        final_dict[MAPPING[i]] = data[i]
    return final_dict


def _get_data():
    """ Get data from cumulus realtime.txt """
    response = requests.get(REALTIME_URL)
    data = response.content.decode().split(" ")
    return data


def get_realtime():
    """ Get latest data from cumulus """
    data = _get_data()
    final_values = remap(data)
    for key, value in final_values.items():
        print(f"{key}: {value}")
    real_datetime = datetime.datetime.strptime(f"{final_values['date']} {final_values['time']}",
                                               "%d/%m/%y %H:%M:%S")
    tz_real_datetime = datetime.datetime(
        year=real_datetime.year, month=real_datetime.month, day=real_datetime.day,
        hour=real_datetime.hour, minute=real_datetime.minute, second=real_datetime.second,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    Data.objects.create(
        real_datetime=tz_real_datetime,
        temperature=float(final_values['outside_temperature']),
        humidity=float(final_values['relative_humidity']),
        wind_speed=float(final_values['latest_wind_speed_reading']),
        wind_bearing_degrees=float(final_values['wind_bearing_degrees']),
        rain_per_hour=float(final_values['current_rain_rate_per_hour']),
        barometer=float(final_values['barometer_sea_level_pressure']),
        wind_direction=final_values['wind_direction_compass'],
        wind_speed_beaufort=int(final_values['wind_speed_beaufort']),
        heat_index=float(final_values['heat_index']),
        humidex=float(final_values['humidex']),
        uv_index=float(final_values['UV_index']),
    )
