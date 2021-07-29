from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def prolink_main_view(request):
    if request.user.is_authenticated is False:
        return redirect('/')
    return render(request, 'prolink-home.html')


def prolink_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'prolink-login.html', {'success': True})
    else:
        form = AuthenticationForm()
    return render(request, 'prolink-login.html', {'form': form})


def prolink_create_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-create.html', {'page_name':'CREATE TOURNAMENT'})


def prolink_start_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-start.html', {'page_name':'START TOURNAMENT'})


def prolink_active_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-active.html', {'page_name':'ACTIVE TOURNAMENTS'})


def prolink_all_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-all.html', {'page_name':'ALL TOURNAMENTS'})


def prolink_formats_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-formats.html', {'page_name':'TOURNAMENT FORMATS'})


def prolink_bowlers_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-bowlers.html', {'page_name':'BOWLERS DATABASE'})


def prolink_centers_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-centers.html', {'page_name':'BOWLING CENTERS'})


def prolink_rankings_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-rankings.html', {'page_name':'RANKINGS'})


def prolink_account_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-account.html', {'page_name':'MY ACCOUNT'})


def prolink_web_settings_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-web-settings.html', {'page_name':'WEBSITE SETTINGS'})


def prolink_pro_settings_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return render(request, 'prolink-pro-settings.html', {'page_name':'SOFTWARE SETTINGS'})


def prolink_ping_view(request):
    if request.user.is_authenticated is False:
        return render(request, 'prolink-error.html')
    return HttpResponse('Ping Success')
