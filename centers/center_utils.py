from centers.models import Center


def get_center_location_uuid(uuid):
    center = Center.objects.filter(center_id=uuid).first()
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