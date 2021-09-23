from ScratchBowling.sbs_utils import is_valid_uuid
from centers.models import Center



def get_center(center_id):
    center_id = is_valid_uuid(center_id)
    if center_id != None:
        return Center.objects.filter(center_id=center_id).first()
    else:
        return None

def get_center_location_uuid(center_id):
    return str(center_id)
    center = get_center(center_id)
    if center != None:
        city = str(center.location_city)
        state = str(center.location_state)
        if city == None or city == '':
            if state == None or state == '':
                return 'Location Unknown'
            else:
                return state
        elif state == None or state == '':
            return city
        else:
            return city + ', ' + state
    else:
        return 'Location Unknown'

def get_center_name_uuid(center_id):
    center = get_center(center_id)
    if center != None:
        return str(center.center_name)
    else:
        return 'Location Unknown'