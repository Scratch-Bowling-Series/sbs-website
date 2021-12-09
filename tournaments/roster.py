import quickle
from random import randrange
from ScratchBowling.sbs_utils import is_valid_uuid
from accounts.account_helper import get_name_from_user, get_rank_from_user, get_user_uuid, get_amount_users, \
    get_rank_color
from tournaments.models import Tournament
from tournaments.tournament_data import deserialize_placement_data

def fix_scraped_tournament_rosters():
    tournaments = Tournament.objects.filter(finished=True)
    for tournament in tournaments:
        roster = []
        placements = deserialize_placement_data(tournament.placement_data)
        for placement in placements:
            roster.append(str(placement.user_id))
        tournament.roster = serialize_roster_data(roster)
    Tournament.objects.bulk_update(tournaments)

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


def roster_data_display(roster, bold_last=True):
    datas = []
    for user_id in roster:
        user = get_user_uuid(user_id)
        if user != None:
            datas.append([user_id, get_name_from_user(user, True, bold_last), get_rank_from_user(user.statistics, False)])
        else:
            datas.append([0, 'Unknown Name', randrange(1, 4000)])


    datas = sorted(datas, key=lambda x: x[2])
    total_users = get_amount_users()
    for data in datas:
        data[2] = get_rank_color(data[2], total_users)

    return datas

