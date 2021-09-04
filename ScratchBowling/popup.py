from django.db.models import Q

from accounts.account_helper import get_location_basic_obj, User


class Popup:
    popup_id = 0
    data = 0
    data_length = 0

def cut_last_name(users, last_name):
    cut = users.filter(Q(last_name__icontains=last_name))
    if cut.count() > 0:
        return cut
    else:
        cut = users.filter(Q(last_name__icontains=last_name[:3]))
        if cut.count() > 0:
            return cut
        else:
            cut = users.filter(Q(last_name__icontains=last_name[:2]))
            if cut.count() > 0:
                return cut
            else:
                cut = users.filter(Q(last_name__icontains=last_name[:1]))
                if cut.count() > 0:
                    return cut
        return users

def check_for_popup(user):
    if user != None and user.is_anonymous == False:
        if user.ask_for_claim:
            users = User.objects.filter(first_name__icontains=str(user.first_name), unclaimed = True)

            if users.count() > 4:
                users = cut_last_name(users, str(user.last_name))
            elif users.count() == 0:
                users = User.objects.filter(first_name__icontains=str(user.first_name)[:5], unclaimed = True)
                if users.count() > 4:
                    users = cut_last_name(users, str(user.last_name))
                elif users.count() == 0:
                    return None
            shadow_list = []
            for shadow in users[:4]:
                shadow_list.append([str(shadow.first_name) + ' ' + str(shadow.last_name), get_location_basic_obj(shadow)])

            popup = Popup()
            popup.popup_id = 2
            popup.data = shadow_list
            popup.data_length = len(shadow_list)
            return popup




