from rest_framework import serializers

from .. import models


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Data
        fields = "__all__"


class DailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyData
        fields = "__all__"
