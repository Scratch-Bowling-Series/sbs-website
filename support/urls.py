from django.conf.urls import url
from django.urls import include, path, re_path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.support_views, name='support')
]
