from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from ScratchBowling.forms import TournamentsSearch
from ScratchBowling.pages import create_page_obj
from ScratchBowling.sbs_utils import is_valid_uuid
from centers.models import Center
from oils.models import Oil_Pattern
from tournaments.forms import CreateTournament, ModifyTournament
from tournaments.models import Tournament
from oils.oil_pattern_scraper import get_oil_colors
from tournaments.roster import deserialize_roster_data, roster_data_display
from tournaments.tournament_utils import get_tournament, get_all_completed_tournaments, get_count_upcoming_tournaments, \
    get_all_upcoming_tournaments, get_count_all_tournaments, convert_to_display_main_upcoming_list, \
    convert_to_display_main_results_list, get_all_live_tournaments
from vods.vod_utils import get_vod_url

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

User = get_user_model()

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
    live_count = 0
    data = {'tournaments': tournaments,
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
    live_count = 0
    data = {'tournaments': tournaments,
            'live_count': live_count,
            'selected_upcoming': True,
            'upcoming_count': upcoming_count,
            'tournaments_count': tournaments_count,
            'search': search,
            'page': create_page_obj(page, per_page, results_count),
    }
    data.update(page_data_upcoming)
    return render(request, 'tournaments/main-tournaments.html', data)

def single_tournament_views(request, id):
    tournament = Tournament.get_tournament_by_uuid(id)
    if tournament:
        render_data = {'nbar': 'tournaments',
                       'tournament': tournament}

        return render(request, 'tournaments/view-tournament.html', render_data)
    else:
        raise Http404('The Tournament you are looking for does not exist.')


                       #  'live': tournament.live,
                       # 'stream_available': tournament.stream_available,
                       # 'finished': tournament.finished,
                       # 'on_roster': on_roster,
                       # 'tournament': display_tournament_view(tournament),
                       # 'center': display_center_view(tournament.center),
                       # 'oil_pattern': Oil_Pattern.get_oil_pattern_converted_uuid(tournament.oil_pattern),
                       # 'oil_colors': get_oil_colors(),
                       # 'roster': roster_data,
                       # 'payout': payout_calculator(30, 10, 5, 50),
                       # 'vod_url' : get_vod_url(tournament.vod_id),
                       # 'tournament_picture': tournament.get_picture(),
                       # 'description': tournament.description





def display_tournament_view(tournament):
    ## FORMAT
    ## [ 0=id, 1=name, date=2, time=3, desc=4,
    #   5=center_id, 6=name, 7=center_location,
    #   8=vod_id, 9=tags, 10=entry_fee, 11=team_entry]
    name = 'Center Unknown'
    center_location = ''
    center_data = Center.get_name_and_location_by_uuid(tournament.center)
    if center_data:
        name = center_data[0]
        center_location = str(center_data[1]) + ', ' + str(center_data[2])

    date = tournament.datetime.date()
    if date.year == datetime.now().year:
        date = date.strftime('%m/%d')
    else:
        date = date.strftime('%m/%d/%y')

    entry_fee = tournament.entry_fee
    if not entry_fee:
        entry_fee = 0
    is_team_entry = False
    if 'double' in tournament.name:
        is_team_entry = True
    if 'Double' in tournament.name:
        is_team_entry = True
    return [tournament.id,
            tournament.name,
            date,
            tournament.tournament_time,
            tournament.description,
            tournament.center,
            name,
            center_location,
            None,
            tournament.get_tags(),
            entry_fee,
            is_team_entry
            ]

def display_center_view(center_id):
    center = Center.get_center_by_uuid(center_id)
    if center:
        return [center.center_id, center.name, center.location_city, center.location_state, center.get_picture()]
    return None

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

                tournament.name = form.cleaned_data.get('tournament_name')
                tournament.description = form.cleaned_data.get('tournament_description')
                tournament.entry_fee = form.cleaned_data.get('entry_fee')
                tournament.total_games = form.cleaned_data.get('total_games')
                tournament.tournament_date = form.cleaned_data.get('tournament_date')
                tournament.tournament_time = form.cleaned_data.get('tournament_time')
                tournament.sponsor_image = '/media/sponsors/sponsor-image-03.png'
                tournament.save(force_update=True)
                if tournament.id != id:
                    return redirect('/')
                return redirect('/tournaments/')
        else:
            testform = None
            form = ModifyTournament(initial={'tournament_name': tournament.name,'tournament_description': tournament.description,'entry_fee': tournament.entry_fee,'total_games': tournament.total_games, 'tournament_date': tournament.tournament_date.strftime('%d-%m-%Y'), 'tournament_time': tournament.tournament_time})
        return render(request, 'tournaments/modify-tournament.html', {'nbar': 'tournaments', 'form': form, 'tournament': tournament, 'testform':testform})
    else:
        return redirect('/')

def tournaments_create_views(request):
    if request.method == 'POST':
        form = CreateTournament(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.create()
            tournament.name = form.cleaned_data.get('tournament_name')
            tournament.description = form.cleaned_data.get('tournament_description')
            tournament.tournament_date = form.cleaned_data.get('tournament_date')
            tournament.tournament_time = form.cleaned_data.get('tournament_time')
            tournament.save()
            return redirect('/tournaments/view/' + str(tournament.id))
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
























