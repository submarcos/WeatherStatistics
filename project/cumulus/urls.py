from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import api, views

router = SimpleRouter()
router.register("data", api.DataViewSet, basename="data")
router.register("daily-data", api.DailyDataViewSet, basename="daily-data")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.HomeView.as_view(), name="home"),
]
