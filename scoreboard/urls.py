from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.scoreboard, name='index'),
]
