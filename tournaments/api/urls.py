from django.urls import include, path
from rest_framework import routers

from tournaments.api import views

router = routers.DefaultRouter()
router.register(r'tournaments', views.TournamentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

]