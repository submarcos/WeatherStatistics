from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets

from .. import models
from . import serializers


class DataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Data.objects.all()
    serializer_class = serializers.DataSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("wind_direction", "daily_data__date")


class DailyDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.DailyData.objects.all()
    serializer_class = serializers.DailyDataSerializer
    pagination_class = pagination.PageNumberPagination
