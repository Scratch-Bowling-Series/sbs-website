import datetime
import json
import os
import quickle
from datetime import datetime
from itertools import islice
from django.contrib.auth import get_user_model
from django.db import transaction
from tournaments.models import Tournament
from tournaments.tournament_data import get_matchplay_object, get_qualifying_object, convert_to_tournament_data_all_tournaments, deserialize_tournament_data, deserialize_placement_data
from tournaments.tournament_utils import in_season, serialize_tournaments_list

User = get_user_model()

## RANKING DATA OBJECT STORAGE ##
class RankPointData:
    points = 0
    date = None

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

def serialize_rank_data(rank_data):
    return quickle.Encoder(registry=[RankData]).dumps(rank_data)

def deserialize_rank_data(data):
    return quickle.Decoder(registry=[RankData]).loads(data)





class RankData_Series:
    series_id = None

    attended = 0
    total = 0
    wins = 0
    rank = 0

    rank_points = 0

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


## EXTERNAL RANKING DATA ACCESS FUNCTIONS ##

def get_top_rankings(amount):
    rank_datas = load_rank_data()
    if rank_datas != None:
        return rank_datas[:amount]

def get_rank_data_from_json(json_data):
    if json_data is not None and len(json_data) > 5:
        import_data = json.loads(json_data)
        rank_data = RankData()
        rank_data.user_id = import_data[0]
        rank_data.rank = import_data[1]
        rank_data.rank_points = import_data[2]
        rank_data.wins = import_data[3]
        rank_data.attended = import_data[4]
        rank_data.total_games_year = import_data[5]
        rank_data.total_games_career = import_data[6]
        rank_data.avg_score_year = import_data[7]
        rank_data.avg_score_career = import_data[8]
        rank_data.top_five_year = import_data[9]
        rank_data.top_five_career = import_data[10]
        return rank_data
    return None


## RUN STATISTICS FUNCTION ##

def convert_tournaments():
    convert_to_tournament_data_all_tournaments()

def calculate_statistics():
    print("RankingSys - Initializing...")
    rank_datas = get_rank_datas_from_all_tournaments()
    apply_rank_data_to_accounts_in_batches(rank_datas, 1000)
    print("RankingSys - Saving Ranking Data to 'rankings.dat'.")
    store_rank_data(rank_datas)
    print('RankingSys - Finished')


## STATISTICS PROCESS TASKS ##

def apply_rank_data_to_accounts_in_batches(rank_datas, batch_size):
    if batch_size < 200: batch_size = 200
    count = 0
    total = 0
    total_batches = int(len(rank_datas) / batch_size)
    while True:
        count += 1
        start = 0 + (batch_size * (count - 1))
        batch = list(islice(rank_datas, start, batch_size * count))
        if not batch: break
        total += apply_rank_data_to_accounts(batch, count, total_batches)
    return total

@transaction.atomic
def apply_rank_data_to_accounts(rank_datas, batch, total_batches):
    print('RankingSys - Saving Ranking Data')
    if rank_datas == None: return 0
    data_count = 0
    total = len(rank_datas)
    last_prog = 0
    for data in rank_datas:
        prog = int((data_count / total) * 100)
        if last_prog != prog:
            last_prog = prog
            print('RankingSys - Saving Ranking Data - Batch: (' + str(batch) + '/'+ str(total_batches) + ') - Progress: ' + str(prog) + '%')
        data_count += 1
        data.rank = data_count
        write_user = User.objects.filter(user_id=data.user_id).first()
        if write_user != None:
            write_user.tournaments = serialize_tournaments_list(data.tournaments)
            data.tournaments = []
            write_user.statistics = serialize_rank_data(data)
            write_user.save()
    return data_count

