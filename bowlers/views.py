from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render

from ScratchBowling.forms import BowlersSearch
from ScratchBowling.pages import create_page_obj
from ScratchBowling.views import load_bowler_of_month
from accounts.views import get_amount_online


User = get_user_model()

def bowlers_views(request, page=1):
    page = int(page)
    per_page = 40

    if request.method == 'POST':
        form = BowlersSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data
            users = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(
                location_city__icontains=search) | Q(location_state__icontains=search))
        else:
            users = User.objects.all()
    else:
        users = User.objects.all()

    bowlers = []
    bowlers_count = len(users)
    start = (per_page * page) - per_page
    end = per_page * page
    for user in users[start:end]:
        bowler = user_to_display_list(user)
        if bowler[1] != None:
            bowlers.append(bowler)

    return render(request, 'bowlers/main-bowlers.html', {'nbar': 'bowlers',
                                                         'bowlers': bowlers,
                                                         'bowlers_count': bowlers_count,
                                                         'bowler_of_month': load_bowler_of_month(),
                                                         'online_count': get_amount_online(),
                                                         'search_type': 'bowlers_search',

                                                         'page': create_page_obj(page, per_page, bowlers_count)})



def user_to_display_list(user):
    return [user.user_id,
            user.first_name,
            user.last_name,
            user.location_city,
            user.location_state,
            user.picture,
            user.statistics
            ]