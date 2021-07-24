from django.urls import include, path
from . import views

app_name = 'broadcasts'

urlpatterns = [
    path('', views.broadcasts_views, name='broadcasts'),
]
