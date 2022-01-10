from datetime import datetime
import quickle

from centers.center_utils import get_center, get_center_location_obj
from tournaments.models import Tournament
from tournaments.roster import get_spots_available_obj, get_roster_length_obj
from tournaments.tournament_data import deserialize_placement_data, deserialize_tournament_data


def serialize_tournaments_list(tournaments):
    return quickle.dumps(tournaments)

def deserialize_tournaments_list(data):
    return quickle.loads(data)

def in_season(tournament):
    in_season = False
    if tournament.datetime.year == datetime.now().date().year:
        in_season = True
    return in_season

def get_count_all_tournaments():
    return Tournament.objects.all().count()

def get_all_completed_tournaments():
    return Tournament.objects.filter(finished=True, live=False)

def get_all_upcoming_tournaments():
    return Tournament.objects.filter(finished=False, live=False)

def get_all_live_tournaments():
    return Tournament.objects.filter(finished=False, live=True)

def get_count_completed_tournaments():
    return Tournament.objects.filter(finished=True, live=False).count()

def get_count_upcoming_tournaments():
    return Tournament.objects.filter(finished=False, live=False).count()

def get_count_live_tournaments():
    return Tournament.objects.filter(finished=False, live=True).count()

def get_tournament(tournament_id):
    return Tournament.objects.filter(tournament_id=tournament_id).first()

def get_place(placement_data, user_id):
    place = 0
    if placement_data != None:
        placements = deserialize_placement_data(placement_data)
        for placement in placements:
            if placement.user_id == user_id:
                place = placement.place
                break
    return place

def get_average(tournament, user_id):
    average = 0
    if tournament != None:
        placements = deserialize_placement_data(tournament.placement_data)
        for placement in placements:
            if placement.user_id == user_id:
                average = placement.average_score
                break
    return average

def get_winner(placement_data):
    if placement_data != None:
        placements = deserialize_placement_data(placement_data)
        for placement in placements:
            if placement.place == 1:
                return placement.user_id
    return None

def get_bowler_id_from_place(tournament_id, place):
    tournament = get_tournament(tournament_id)
    if tournament != None:
        placements = deserialize_placement_data(tournament.placement_data)
        for placement in placements:
            if placement.place == place:
                return placement.user_id
    return None

def get_top_placements(placement_data, count):
    ids = []
    if placement_data != None:
        placements = deserialize_placement_data(placement_data)
        while count > 0:
            for placement in placements:
                if placement.place == count:
                    ids.append([placement.user_id, get_name_from_uuid(placement.user_id, True, True)])
                    break
            count -= 1
    return ids

def get_all_tournaments(user_tournaments_data):
    tournaments = []
    if user_tournaments_data !=  None:
        tournament_ids = deserialize_tournaments_list(user_tournaments_data)
        for tournament_id in tournament_ids:
            tournament = get_tournament(tournament_id)
            if tournament != None:
                tournaments.append(tournament)
    return tournaments

def get_date_time(date, time):
    if date is not None and time is not None:
        date_str = date + ' ' + time
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    else:
        return datetime.now()

def qualifying_display_view(tournament_data):
    ## FORMAT
    ## [ 0=id, 1=name, 2=place, 3=scores, 4=total]
    tournament_data = deserialize_tournament_data(tournament_data)
    display_data = []
    if tournament_data != None:
        if tournament_data.number_of_qualifying_matches == 1:
            match_data = tournament_data.match_datas[0]
            for bowler_data in match_data.bowler_datas:
                scores = []
                for game_data in bowler_data.game_datas:
                    scores.append(game_data.total_score)

                display_data.append([bowler_data.user_id,
                                     get_name_from_uuid(bowler_data.user_id, True, True),
                                     0,## PLACE
                                     scores,
                                     bowler_data.total_score])

# DISPLAY CONVERSIONS
def convert_to_display_main_upcoming_list(tournament_list):
    temp_list = []
    for t in tournament_list:
        temp_list.append(convert_to_display_main_upcoming(t))
    return temp_list
def convert_to_display_main_upcoming(tournament):
    ## UPCOMING TOURNAMENTS FORMAT
    ## [0=id, 1=name, 2=date, 3=time, 4=sponsor_id, 5=center_id,
    # 6=center_name, 7=center_location, 8=spots_available, 9=spots_reserved, 10=entry_fee, 11=is_team_entry, 12=tags]
    center_name = 'Unknown Center'
    center_id = 0
    center_location = 'Unknown Location'
    center = get_center(tournament.center)
    if center != None:
        center_name = center.center_name
        center_id = center.center_id
        center_location = get_center_location_obj(center)
    is_team_entry = False
    spots_reserved = tournament.spots_reserved
    if 'double' in tournament.name:
        is_team_entry = True
    if 'Double' in tournament.name:
        is_team_entry = True
    if spots_reserved == 0:
        spots_reserved = 120



    return [tournament.id,
            tournament.name,
            tournament.datetime.strftime("%m/%d"),
            tournament.datetime.time(),
            tournament.get_sponsor_image(),
            center_id,
            center_name,
            center_location,
            tournament.get_roster_length(),
            spots_reserved,
            tournament.entry_fee,
            is_team_entry,
            tournament.get_tags()
            ]

def convert_to_display_main_results_list(tournament_list):
    temp_list = []
    for t in tournament_list:
        temp_list.append(convert_to_display_main_results(t))
    return temp_list
def convert_to_display_main_results(tournament):
    ## RESULTS TOURNAMENTS FORMAT
    ## [0=id, 1=name, 2=date, 3=sponsor_id, 4=center_id,
    # 5=center_name, 6=center_location, 7=participants, 8=winner_name, 9=winner_id, 10=winner_avg, 11=tags]
    center_name = 'Unknown Center'
    center_id = 0
    center_location = 'Unknown Location'
    center = get_center(tournament.center)
    if center != None:
        center_name = center.center_name
        center_id = center.center_id
        center_location = get_center_location_obj(center)

    winner_id = get_winner(tournament.placement_data)
    winner = get_name_from_uuid(winner_id, True, True, True)
    winner_average = get_average(tournament, winner_id)

    date = tournament.datetime.date()
    if date.year == datetime.now().year:
        date = date.strftime('%m/%d')
    else:
        date = date.strftime('%m/%d/%y')

    return [tournament.id,
            tournament.name,
            date,
            tournament.get_sponsor_image(),
            center_id,
            center_name,
            center_location,
            get_roster_length_obj(tournament),
            winner,
            winner_id,
            winner_average,
            tournament.get_tags()
            ]