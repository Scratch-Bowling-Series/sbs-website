from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from ScratchBowling.forms import BowlersSearch
from accounts.forms import User
from centers.models import Center
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
                   'tournaments_count': get_tournaments_count(),
                   'top_ten_ranks': get_top_ten_ranks(),
                   'donation_count': get_donation_count(),
                   })

def search(request):
    if request.method == 'POST':
        form = BowlersSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']

            bowlers = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(location_city__icontains=search) | Q(location_state__icontains=search))[:4]
            temp_bowlers = []
            for bowler in bowlers:
                temp_bowlers.append(user_to_display_list(bowler))
            bowlers = temp_bowlers


            tournaments_upcoming = Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())
            tournaments_results = Tournament.objects.filter(tournament_date__lte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__gt=datetime.now().time())

            tournaments_upcoming = tournaments_upcoming.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))[:4]
            ##tournaments_results = tournaments_results.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))[:4]





            centers = Center.objects.filter(Q(center_name__icontains=search) | Q(location_city__icontains=search) | Q(location_state__icontains=search))[:4]
            return render(request, 'search-main.html', {'tournament_upcoming': tournaments_upcoming,
                                                        'tournament_upcoming_count': len(tournaments_upcoming),
                                                        'tournament_results': tournaments_results,
                                                        'tournament_results_count': len(tournaments_results),
                                                        'bowlers': bowlers,
                                                        'bowlers_count': len(bowlers),
                                                        'centers': centers,
                                                        'centers_count': len(centers),
                                                        'search': search})
    else:
        return redirect('/')


def user_to_display_list(user):
    return [user.user_id,
            user.first_name,
            user.last_name,
            user.location_city,
            user.location_state,
            user.picture,
            user.statistics
            ]

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
