from django.urls import include, path
from . import views

app_name = 'bowlers'

urlpatterns = [
    path('', views.bowlers_views, name='bowlers'),
    path('page/<page>', views.bowlers_views, name='bowlers'),
]
