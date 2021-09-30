from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('watch/<id>', views.watch_views, name='watch'),
    path('poster/<id>', views.poster_views, name='poster'),
]

