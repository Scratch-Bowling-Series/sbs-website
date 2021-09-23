from django.urls import path
from . import views

app_name = 'oils'

urlpatterns = [
    path('', views.all_patterns_views, name='patterns'),
    path('view/<id>', views.view_pattern_views, name='view')
]