def get_rank_data_from_tournaments():
    rank_data_lib = []
    tournaments = Tournament.objects.all()
    tournaments_length = tournaments.count()
    ## LOGGING
    log_count = 0
    log_total = tournaments_length
    log_prog_las = 0
    log_prog_inc = 0
    for tournament in tournaments:
        ## LOGGING
        log_count += 1
        log_prog = int((log_count / log_total) * 100)
        if log_prog_las != log_prog:
            log_prog_las = log_prog
            if log_prog >= log_prog_inc:
                log_prog_inc += 25
                print('RankingSys - Calculating Statistics - Progress: ' + str(log_prog) + '%')

        ## CHECK IF TOURNAMENT IS IN SEASON


        ## GET TOURNAMENT DATA
        qualifying_objects = get_qualifying_object(tournament)
        matchplay_objects = get_matchplay_object(tournament)
        if qualifying_objects == None and matchplay_objects == None: continue

        ## CREATE PLACEMENTS FROM QUALIFYINGS AND MATPLAY
        for qualifying in qualifying_objects:
            for matchplay in matchplay_objects:
                if qualifying.user_id == matchplay.user_id:
                    qualifying.place = matchplay.place
                    qualifying.scores += matchplay.scores
                    break
        qualifying_objects_length = len(qualifying_objects)

        ## UPDATE DATA LIBRARY WITH PLACEMENTS
        for placement in qualifying_objects:

            ## get rank data object
            rank_data = None
            for data in rank_data_lib:
                if data.user_id == placement.user_id:
                    rank_data = data
            if rank_data == None:
                rank_data = RankData()
                rank_data.user_id = placement.user_id
                rank_data_lib.append(rank_data)
            if rank_data == None:
                continue

            t_score_average = task_get_average(placement.scores)
            if placement.scores == None:
                t_total_games = 0
            else:
                t_total_games = len(placement.scores)
            # season data
            if in_season:
                # get rank points
                rank_data.rank_points = task_get_rank_points(placement, t_score_average, qualifying_objects_length,tournament.tournament_date)
                # get avg score year
                rank_data.avg_score_year_total += t_score_average
                rank_data.avg_score_year_amount += 1
                rank_data.avg_score_year = round(rank_data.avg_score_year_total / rank_data.avg_score_year_amount, 2)
                # get best games year
                rank_data.top_five_year = task_best_score(rank_data.top_five_year, placement.scores,tournament.tournament_id)
            # get avg score career
            rank_data.avg_score_career_total += t_score_average
            rank_data.avg_score_career_amount += 1
            rank_data.avg_score_career = round(rank_data.avg_score_career_total / rank_data.avg_score_career_amount, 2)
            # get total wins
            if placement.place == 1:
                rank_data.wins += 1
            # get attended
            rank_data.attended += 1
            # get total games year
            rank_data.total_games_year += t_total_games
            # get total games career
            rank_data.total_games_career += t_total_games
            # get best games career
            rank_data.top_five_career = task_best_score(rank_data.top_five_career, placement.scores,tournament.tournament_id)
            # add tournament to list
            rank_data.tournaments = task_store_tournament(tournament.tournament_id, rank_data.tournaments)
    return sorted(rank_data_lib, key=lambda x: x.rank_points, reverse=True)

