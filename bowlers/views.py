from django.contrib.auth import get_user_model
from django.shortcuts import render

from ScratchBowling.views import load_bowler_of_month

User = get_user_model()

def bowlers_views(request):
    users = User.objects.all()
    bowlers= []
    bowlers_count = len(users)
    for user in users[:50]:
        bowler = user_to_display_list(user)
        if bowler[1] != None:
            bowlers.append(bowler)

    return render(request, 'bowlers/main-bowlers.html', {'nbar': 'bowlers', 'bowlers': bowlers, 'bowlers_count': bowlers_count,'bowler_of_month': load_bowler_of_month()})



def user_to_display_list(user):
    return [user.user_id,
            user.first_name,
            user.last_name,
            user.location_city,
            user.location_state,
            user.picture,
            user.statistics
            ]