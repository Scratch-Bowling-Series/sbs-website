from django.urls import include, path
from . import views

app_name = 'merch'

urlpatterns = [
    path('', views.merch_views, name='merch'),
]
