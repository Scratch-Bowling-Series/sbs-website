from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect
from ScratchBowling.forms import TournamentsSearch
from ScratchBowling.pages import create_page_obj
from ScratchBowling.sbs_utils import is_valid_uuid
from oils.oil_pattern import  get_oil_display_data
from tournaments.forms import CreateTournament, ModifyTournament
from tournaments.models import Tournament
from oils.oil_pattern_scraper import get_oil_colors
from tournaments.tournament_utils import get_tournament


def tournaments_results_views(request, page=1, search=''):
    page = int(page)
    per_page = 20
    selected_upcoming = False
    tournaments_count = Tournament.objects.all().count()
    tournaments_past = Tournament.objects.filter(tournament_date__lte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__gt=datetime.now().time())

    if request.method == 'POST':
        form = TournamentsSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']
            tournaments_past = tournaments_past.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))
    elif search != '':
        tournaments_past = tournaments_past.filter(Q(tournament_name__icontains=search) | Q(tournament_date__icontains=search))

    reallist = []
    for tournament in tournaments_past:

        qualifying = None ##get_qualifying_object(tournament)
        if qualifying != None and len(qualifying) > 0:
            reallist.append(tournament)
    start = (per_page * page) - per_page
    end = per_page * page
    total_count = len(reallist)
    tournaments_past = reallist[start:end]
    return render(request, 'tournaments/main-tournaments.html', {'nbar': 'tournaments',
                                                                 'tournaments_past': tournaments_past,
                                                                 'selected_upcoming':selected_upcoming,
                                                                 'tournaments_count': tournaments_count,
                                                                 'upcoming_count': Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time()).count(),
                                                                 'results_count': total_count,
                                                                 'search_type': 'tournaments_results',
                                                                 'search': search,
                                                                 'page': create_page_obj(page, per_page, total_count),
                                                                 'page_title': 'Tournament Results',
                                                                 'page_description': 'Check our list of Tournament Results and view info about a Tournament.',
                                                                 'page_keywords': 'Tournament, Results, Scores, Information, Statistics, Bowlers, Checking, Reserve, Roster, Bowl, Entry'
                                                                 })

def tournaments_upcoming_views(request):
    selected_upcoming = True
    tournaments_count = Tournament.objects.all().count()
    tournaments_upcoming = Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())
    return render(request, 'tournaments/main-tournaments.html', {'nbar': 'tournaments',
                                                                 'tournaments_upcoming': tournaments_upcoming,
                                                                 'selected_upcoming':selected_upcoming,
                                                                 'upcoming_count': tournaments_upcoming.count(),
                                                                 'tournaments_count': tournaments_count,
                                                                 'search_type': 'tournaments_upcoming',
                                                                 'page_title': 'Upcoming Tournaments',
                                                                 'page_description': 'View all of our Upcoming Tournaments. Join a Roster. Bowl Today!',
                                                                 'page_keywords': 'Bowl, Upcoming, Tournaments, Roster, Join, View, Reserver, Entry, Results, Scores'

                                                                 })

def tournaments_view_views(request, id):
    tournament = Tournament.objects.get(tournament_id=id)

    oil_pattern = get_oil_display_data(879)
    oil_colors = get_oil_colors()

    return render(request, 'tournaments/view-tournament.html', {'nbar': 'tournaments', 'tournament': tournament, 'oil_pattern': oil_pattern, 'oil_colors': oil_colors})

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





















