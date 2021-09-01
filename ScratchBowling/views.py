from datetime import datetime
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from accounts.forms import User
from check_git import get_last_commit
from scoreboard.ranking import get_top_rankings
from support.donation import get_donation_count
from tournaments.models import Tournament
from tournaments.tournament_scraper import scrape_tournaments_task

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
                   'tournaments_count': None, ##get_tournaments_count(),
                   'top_ten_ranks': None, ##get_top_ten_ranks(),
                   'donation_count': None, ##get_donation_count(),
                   })


def about(request):
    return render(request, 'about.html', {'nbar': 'about'})


def contact(request):
    user = User.objects.filter(email='christianjstarr@icloud.com').first()
    return render(request, 'contact.html', {'nbar': 'contact', 'test': user})

def load_tournament_live():
    live_center = {'name': '300 Bowl', 'city': 'Detroit', 'state': 'MI'}
    live_status = 'Qualifying (3/10)'
    live_leader = 'Christian S.'
    live_score = '410'
    return {'is_live': True, 'center': live_center, 'status': live_status, 'leader': live_leader, 'score': live_score}


def load_tournament_recent():
    return Tournament.objects.all().first()

def load_tournament_winners():
    return Tournament.objects.all()[:10]

def load_tournament_upcoming():
    return Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())

def load_bowler_of_month():
    return User.objects.all().first()

def get_users_count():
    return User.objects.all().count()

def get_tournaments_count():
    return Tournament.objects.all().count()

def get_top_ten_ranks():
    return None
    ##return get_top_rankings(10)

def has_content_changed(request):
    data = get_last_commit()
    return HttpResponse(str(data))

def scrape_tournaments(request):
    output = scrape_tournaments_task()
    return HttpResponse(output)

def scrape_bowlers(request):
    return None
