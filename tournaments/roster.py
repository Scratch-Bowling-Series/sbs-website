import quickle
from random import randrange
from ScratchBowling.sbs_utils import is_valid_uuid
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


def roster_data_display(roster):
    datas = []
    for user_id in roster:
        user = get_user_uuid(user_id)
        if user:
            statistics = user.statistics
            if statistics:
                datas.append([user_id, user.first_name, user.last_name, user.short_location, statistics.rank, statistics.rank_badge])
    return sorted(datas, key=lambda x: x[4])
