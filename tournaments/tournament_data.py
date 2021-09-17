import json

from ScratchBowling.sbs_utils import is_valid_uuid


class Qualifying:
    user_id = None
    place = 0
    scores = []

class MatchPlay:
    user_id = None
    place = 0
    scores = []

def get_qualifying_object(tournament):
    if tournament is None:
        return None

    import_data = tournament.qualifiers.replace("'", '"')
    try:
        import_data = json.loads(import_data)
    except ValueError:
        return None
    if import_data is None:
        return None

    qualifyings = []
    for data in import_data:
        user_id = is_valid_uuid(data[1])
        if user_id is not None:
            qualifying = Qualifying()
            qualifying.user_id = user_id
            # set place
            qualifying.place = 0
            try:
                qualifying.place = int(data[0])
            except TypeError:
                qualifying.place = 0

            # set scores
            qualifying.scores = []
            for x in range(2, len(data) - 1):
                score = 0
                try:
                    score = int(data[x])
                except TypeError:
                    score = 0
                qualifying.scores.append(score)
            qualifyings.append(qualifying)
    return qualifyings

def get_matchplay_object(tournament):
    import_data = tournament.matchplay.replace("'", '"')
    try:
        import_data = json.loads(import_data)
    except ValueError:
        return None
    if import_data is None:
        return None

    matchplays = []
    for data in import_data:
        user_id = is_valid_uuid(data[1])
        if user_id is not None:
            matchplay = MatchPlay()
            matchplay.user_id = user_id
            # set place
            matchplay.place = 0
            try:
                matchplay.place = int(data[0])
            except TypeError:
                matchplay.place = 0

            # set scores
            matchplay.scores = []
            for x in range(2, len(data) - 1):
                score = 0
                try:
                    score = int(data[x])
                except TypeError:
                    score = 0
                qualifying.scores.append(score)
            matchplays.append(matchplay)
    return matchplays






class Tournament_Data:
    tournament_id = None
    number_of_qualifying_matches = 1
    match_datas = []

class Match_Data:
    match_number = 0
    bowler_datas = []

class Bowler_Data:
    user_id = None
    total_score = 0
    game_datas = []

class Game_Data:
    game_number = 0
    scores = []
    total_score = 0
    pin_datas = None

class Pin_Data:
    # BINARY FORMAT (x10) ex. '0110101001' 1 Pin Up : 0 Pin Down
    pins = 0


def convert_to_tournament_data_object(tournament):
    if tournament != None:
        tournament_data = Tournament_Data()
        tournament_data.tournament_id = tournament.tournament_id
        ## CONVERT QUALIFYING INTO MATCH DATA
        qualifying_objects = get_qualifying_object(tournament)
        if qualifying_objects != None:
            qualifying_match = Match_Data()
            qualifying_match.match_number = 1
            for qualifying in qualifying_objects:
                bowler_data = Bowler_Data()
                bowler_data.user_id = qualifying.user_id
                game_number = 0
                for score in qualifying.scores:
                    game_number += 1
                    game_data = Game_Data()
                    game_data.game_number = game_number
                    game_data.total_score = score
                    bowler_data.game_datas.append(game_data)
                qualifying_match.bowler_datas.append(bowler_data)
            tournament_data.match_datas.append(qualifying_match)
        ## CONVERT MATCHPLAY INTO MATCH DATA
        matchplay_objects = get_matchplay_object(tournament)
        if matchplay_objects != None:
            match_datas = []
            for matchplay in matchplay_objects:
                last_match_index = -1
                placed = False
                for match_data in match_datas:
                    last_match_index += 1
                    exists = False
                    for bowler_data in match_data.bowler_datas:
                        if bowler_data.user_id == matchplay.user_id:
                            exists = True
                            break
                    if not exists:
                        bowler_data = Bowler_Data()
                        bowler_data.user_id = matchplay.user_id
                        game_number = 0
                        for score in matchplay.scores:
                            game_number += 1
                            game_data = Game_Data()
                            game_data.game_number = game_number
                            game_data.total_score = score
                            bowler_data.game_datas.append(game_data)
                        match_data.bowler_datas.append(bowler_data)
                        placed = True
                        break
                if placed == False:
                    match_data = Match_Data()
                    bowler_data = Bowler_Data()
                    bowler_data.user_id = matchplay.user_id
                    game_number = 0
                    for score in matchplay.scores:
                        game_number += 1
                        game_data = Game_Data()
                        game_data.game_number = game_number
                        game_data.total_score = score
                        bowler_data.game_datas.append(game_data)
                    match_data.bowler_datas.append(bowler_data)
                    match_datas.append(match_data)

            match_number = tournament_data.match_datas.count()
            for match_data in match_datas:
                match_number += 1
                match_data.match_number = match_number
                tournament_data.match_datas.append(match_data)

        return tournament_data
    return None

## GET AVERAGE SCORE
def get_average_score_game(game_data):
    average = 0
    average_count = 0
    average_total = 0
    for score in game_data.scores:
        average_count += 1
        average_total += score
    if average_total != 0 and average_count != 0:
        average = average_total / average_count
    return average
def get_average_score_match(bowler_data):
    average = 0
    average_count = 0
    average_total = 0
    for game_data in bowler_data.game_datas:
        average_count += 1
        average_total += game_data.total_score
    if average_total != 0 and average_count != 0:
        average = average_total / average_count
    return average
def get_average_score_tournament(tournament_data, user_id):
    average = 0
    average_count = 0
    average_total = 0
    for match_data in tournament_data.match_datas:
        for bowler_data in match_data.bowler_datas:
            if bowler_data.user_id == user_id:
                for game_data in bowler_data.game_datas:
                    average_count += 1
                    average_total += game_data.total_score
                break
    if average_total != 0 and average_count != 0:
        average = average_total / average_count
    return average

## GET HIGH SCORE
def get_high_score_tournament(tournament_data, user_id):
    highest_score = 0
    for match_data in tournament_data.match_datas:
        for bowler_data in match_data.bowler_datas:
            if bowler_data.user_id == user_id:
                for game_data in bowler_data.game_datas:
                    if game_data.total_score > highest_score:
                        highest_score = game_data.total_score
                break
    return highest_score

## GET TOTAL GAMES
def get_total_games_tournament(tournament_data, user_id):
    total_games = 0
    for match_data in tournament_data.match_datas:
        for bowler_data in match_data.bowler_datas:
            if bowler_data.user_id == user_id:
                total_games += len(bowler_data.game_datas)
                break
    return total_games


class Placement_Data:
    user_id = 0
    place = 0
    average_score = 0
    high_score = 0
    total_games = 0

def get_placement_datas_from_tournament_data(tournament_data):
    placement_datas = []
    for match_data in tournament_data.match_datas:
        match_data.bowler_datas = sorted(match_data.bowler_datas, key=lambda x: x.total_score, reverse=True)
        place = 0
        for bowler_data in match_data.bowler_datas:
            place += 1
            exists = False
            for placement_data in placement_datas:
                if placement_data.user_id == bowler_data.user_id:
                    placement_data.place = place
                    exists = True
                    break
            if not exists:
                placement_data = Placement_Data()
                placement_data.user_id = bowler_data.user_id
                placement_data.place = place

    for placement_data in placement_datas:
        placement_data.average_score = get_average_score_tournament(tournament_data, placement_data.user_id)
        placement_data.high_score = get_high_score_tournament(tournament_data, placement_data.user_id)
        placement_data.total_games = get_total_games_tournament(tournament_data, placement_data.user_id)

    return placement_datas