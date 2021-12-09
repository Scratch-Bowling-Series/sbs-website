from django.urls import path
from . import views

app_name = 'oils'

urlpatterns = [
    path('', views.all_patterns_views, name='patterns'),
    path('<int:amount>/<int:offset>/', views.all_patterns_views, name='patterns'),
    path('view/<id>/', views.single_pattern_views, name='view')
]