def get_rank_datas_from_all_tournaments():
    rank_data_lib = []
    tournaments = Tournament.objects.all()
    tournaments_length = tournaments.count()
    ## LOGGING
    log_count = 0
    log_total = tournaments_length
    log_prog_las = 0
    log_prog_inc = 0
    for tournament in tournaments:
        tournament_data = deserialize_tournament_data(tournament.tournament_data)
        placement_datas = deserialize_placement_data(tournament.placement_data)
        ## LOGGING
        log_count += 1
        log_prog = int((log_count / log_total) * 100)
        if log_prog_las != log_prog:
            log_prog_las = log_prog
            if log_prog >= log_prog_inc:
                log_prog_inc += 5
                print('RankingSys - Calculating Statistics - Progress: ' + str(log_prog) + '%')

        placements_length = len(placement_datas)

        for placement in placement_datas:
            ## get rank data object
            rank_data = None
            for data in rank_data_lib:
                if data.user_id == placement.user_id:
                    rank_data = data
            if rank_data == None:
                rank_data = RankData()
                rank_data.user_id = placement.user_id
                rank_data_lib.append(rank_data)
            if rank_data == None:
                continue

            # season data
            if in_season(tournament):
                # get rank points
                rank_data.rank_points = task_get_rank_points(placement, placement.average_score, placements_length,tournament.tournament_date)
                print(str(rank_data.rank_points) + '   :     ' + str(rank_data.user_id))
                # get avg score year
                rank_data.avg_score_year_total += placement.average_score
                rank_data.avg_score_year_amount += 1
                rank_data.avg_score_year = round(rank_data.avg_score_year_total / rank_data.avg_score_year_amount, 2)
                # get best games year
                rank_data.top_five_year = task_best_score(rank_data.top_five_year, placement.high_score,tournament.tournament_id)
            # get avg score career
            rank_data.avg_score_career_total += placement.average_score
            rank_data.avg_score_career_amount += 1
            rank_data.avg_score_career = round(rank_data.avg_score_career_total / rank_data.avg_score_career_amount, 2)
            # get total wins
            if placement.place == 1:
                rank_data.wins += 1
            # get attended
            rank_data.attended += 1
            # get total games year
            rank_data.total_games_year += placement.total_games
            # get total games career
            rank_data.total_games_career += placement.total_games
            # get best games career
            rank_data.top_five_career = task_best_score(rank_data.top_five_career, placement.high_score,tournament.tournament_id)
            # add tournament to list
            rank_data.tournaments = task_store_tournament(tournament.tournament_id, rank_data.tournaments)
    return sorted(rank_data_lib, key=lambda x: x.rank_points, reverse=True)

def get_rank_data(rank_datas, user_id):
    for rank_data in rank_datas:
        if rank_data.user_id == user_id:
            return rank_data
    instance = RankData()
    instance.user_id = user_id
    rank_datas.append(instance)
    return instance

def task_get_rank_points(placement, avgerage, length, date):
    # calculate points
    place_points = 0
    score_points = 0
    if placement.place != 0:
        place_points = (4000 / placement.place) * (length / 50)
    if avgerage !=  0:
        score_points = (((avgerage / 10) * avgerage) / 10)
    total_points = place_points + score_points

    # apply decay
    delta = datetime.now().date() - date
    if delta.days >= 0:
        decay = 0.002 * delta.days
        total_points = total_points - (total_points * decay)
    return round(total_points)

def task_get_average(scores):
    if scores == None:
        return 0
    amount = len(scores)
    total = sum(scores)
    average = round(total / amount, 2)
    return average

def task_best_score(top_five, best_score, tournament_id):
    top_1 = top_five[0]
    top_2 = top_five[1]
    top_3 = top_five[2]
    top_4 = top_five[3]
    top_5 = top_five[4]

    if top_1 is None:
        top_1 = [str(tournament_id), best_score]
    else:
        if best_score > top_1[1]:
            top_2 = top_1
            top_1[1] = best_score
            top_1[0] = str(tournament_id)
        elif top_2 is None:
            top_2 = [str(tournament_id), best_score]
        elif best_score > top_2[1]:
            top_3 = top_2
            top_2[1] = best_score
            top_2[0] = str(tournament_id)
        elif top_3 is None:
            top_3 = [str(tournament_id), best_score]
        elif best_score > top_3[1]:
            top_4 = top_3
            top_3[1] = best_score
            top_3[0] = str(tournament_id)
        elif top_4 is None:
            top_4 = [str(tournament_id), best_score]
        elif best_score > top_4[1]:
            top_5 = top_4
            top_4[1] = best_score
            top_4[0] = str(tournament_id)
        elif top_5 is None:
            top_5 = [str(tournament_id), best_score]
        elif best_score > top_5[1]:
            top_5[1] = best_score
            top_5[0] = str(tournament_id)

    return [top_1, top_2, top_3, top_4, top_5]

def task_store_tournament(tournament_id, tournaments):
    exists = False
    for id in tournaments:
        if id == str(tournament_id):
            exists = True
            break
    if not exists:
        tournaments.append(str(tournament_id))
    return tournaments






if __name__ == "__main__":
    calculate_statistics()