from django.urls import path, include
from planetarium.views import *
from rest_framework import routers

app_name = "planetarium"

router = routers.DefaultRouter()

router.register("planetarium-dome", PlanetariumDomeViewSet)
router.register("ticket", TicketViewSet)
router.register("show-session", ShowSessionViewSet)
router.register("theme", ShowThemeViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]