from django.urls import path
from . import views

app_name = 'bowlers'

urlpatterns = [
    path('', views.bowlers_views, name='bowlers'),
    path('page/<page>', views.bowlers_views, name='bowlers'),
    path('search/<search>/page/<page>', views.bowlers_views, name='bowlers'),
]
