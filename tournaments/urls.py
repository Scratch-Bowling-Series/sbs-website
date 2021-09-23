from django.urls import path
from . import views, data

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournaments_upcoming_views, name='tournaments'),

    ## UPCOMING PAGE
    path('upcoming', views.tournaments_upcoming_views, name='upcoming'),
    path('upcoming/page/<page>', views.tournaments_upcoming_views, name='upcoming'),
    path('upcoming/search/<search>/page/<page>', views.tournaments_upcoming_views, name='upcoming'),

    ## RESULTS PAGE
    path('results', views.tournaments_results_views, name='results'),
    path('results/page/<page>', views.tournaments_results_views, name='results'),
    path('results/search/<search>/page/<page>', views.tournaments_results_views, name='results'),

    path('create', views.tournaments_create_views, name='create'),
    path('view/<id>', views.tournaments_view_views, name='view'),
    path('modify/<id>', views.tournaments_modify_views, name='modify'),


    path('data/sponsor-pic/<id>', data.get_sponsor_pic, name='data-sponsor-pic'),
    path('data/tournament-pic/<id>', data.get_tournament_pic, name='data-winners-pic')
]

