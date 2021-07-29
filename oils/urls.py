from django.conf.urls import url
from django.urls import include, path, re_path
from . import views

app_name = 'oils'

urlpatterns = [
    path('', views.all_patterns_views, name='patterns'),
    path('view/<id>', views.view_pattern_views, name='view')
]
