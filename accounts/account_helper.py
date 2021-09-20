import uuid

from django.contrib.auth import get_user_model

User = get_user_model()

def get_name_from_uuid(uuid,last_name=True, bold_last=False, truncate_last=False):
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
