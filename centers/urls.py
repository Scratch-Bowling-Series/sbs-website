from django.urls import include, path
from . import views

app_name = 'centers'

urlpatterns = [
    path('', views.centers_views, name='centers'),
]
