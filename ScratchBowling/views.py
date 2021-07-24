from datetime import datetime
import json
from django.template.defaulttags import register
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import random
from accounts.forms import User
from scoreboard.ranking import get_top_rankings
from tournaments.models import Tournament

User = get_user_model()

def index(request):
    return render(request,
                  'homepage.html',
                  {'nbar': 'home',
                   'tournament_live': load_tournament_live(),
                   'tournament_winners': load_tournament_winners(),
                   'tournaments_upcoming': load_tournament_upcoming(),
                   'tournament_recent': load_tournament_recent(),
                   'bowler_of_month': load_bowler_of_month(),
                   'users_count': get_users_count(),
                   'tournaments_count': get_tournaments_count(),
                   'top_ten_ranks': get_top_ten_ranks(),
                   })


def about(request):
    return render(request, 'about.html', {'nbar': 'about'})


def load_tournament_live():
    live_center = {'name': 'Center Name', 'city': 'City', 'state': 'State'}
    live_status = 'Qualifying (3/10)'
    live_leader = 'Leader Name'
    live_score = '(110)'
    return {'is_live': False, 'center': live_center, 'status': live_status, 'leader': live_leader, 'score': live_score}


def load_tournament_recent():
    return Tournament.objects.all()[4]


def load_tournament_winners():
    tournaments = Tournament.objects.all()
    data = []
    for x in range(0,10):
        data.append(tournaments[x])
    return data


def load_tournament_upcoming():
    return Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())



def load_bowler_of_month():
   return User.objects.all()[222]


def get_users_count():
    users = User.objects.all()
    return users.count()


def get_tournaments_count():
    return Tournament.objects.all().count()


def get_top_ten_ranks():
    return get_top_rankings(10)

