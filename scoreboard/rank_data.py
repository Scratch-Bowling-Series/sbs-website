import os
import quickle



class RankData(quickle.Struct):
    user_id : str = None
    rank : int = 0
    rank_points : int = 0
    rank_point_data : list = []
    wins : int = 0
    attended : int = 0
    total_games_year : int = 0
    total_games_career : int = 0
    avg_score_year : int = 0
    avg_score_year_amount : int = 0
    avg_score_year_total : int = 0
    avg_score_career : int = 0
    avg_score_career_amount : int = 0
    avg_score_career_total : int = 0
    top_five_year : list = [None, None, None, None, None]
    top_five_career : list = [None, None, None, None, None]
    tournaments : list = []
    def to_list(self):
        return [
            str(self.user_id),
            self.rank,
            self.rank_points,
            self.wins,
            self.attended,
            self.total_games_year,
            self.total_games_career,
            self.avg_score_year,
            self.avg_score_career,
            self.top_five_year,
            self.top_five_career
        ]

class RankPointData:
    points = 0
    date = None

class RankData_Series:
    series_id = None

    attended = 0
    total = 0
    wins = 0
    rank = 0

    rank_points = 0




def serialize_rank_data(rank_data):
    if rank_data != None:
        return quickle.Encoder(registry=[RankData]).dumps(rank_data)

def deserialize_rank_data(data):
    if data != None:
        return quickle.Decoder(registry=[RankData]).loads(data)

def store_rank_data(rank_datas):
    try:
        pwd = os.path.dirname(__file__)
        file = open(pwd + '/rankings.dat', 'wb')
        file.write(serialize_rank_data(rank_datas))
        file.close()
    except FileNotFoundError:
        return None

def load_rank_data():
    try:
        pwd = os.path.dirname(__file__)
        file = open(pwd + '/rankings.dat', 'rb')
        return deserialize_rank_data(file.read())
    except FileNotFoundError:
        return None
