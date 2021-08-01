from django.db.models import Q
from django.http import request

from accounts.forms import User
from centers.models import Center
from oils.models import Oil_Pattern


def get_list_of_all_bowlers(request, page, amount_per_page, search_args=None, filter_args=None, sort_args=None):
    total = page * amount_per_page
    start = total - amount_per_page
    end = total - 1
    temp = []
    users = User.objects.all()[start:end]

    for user in users:
        temp.append(bowler_to_list(user))
    return  temp


def bowler_to_list(user):
    if (user.location_city is '' or user.location_city is None) and (user.location_state is '' or user.location_state is None):
        bowler = [str(user.first_name) + ' ' + str(user.last_name),
                  str(user.location_city) + ', ' + str(user.location_state), str(user.date_joined),
                  str(user.user_id), str(user.picture)]
        return bowler
    elif user.location_city is '' or user.location_city is None:
        bowler = [str(user.first_name) + ' ' + str(user.last_name),
                  str(user.location_city) + ', ' + str(user.location_state), str(user.date_joined),
                  str(user.user_id), str(user.picture)]
        return bowler
    elif user.location_state is '' or user.location_state is None:
        bowler = [str(user.first_name) + ' ' + str(user.last_name),
                  str(user.location_city) + ', ' + str(user.location_state), str(user.date_joined),
                  str(user.user_id), str(user.picture)]
        return bowler
    else:
        bowler = [str(user.first_name) + ' ' + str(user.last_name),
              str(user.location_city) + ', ' + str(user.location_state), str(user.date_joined),
              str(user.user_id), str(user.picture)]
        return bowler


def get_centers_from_auto_field(search_args):
    centers = Center.objects.filter(Q(center_name__icontains=search_args) | Q(location_city__icontains=search_args) | Q(location_state__icontains=search_args))
    return_data = []
    print(len(centers))
    print(len(Center.objects.all()))
    for center in centers:
        name = ''
        if center.center_name is not None:
            name = center.center_name

        date = ''
        if center.location_city is not None:
            date = center.location_city[:10]
        return_data.append([name, date])

    return return_data


def get_oils_from_auto_field(search_args):
    oil_patterns = Oil_Pattern.objects.filter(Q(pattern_name__icontains=search_args) | Q(pattern_db_id__icontains=search_args))
    return_data = []
    for oil_pattern in oil_patterns:
        name = ''
        if oil_pattern.pattern_name is not None:
            name = oil_pattern.pattern_name

        db_id = ''
        if oil_pattern.pattern_db_id is not None:
            db_id = oil_pattern.pattern_db_id
        return_data.append([name, db_id])

    return return_data