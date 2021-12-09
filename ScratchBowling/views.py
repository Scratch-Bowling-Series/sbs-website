import os
from datetime import datetime
from random import randrange
from uuid import UUID

import requests
from django import template
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ScratchBowling import settings
from ScratchBowling.forms import BowlersSearch
from ScratchBowling.models import WebData
from ScratchBowling.popup import check_for_popup
from ScratchBowling.sbs_utils import is_valid_uuid
from accounts.account_helper import get_name_from_uuid, load_bowler_of_month, get_amount_users, get_top_ranks
from accounts.forms import User
from bowlers.views import display_get_bowlers
from broadcasts.models import Clip
from cacher.models import Homepage_Cache
from centers.center_utils import get_center_name_uuid, get_center_location_uuid
from centers.models import Center
from check_git import get_last_commit
from scoreboard.rank_data import serialize_rank_data
from support.donation import get_donation_count
from tournaments.models import Tournament
from tournaments.tournament_scraper import scrape_tournaments_task
from tournaments.tournament_utils import get_winner, get_top_placements, get_all_live_tournaments
import quickle

User = get_user_model()




# <editor-fold desc="PAGES">
def index(request, notify=''):
    data = {'nbar': 'home',
            'notify': notify,
            'popup': check_for_popup(request.user),
            'tournament_live': load_tournament_live(),
            'tournaments_upcoming': load_tournament_upcoming(),
            'tournament_winners': load_tournament_winners(),
            'top_ten_ranks': get_top_ranks(10),
            'tournament_recent': load_tournament_recent(),
            'bowler_of_month': load_bowler_of_month(),
            'users_count': get_amount_users(),
            'tournaments_count': get_tournaments_count(),
            'donation_count': get_donation_count(),
            'broadcast_clips': load_recent_broadcast_clips(),
            }

    meta = {'page_title': '',
            'page_description': 'Bowling Tournaments Done Better. Welcome to the Scratch Bowling Series. Come bowl today!',
            'page_keywords': 'scratchbowling, bowling, tournaments, events, competitive, sports, gaming, live, rankings, scores, points, elo, statistics, bowlers, professional'
    }
    return render(request, 'homepage.html', data | meta)

def search(request):
    if request.method == 'POST':
        form = BowlersSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search_args']
            bowlers = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(location_city__icontains=search) | Q(location_state__icontains=search))
            more_results_bowlers = len(bowlers) - 4
            bowlers = display_get_bowlers(bowlers[:4])

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

def help_center(request):
    return render(request, 'help-center.html', {'nbar': 'help-center'})

def live_chat(request):
    return render(request, 'live-chat.html', {'nbar': 'live-chat'})

def privacy(request):
    return render(request, 'privacy.html', {'nbar': 'privacy'})
def terms(request):
    return render(request, 'terms.html', {'nbar': 'terms'})

def contact(request):
    return render(request, 'contact.html', {'nbar': 'contact',
                                            'page_title': 'Contact',
                                            'page_description': 'If you have any questions or need help with something. Please contact us here and we will get back with you as soon as possible.',
                                            'page_keywords': 'Contact, Message, Help, Email, Faqs, Support, Call, Maintenance'
                                            })
# </editor-fold>

# <editor-fold desc="INDEX DATA">
def load_tournament_live():
    live_tournaments = get_all_live_tournaments()
    if live_tournaments != None:
        tournament = live_tournaments.filter(stream_available=True).first()
        if tournament != None:
            return {'stream': True,
                    'center': {'name': get_center_name_uuid(tournament.center),
                               'location': get_center_location_uuid(tournament.center)},
                    'status': tournament.live_status_header,
                    'leader': tournament.live_status_leader,
                    'score': tournament.live_status_leader_score}
        else:
            tournament = live_tournaments.first()
            if tournament != None:
                return {'stream': False,
                    'center': {'name': get_center_name_uuid(tournament.center),
                               'location': get_center_location_uuid(tournament.center)},
                    'status': tournament.live_status_header,
                    'leader': tournament.live_status_leader,
                    'score': tournament.live_status_leader_score}

    return None

def load_tournament_recent():
    webData = WebData.get_current()
    webData.preview_tournament = is_valid_uuid("56e44a8d-9fda-4ff3-b0f7-ad0236c6c667")
    webData.save()

    ## FORMAT
    ## [0=id, 1=name, 2=date, 3=center_name, 4=center_location, 5=description, 6=topfour]
    tournament = Tournament.objects.filter(tournament_id=WebData.get_current().preview_tournament).first()
    if tournament:
        return [
            str(tournament.tournament_id),
            tournament.tournament_name,
            tournament.tournament_date,
            get_center_name_uuid(tournament.center),
            get_center_location_uuid(tournament.center),
            tournament.tournament_description[:250],
            get_top_placements(tournament.placement_data, 4),
            tournament.get_picture()
        ]
    return None

def load_tournament_winners():
    ## FORMAT: ARRAY OF LISTS
    ## [id, name, date, winner_name, winner_uuid]
    winner_data = []
    last_ten_tournaments = Tournament.objects.all()[:10]
    for tournament in last_ten_tournaments:
        winner_id = get_winner(tournament.placement_data)
        winner_data.append([str(tournament.tournament_id), tournament.tournament_name, tournament.tournament_date, get_name_from_uuid(winner_id, True, True), str(winner_id)])
    return winner_data

def load_tournament_upcoming():
    ## FORMAT: ARRAY OF LISTS
    ## [id, name, date, entry_fee]
    tournaments = Tournament.get_upcoming_tournaments()
    output = []
    for tournament in tournaments:
        output.append([str(tournament.tournament_id), tournament.tournament_name, tournament.datetime, tournament.entry_fee])
    return output

def load_recent_broadcast_clips():
    ## FORMAT: ARRAY OF LISTS
    ## [0=clip_id, 1=clip_name, 2=clip_date, 3=clip_duration, 4=clip_thumbnail]
    clips = Clip.get_most_recent(4)
    output = []
    if clips:
        for clip in clips:
            output.append([clip.clip_id, clip.title, clip.datetime, clip.duration, clip.thumbnail_image])
    return output

def get_tournaments_count():
    return Tournament.objects.all().count()


# </editor-fold>






def scrape_tournaments(request):
    output = scrape_tournaments_task()
    return HttpResponse(output)

def scrape_bowlers(request):
    return None

