import uuid
from django.contrib.auth import get_user_model
from scoreboard.ranking import deserialize_rank_data



User = get_user_model()

def get_name_from_uuid(uuid,last_name=True, bold_last=False, truncate_last=False):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        user = User.objects.filter(user_id=uuid).first()
        if user == None:
            return 'Unknown User'

        first = str(user.first_name)
        last = str(user.last_name)
        last_initial = last[0]

        if last_name == False:
            bold_last = False

        if truncate_last:
            if bold_last:
                return first + '&nbsp;<span class="bold">' + last_initial + '.</span>'
            else:
                if last_name:
                    return first + ' ' + last_initial + '.'
                else:
                    return first
        else:
            if bold_last:
                return first + '&nbsp;<span class="bold">' + last + '</span>'
            else:
                if last_name:
                    return first + ' ' + last_initial
                else:
                    return first
    return 'Unknown User'

def get_name_from_user(user,last_name=True, bold_last=False, truncate_last=False):
    if user == None:
        return 'Unknown User'

    first = str(user.first_name)
    last = str(user.last_name)
    last_initial = last[0]

    if last_name == False:
        bold_last = False

    if truncate_last:
        if bold_last:
            return first + '&nbsp;<span class="bold">' + last_initial + '.</span>'
        else:
            if last_name:
                return first + ' ' + last_initial + '.'
            else:
                return first
    else:
        if bold_last:
            return first + '&nbsp;<span class="bold">' + last + '</span>'
        else:
            if last_name:
                return first + ' ' + last_initial
            else:
                return first



def get_location_basic_uuid(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        user = User.objects.filter(user_id=uuid).first()
        if user is not None:
            city = str(user.location_city)
            state = str(user.location_state)
            if city == None or city == '':
                if state == None or state == '':
                    return 'Location Unknown'
                else:
                    return state
            elif state == None or state == '':
                return city
            else:
                return city + ', ' + state


def get_location_basic_obj(user):
        if user is not None:
            city = str(user.location_city)
            state = str(user.location_state)
            if city == None or city == '':
                if state == None or state == '':
                    return 'Location Unknown'
                else:
                    return state
            elif state == None or state == '':
                return city
            else:
                return city + ', ' + state
        return 'Location Unknown'


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


def display_get_bowlers(users):
    # FORMAT : Array of Lists
    # [id, name, location, rank, attend, wins, average]
    data = []
    for user in users:
        rank_data = deserialize_rank_data(user.statistics)
        if rank_data != None:
            data.append([str(user.user_id), get_name_from_user(user), get_location_basic_obj(user), make_ordinal(rank_data.rank), rank_data.attended, rank_data.wins, rank_data.average_score_career])
    return data


def make_ordinal(n):
    n = int(n)
    if n == 0:
        return '0'
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix