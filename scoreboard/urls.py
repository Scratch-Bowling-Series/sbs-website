from django.urls import include, path
from . import views

app_name = 'scoreboard'

urlpatterns = [
    path('', views.scoreboard, name='index'),
]
