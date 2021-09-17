from datetime import datetime


def in_season(tournament):
    in_season = False
    if tournament.tournament_date.year == datetime.now().date().year:
        in_season = True
    return in_season