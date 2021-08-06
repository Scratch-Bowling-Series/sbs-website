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
    path('oils/', views.prolink_oils_view, name='oils'),
    path('bowlers/', views.prolink_bowlers_view, name='bowlers'),
    path('centers/', views.prolink_centers_view, name='centers'),
    path('rankings/', views.prolink_rankings_view, name='rankings'),
    path('account/', views.prolink_account_view, name='account'),
    path('websettings/', views.prolink_web_settings_view, name='websettings'),
    path('prosettings/', views.prolink_pro_settings_view, name='prosettings'),
    path('ping/', views.prolink_ping_view, name='ping'),

    path('centers/autofield/<args>/', views.prolink_centers_autofield, name='centers_autofield'),
    path('oils/autofield/<args>/', views.prolink_oils_autofield, name='oils_autofield'),

    path('load/', views.prolink_load_view, name='load'),
    path('load/background', views.prolink_load_bkg_view, name='load'),
    path('load/bowlers/', views.prolink_load_bowlers_request, name='load_bowlers'),
    path('load/patterns/', views.prolink_load_patterns_request, name='load_patterns'),
    path('load/tournaments/', views.prolink_load_tournaments_request, name='load_tournaments'),
    path('load/centers/', views.prolink_load_centers_request, name='load_centers'),

    path('updater/', views.prolink_updater_view, name='updater'),
    path('update/', views.prolink_update, name='update'),

    path('download/', views.prolink_download, name='download'),
]
