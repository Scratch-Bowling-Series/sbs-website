from django.conf.urls import url
from django.urls import include, path, re_path
from . import views
from .views import BowlerAutocomplete

app_name = 'tournaments'

urlpatterns = [
    url(r'^bowler_autocomplete/?', BowlerAutocomplete.as_view(), name='bowler_autocomplete'),
    path('', views.tournaments_upcoming_views, name='tournaments'),
    path('upcoming', views.tournaments_upcoming_views, name='upcoming'),
    path('results', views.tournaments_results_views, name='results'),
    path('create', views.tournaments_create_views, name='create'),
    path('view/<id>', views.tournaments_view_views, name='view'),
    path('modify/<id>', views.tournaments_modify_views, name='modify'),
    path('scraper', views.scraper_views, name='scraper'),
    path('scraper/bowlers', views.scraper_bowlers_views, name='bowlers')
]
