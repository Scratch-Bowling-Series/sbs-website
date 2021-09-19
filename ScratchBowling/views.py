from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from ScratchBowling.forms import BowlersSearch
from ScratchBowling.popup import check_for_popup
from ScratchBowling.shortener import create_link
from accounts.account_helper import get_name_from_uuid
from accounts.forms import User
from accounts.models import Shorten
from centers.models import Center
from check_git import get_last_commit
from scoreboard.ranking import get_top_rankings
from support.donation import get_donation_count
from tournaments.models import Tournament
from tournaments.tournament_scraper import scrape_tournaments_task
from tournaments.tournament_utils import get_winner

User = get_user_model()


def index(request, notify=''):
    data = {'nbar': 'home',
            'notify':notify,
            'popup': check_for_popup(request.user),
            'tournament_live': load_tournament_live(),
            'tournament_winners': load_tournament_winners(),
            'tournaments_upcoming': load_tournament_upcoming(),
            'tournament_recent': load_tournament_recent(),
            'bowler_of_month': load_bowler_of_month(),
            'users_count': get_users_count(),
            'tournaments_count': get_tournaments_count(),
            'top_ten_ranks': get_top_ten_ranks(),
            'donation_count': get_donation_count(),
            'page_title': '',
            'page_description': 'Bowling Tournaments Done Better. Welcome to the Scratch Bowling Series. Come bowl today!',
            'page_keywords': 'scratchbowling, bowling, tournaments, events, competitive, sports, gaming, live, rankings, scores, points, elo, statistics, bowlers, professional'
    }
    return render(request, 'homepage.html', data)

def search(request):
    if request.method == 'POST':
        form = BowlersSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']
            bowlers = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(location_city__icontains=search) | Q(location_state__icontains=search))
            more_results_bowlers = len(bowlers) - 4
            bowlers = bowlers[:4]
            temp_bowlers = []
            for bowler in bowlers:
                temp_bowlers.append(user_to_display_list(bowler))
            bowlers = temp_bowlers

            tournaments_upcoming = Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())
            tournaments_results = Tournament.objects.filter(tournament_date__lte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__gt=datetime.now().time())

            tournaments_upcoming = tournaments_upcoming.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
            tournaments_results = tournaments_results.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))

            more_results_upcoming = len(tournaments_upcoming) - 4
            more_results_results = len(tournaments_results) - 4

            tournaments_upcoming = tournaments_upcoming[:4]
            tournaments_results = tournaments_results[:4]

            centers = Center.objects.filter(Q(center_name__icontains=search) | Q(location_city__icontains=search) | Q(location_state__icontains=search))
            more_results_centers = len(centers) - 4
            centers = centers[:4]

            return render(request, 'search-main.html', {'tournament_upcoming': tournaments_upcoming,
                                                        'tournament_upcoming_count': len(tournaments_upcoming),
                                                        'more_results_upcoming': more_results_upcoming,
                                                        'tournament_results': tournaments_results,
                                                        'tournament_results_count': len(tournaments_results),
                                                        'more_results_results': more_results_results,
                                                        'bowlers': bowlers,
                                                        'bowlers_count': len(bowlers),
                                                        'more_results_bowlers': more_results_bowlers,
                                                        'centers': centers,
                                                        'centers_count': len(centers),
                                                        'more_results_centers': more_results_centers,
                                                        'search': search})
    else:
        return HttpResponseRedirect('/')

def about(request):
    return render(request, 'about.html', {'nbar': 'about'})

def contact(request):
    return render(request, 'contact.html', {'nbar': 'contact',
                                            'page_title': 'Contact',
                                            'page_description': 'If you have any questions or need help with something. Please contact us here and we will get back with you as soon as possible.',
                                            'page_keywords': 'Contact, Message, Help, Email, Faqs, Support, Call, Maintenance'
                                            })

def shortener(request, code):
    if code == '' or len(code) != 5:
        return Http404('This link is broken...')
    shorten = Shorten.objects.filter(code=code).first()
    if shorten != None:
        return HttpResponseRedirect(shorten.url)
    return Http404('This link is broken...')

def shortener_create(request, url):
    if url == '' or len(url) < 5:
        return HttpResponse('')
    else:
        return HttpResponse(create_link(url))



def user_to_display_list(user):
    return [user.user_id,
            user.first_name,
            user.last_name,
            user.location_city,
            user.location_state,
            user.picture,
            user.statistics
            ]

def load_tournament_live():
    live_center = {'name': '300 Bowl', 'city': 'Detroit', 'state': 'MI'}
    live_status = 'Qualifying (3/10)'
    live_leader = 'Christian S.'
    live_score = '410'
    return {'is_live': True, 'center': live_center, 'status': live_status, 'leader': live_leader, 'score': live_score}

def load_tournament_recent():
    return Tournament.objects.all().first()

def load_tournament_winners():
    ## FORMAT: ARRAY OF LISTS [id, name, date, winner_name, winner_uuid]
    winner_data = []
    last_ten_tournaments = Tournament.objects.all()[:10]
    for tournament in last_ten_tournaments:
        winner_id = get_winner(tournament.placement_data)
        winner_data.append([str(tournament.tournament_id), tournament.tournament_name, tournament.tournament_date, get_name_from_uuid(winner_id), str(winner_id)])
    return winner_data

def load_tournament_upcoming():
    return Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())

def load_bowler_of_month():
    return User.objects.all().first()

def get_users_count():
    return User.objects.all().count()

def get_tournaments_count():
    return Tournament.objects.all().count()

def get_top_ten_ranks():
    return get_top_rankings(10)

def has_content_changed(request):
    data = get_last_commit()
    return HttpResponse(str(data))

def scrape_tournaments(request):
    output = scrape_tournaments_task()
    return HttpResponse(output)

def scrape_bowlers(request):
    return None
