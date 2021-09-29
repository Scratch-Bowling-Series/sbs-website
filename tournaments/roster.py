from random import randrange

from ScratchBowling.sbs_utils import is_valid_uuid
import quickle

from accounts.account_helper import get_name_from_uuid, get_location_basic_uuid, get_name_from_user, get_rank_from_user, \
    get_user_uuid, make_ordinal, get_amount_users


def add_user_to_roster_obj(tournament, user_id):
    roster_data = tournament.roster
    if roster_data != None:
        user_id = is_valid_uuid(user_id)
        if user_id != None:
            user_id = str(user_id)
            roster = quickle.loads(roster_data)
            roster_length = len(roster)
            if roster_length < tournament.spots_reserved:
                exists = False
                for user in roster:
                    if user == user_id:
                        exists = True
                if not exists:
                    roster.append(user_id)
                    tournament.roster = quickle.dumps(roster)


def remove_user_from_roster_obj(tournament, user_id):
    roster_data = tournament.roster
    if roster_data != None:
        user_id = is_valid_uuid(user_id)
        if user_id != None:
            user_id = str(user_id)
            roster = quickle.loads(roster_data)
            new_roster = []
            for user in roster:
                if user != user_id:
                    new_roster.append(user)
            tournament.roster = quickle.dumps(new_roster)


def get_roster_length_obj(tournament):
    roster_data = tournament.roster
    if roster_data != None:
        roster = quickle.loads(roster_data)
        if roster != None:
            return len(roster)


def get_spots_available_obj(tournament):
    roster_data = tournament.roster
    if roster_data != None:
        roster = quickle.loads(roster_data)
        if roster != None:
            available = tournament.spots_reserved - len(roster)
            if available < 0:
                available = 0
            return available


def serialize_roster_data(roster):
    return quickle.dumps(roster)


def deserialize_roster_data(roster_data):
    return quickle.loads(roster_data)


def roster_data_display(roster):
    datas = []
    for user_id in roster:
        user = get_user_uuid(user_id)
        if user != None:
            datas.append([user_id, get_name_from_user(user), get_rank_from_user(user.statistics, False)])
        else:
            datas.append([0, 'Unknown Name', randrange(1, 4000)])


    datas = sorted(datas, key=lambda x: x[2])
    total_users = get_amount_users()
    for data in datas:
        data[2] = get_rank_color(data[2], total_users)

    return datas

def get_rank_color(rank, total_users):
    diamond = total_users / 10
    gold = total_users / 5
    silver = total_users / 2.5

    diamond_icon = 'icon-play'
    diamond_color = '#42d1f5'

    gold_icon = 'icon-play'
    gold_color = '#f5d442'

    silver_icon = 'icon-play'
    silver_color = '#c2c2c2'

    bronze_icon = 'icon-play'
    bronze_color = '#CD7F32'
    if rank > 0 and rank <= diamond:
        return create_icon_html(diamond_icon, diamond_color)
    elif rank > diamond and rank <= gold:
        return create_icon_html(gold_icon, gold_color)
    elif rank > gold and rank <= silver:
        return create_icon_html(silver_icon, silver_color)
    elif rank > silver:
        return create_icon_html(bronze_icon, bronze_color)


def create_icon_html(icon, color, clss=''):
    return '<i class="' + icon + ' ' + clss + '" style="color:' + color + ';"></i>'