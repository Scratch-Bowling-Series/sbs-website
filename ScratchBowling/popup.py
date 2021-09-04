from django.db.models import Q

from accounts.account_helper import get_location_basic_obj, User


def check_for_popup(user):
    if user != None and user.is_anonymous == False:
        if user.ask_for_claim:
            shadows = User.objects.filter(first_name=str(user.first_name), unclaimed = True)
            if shadows.count() > 15:
                cut = shadows.filter(Q(last_name__icontains=str(user.last_name)[0]))
                if cut.count() > 0:
                    shadows = cut
            elif shadows.count() == 0:
                return None
            shadow_list = []
            for shadow in shadows:
                shadow_list.append([str(shadow.first_name) + ' ' + str(shadow.last_name), get_location_basic_obj(shadow)])
            return [shadow_list, False, True, False, False, False]