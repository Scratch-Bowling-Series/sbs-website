from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from ScratchBowling.forms import TournamentsSearch
from ScratchBowling.pages import create_page_obj
from ScratchBowling.sbs_utils import is_valid_uuid
from centers.center_utils import get_center_name_uuid, get_center_location_uuid
from oils.oil_pattern import get_oil_display_data_uuid
from tournaments.forms import CreateTournament, ModifyTournament
from tournaments.models import Tournament
from oils.oil_pattern_scraper import get_oil_colors
from tournaments.roster import deserialize_roster_data, roster_data_display
from tournaments.tournament_utils import get_tournament, get_all_completed_tournaments, get_count_upcoming_tournaments, \
    get_all_upcoming_tournaments, get_count_all_tournaments, convert_to_display_main_upcoming_list, \
    convert_to_display_main_results_list, get_all_live_tournaments

page_data_results = {'nbar': 'tournaments',
                     'search_type': 'tournaments_results',
                     'page_title': 'Tournament Results',
                     'page_description': 'Check our list of Tournament Results and view info about a Tournament.',
                     'page_keywords': 'Tournament, Results, Scores, Information, Statistics, Bowlers, Checking, Reserve, Roster, Bowl, Entry'
}
page_data_upcoming = {'nbar': 'tournaments',
                      'search_type': 'tournaments_upcoming',
                      'page_title': 'Upcoming Tournaments',
                      'page_description': 'View all of our Upcoming Tournaments. Join a Roster. Bowl Today!',
                      'page_keywords': 'Bowl, Upcoming, Tournaments, Roster, Join, View, Reserver, Entry, Results, Scores'
}


def tournaments_results_views(request, page=1, search=''):
    page = int(page)
    per_page = 20
    tournaments = get_all_completed_tournaments()
    tournaments_count = tournaments.count()
    results_count = tournaments_count
    if request.method == 'POST':
        form = TournamentsSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']
            tournaments = tournaments.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
            results_count = tournaments.count()
    elif search != '':
        tournaments = tournaments.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
        results_count = tournaments.count()
    start = (per_page * page) - per_page
    end = per_page * page
    tournaments = tournaments[start:end]
    tournaments = convert_to_display_main_results_list(tournaments)
    tournaments_live = convert_to_display_main_results_list(get_all_live_tournaments())
    live_count = 0
    if tournaments_live != None:
        live_count = len(tournaments_live)
    data = {'tournaments_past': tournaments,
            'tournaments_live': tournaments_live,
            'live_count': live_count,
            'selected_upcoming': False,
            'tournaments_count': tournaments_count,
            'upcoming_count': get_count_upcoming_tournaments(),
            'results_count': results_count,
            'search': search,
            'page': create_page_obj(page, per_page, results_count),
            }
    data.update(page_data_results)
    return render(request, 'tournaments/main-tournaments.html', data)

def tournaments_upcoming_views(request, page=1, search=''):

    page = int(page)
    per_page = 20
    tournaments = get_all_upcoming_tournaments()
    tournaments_count = get_count_all_tournaments()
    upcoming_count = tournaments.count()
    results_count = upcoming_count
    if request.method == 'POST':
        form = TournamentsSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']
            tournaments = tournaments.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
            results_count = tournaments.count()
    elif search != '':
        tournaments = tournaments.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
        results_count = tournaments.count()
    start = (per_page * page) - per_page
    end = per_page * page
    tournaments = tournaments[start:end]
    tournaments = convert_to_display_main_upcoming_list(tournaments)
    tournaments_live = convert_to_display_main_results_list(get_all_live_tournaments())
    live_count = 0
    if tournaments_live != None:
        live_count = len(tournaments_live)
    data = {'tournaments_upcoming': tournaments,
            'tournaments_live': tournaments_live,
            'live_count': live_count,
            'selected_upcoming': True,
            'upcoming_count': upcoming_count,
            'tournaments_count': tournaments_count,
            'search': search,
            'page': create_page_obj(page, per_page, results_count),
    }
    data.update(page_data_upcoming)
    return render(request, 'tournaments/main-tournaments.html', data)

def tournaments_view_views(request, id):
    tournament = get_tournament(id)
    if tournament != None:
        render_data = {'nbar': 'tournaments',
                       'live': True,
                       'stream_available': True,
                       'tournament': display_tournament_view(tournament),
                       'oil_pattern': get_oil_display_data_uuid(tournament.oil_pattern),
                       'oil_colors': get_oil_colors(),
                       'roster': roster_data_display(deserialize_roster_data(tournament.roster)),
                       'payout': payout_calculator(30, 10, 5, 50)
                       }
        render_data.update(make_tournament_meta(tournament))
        return render(request, 'tournaments/view-tournament.html', render_data)
    else:
        return Http404('Tournament does not exist.')

def display_tournament_view(tournament):
    ## FORMAT
    ## [ 0=id, 1=name, date=2, time=3, desc=4, 5=center_id, 6=center_name, 7=center_location ]
    return [tournament.tournament_id,
            tournament.tournament_name,
            tournament.tournament_date,
            tournament.tournament_time,
            tournament.tournament_description,
            tournament.center,
            get_center_name_uuid(tournament.center),
            get_center_location_uuid(tournament.center)
            ]

def tournaments_modify_views(request, id):
    id = is_valid_uuid(id)
    if request.user.admin and id != None:
        tournament = get_tournament(id)
        if tournament is None:
            redirect('/')
        if request.method == 'POST':
            form = ModifyTournament(request.POST)
            if form.is_valid():
                testform = None

                tournament.tournament_name = form.cleaned_data.get('tournament_name')
                tournament.tournament_description = form.cleaned_data.get('tournament_description')
                tournament.entry_fee = form.cleaned_data.get('entry_fee')
                tournament.total_games = form.cleaned_data.get('total_games')
                tournament.tournament_date = form.cleaned_data.get('tournament_date')
                tournament.tournament_time = form.cleaned_data.get('tournament_time')
                tournament.sponsor_image = '/media/sponsors/sponsor-image-03.png'
                tournament.save(force_update=True)
                if tournament.tournament_id != id:
                    return redirect('/')
                return redirect('/tournaments/')
        else:
            testform = None
            form = ModifyTournament(initial={'tournament_name': tournament.tournament_name,'tournament_description': tournament.tournament_description,'entry_fee': tournament.entry_fee,'total_games': tournament.total_games, 'tournament_date': tournament.tournament_date.strftime('%d-%m-%Y'), 'tournament_time': tournament.tournament_time})
        return render(request, 'tournaments/modify-tournament.html', {'nbar': 'tournaments', 'form': form, 'tournament': tournament, 'testform':testform})
    else:
        return redirect('/')

def tournaments_create_views(request):
    if request.method == 'POST':
        form = CreateTournament(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.create()
            tournament.tournament_name = form.cleaned_data.get('tournament_name')
            tournament.tournament_description = form.cleaned_data.get('tournament_description')
            tournament.tournament_date = form.cleaned_data.get('tournament_date')
            tournament.tournament_time = form.cleaned_data.get('tournament_time')
            tournament.save()
            return redirect('/tournaments/view/' + str(tournament.tournament_id))
    else:
        form = CreateTournament()

    return render(request, 'tournaments/create-tournament.html', {'form': form, 'nbar': 'tournaments'})

def make_tournament_meta(tournament):
    return {'test': None}

def payout_calculator(prize, lineage, expense, current):
    minv = current / 2
    maxv = current + (current / 2)
    payouts = []
    return [prize, lineage, expense, payouts, minv, maxv, current]




















