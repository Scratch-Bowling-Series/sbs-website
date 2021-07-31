from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'prolink'

urlpatterns = [
    path('', views.prolink_main_view, name='home'),
    path('login/', views.prolink_login_view, name='login'),
    path('create/', views.prolink_create_view, name='create'),
    path('start/', views.prolink_start_view, name='start'),
    path('active/', views.prolink_active_view, name='active'),
    path('all/', views.prolink_all_view, name='all'),
    path('formats/', views.prolink_formats_view, name='formats'),
    path('bowlers/', views.prolink_bowlers_view, name='bowlers'),
    path('bowlers/request/<int:page>/<int:amount>/', views.prolink_bowlers_request, name='bowlers_request'),
    path('centers/', views.prolink_centers_view, name='centers'),
    path('rankings/', views.prolink_rankings_view, name='rankings'),
    path('account/', views.prolink_account_view, name='account'),
    path('websettings/', views.prolink_web_settings_view, name='websettings'),
    path('prosettings/', views.prolink_pro_settings_view, name='prosettings'),
    path('ping/', views.prolink_ping_view, name='ping'),



    path('centers/autofield/<args>/', views.prolink_centers_autofield, name='centers_autofield'),

]
