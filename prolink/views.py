import json
from time import sleep

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from accounts.views import User
from centers.center_web_scraper import scrape_centers
from oils.oil_pattern_scraper import update_library
from prolink.prolink_requests import get_list_of_all_bowlers, get_centers_from_auto_field, get_oils_from_auto_field, \
    get_list_of_all_patterns, get_list_of_all_tournaments, get_list_of_all_centers


def prolink_main_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-home.html', {'page_name':'DASHBOARD', 'nbar':'home'})


def prolink_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'prolink-login.html', {'success': True})
        else:
            return render(request, 'prolink-login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'prolink-login.html', {'form': form})


def prolink_create_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-create.html', {'page_name':'CREATE TOURNAMENT', 'nbar':'create'})


def prolink_start_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-start.html', {'page_name':'START TOURNAMENT', 'nbar':'start'})


def prolink_active_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-active.html', {'page_name':'ACTIVE TOURNAMENTS', 'nbar':'active'})


def prolink_all_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-all.html', {'page_name':'ALL TOURNAMENTS', 'nbar':'all'})


def prolink_formats_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-formats.html', {'page_name':'TOURNAMENT FORMATS', 'nbar':'formats'})


def prolink_oils_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-oils.html', {'page_name':'OIL PATTERNS', 'nbar':'oils'})


def prolink_bowlers_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    bowlers = []
    datas = User.objects.all()[:10]
    for data in datas:
        bowler = None
        if (data.location_city is '' or data.location_city is None) and (data.location_state is '' or data.location_state is None):
            bowler = [str(data.first_name) + ' ' + str(data.last_name), 'Location Unknown', data.date_joined]
        elif data.location_city is '' or data.location_city is None:
            bowler = [str(data.first_name) + ' ' + str(data.last_name), str(data.location_state), data.date_joined]
        elif data.location_state is '' or data.location_state is None:
            bowler = [str(data.first_name) + ' ' + str(data.last_name), str(data.location_city), data.date_joined]
        else:
            bowler = [str(data.first_name) + ' ' + str(data.last_name), str(data.location_city) + ', ' + str(data.location_state), data.date_joined]
        bowlers.append(bowler)
    return render(request, 'prolink-bowlers.html', {'page_name':'BOWLERS DATABASE', 'nbar':'bowlers', 'bowlers': bowlers})


def prolink_centers_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-centers.html', {'page_name':'BOWLING CENTERS', 'nbar':'centers'})


def prolink_centers_autofield(request, args):
    return HttpResponse(json.dumps(get_centers_from_auto_field(args)))


def prolink_rankings_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-rankings.html', {'page_name':'RANKINGS', 'nbar':'rankings'})


def prolink_account_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-account.html', {'page_name':'MY ACCOUNT', 'nbar':'account'})


def prolink_web_settings_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-web-settings.html', {'page_name':'WEBSITE SETTINGS', 'nbar':'websettings'})


def prolink_pro_settings_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return render(request, 'prolink-pro-settings.html', {'page_name':'SOFTWARE SETTINGS', 'nbar':'prosettings'})


def prolink_ping_view(request):
    if is_pro_auth(request): return render(request, 'prolink-error.html')
    return HttpResponse('Ping Success')


def prolink_oils_autofield(request, args):
    return HttpResponse(json.dumps(get_oils_from_auto_field(args)))


def prolink_load_view(request):
    return render(request, 'prolink-load.html')

def prolink_load_bkg_view(request):
    return render(request, 'prolink-load-bkg.html')


def prolink_load_bowlers_request(request):
    return JsonResponse(get_list_of_all_bowlers())


def prolink_load_patterns_request(request):
    return JsonResponse(get_list_of_all_patterns())


def prolink_load_tournaments_request(request):
    return JsonResponse(get_list_of_all_tournaments())


def prolink_load_centers_request(request):
    return JsonResponse(get_list_of_all_centers())


def is_pro_auth(request):
    return False
    return not request.user.is_authenticated
