from datetime import datetime

from tournaments.models import Tournament
from tournaments.tournament_data import deserialize_placement_data


def in_season(tournament):
    in_season = False
    if tournament.tournament_date.year == datetime.now().date().year:
        in_season = True
    return in_season

def get_tournament(tournament_id):
    return Tournament.objects.filter(tournament_id=tournament_id).first()

def get_place(tournament_id, user_id):
    place = 0
    tournament = get_tournament(tournament_id)
    if tournament != None:
        placements = deserialize_placement_data(tournament.placement_data)
        for placement in placements:
            if placement.user_id == user_id:
                place = placement.place
                break
    return place

def get_average(tournament_id, user_id):
    average = 0
    tournament = get_tournament(tournament_id)
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

def get_bowler_from_place(tournament_id, place):
    tournament = get_tournament(tournament_id)
    if tournament != None:
        placements = deserialize_placement_data(tournament.placement_data)
        for placement in placements:
            if placement.place == place:
                return placement.user_id
    return None


def make_ordinal(n):
    n = int(n)
    if n == 0:
        return '0'
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix