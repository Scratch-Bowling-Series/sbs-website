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
            if placement.bowler_id == user_id:
                place = placement.place
                break
    return place

def get_winner(placement_data):
    if placement_data != None:
        placements = deserialize_placement_data(placement_data)
        for placement in placements:
            if placement.place == 1:
                return placement.bowler_id
    return None