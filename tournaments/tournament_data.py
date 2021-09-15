import json


class Qualifying:
    user_id = None
    place = 0
    scores = []


class MatchPlay:
    user_id = None
    place = 0
    scores = []


class Score_Data:
    user_id = None
    score = 0
    start_time = None
    end_time = None
    total_time = 0


class Game_Data:
    game_number = 0
    score_datas = []


class Tournament_Data:
    tournament_id = None
    game_datas = []


def data_to_json(data):
    return json.dumps(data)


def data_from_json(json_str):
    return json.loads(json_str)


def create_score_data(user_id, score, start_time=0, end_time=0, total_time=0):
    score_data = Score_Data()
    score_data.user_id = user_id
    score_data.score = score
    score_data.start_time = start_time
    score_data.end_time = end_time
    score_data.total_time = total_time
    return score_data


def add_to_game_data(tournament_data, score_data):
    tournament_data.game_datas.append(score_data)










