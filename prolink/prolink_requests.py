import quickle
from django.db.models import Q
from accounts.forms import User
from centers.models import Center
from oils.models import Oil_Pattern
from tournaments.models import Tournament


def get_list_of_all_bowlers():
    users = User.objects.all()
    temp = {}
    for user in users:
        data = []
        data.append(str(user.first_name))
        data.append(str(user.last_name))
        data.append(str(user.last_login))
        data.append(str(user.city))
        data.append(str(user.state))
        data.append(str(user.picture))
        data.append(str(user.email))
        data.append(str(user.bio))
        temp[str(user.id)] = data
    return  temp


def get_list_of_all_patterns():
    oil_patterns = Oil_Pattern.objects.all()
    temp = {}
    for oil_pattern in oil_patterns:
        pattern_cache = oil_pattern.pattern_cache
        if pattern_cache is not None:
            pattern_cache = quickle.loads(pattern_cache)
            data = []
            data.append(oil_pattern.pattern_name)
            data.append(oil_pattern.pattern_db_id)
            data.append(pattern_cache)
            data.append(oil_pattern.pattern_forward)
            data.append(oil_pattern.pattern_backward)
            data.append(oil_pattern.pattern_length)
            data.append(oil_pattern.pattern_volume)
            data.append(oil_pattern.pattern_ratio)
            temp[str(oil_pattern.pattern_id)] = data
    return temp


def get_list_of_all_tournaments():
    tournaments = Tournament.objects.all()
    temp = {}
    for tournament in tournaments:
        data = []
        data.append(str(tournament.name))
        data.append(str(tournament.description))
        data.append(str(tournament.datetime))
        temp[str(tournament.id)] = data

    return temp


def get_list_of_all_centers():
    centers = Center.objects.all()
    temp = {}
    for center in centers:
        data = []
        data.append(str(center.name))
        data.append(str(center.center_description))
        temp[str(center.center_id)] = data
    return temp


def get_centers_from_auto_field(search_args):
    centers = Center.objects.filter(Q(name__icontains=search_args) | Q(location_city__icontains=search_args) | Q(location_state__icontains=search_args))
    return_data = []
    print(len(centers))
    print(len(Center.objects.all()))
    for center in centers:
        name = ''
        if center.name is not None:
            name = center.name

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