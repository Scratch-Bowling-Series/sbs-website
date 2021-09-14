import datetime
import json
import os
from datetime import datetime
from itertools import islice

from django.contrib.auth import get_user_model
from django.db import transaction

from tournaments.models import Tournament
from tournaments.views import get_qualifying, get_matchplay, get_qualifying_object, get_matchplay_object, get_placements
User = get_user_model()




## RANKING DATA OBJECT STORAGE ##
class RankData:
    user_id = None
    rank = 0
    rank_points = 0
    wins = 0
    attended = 0
    total_games_year = 0
    total_games_career = 0
    avg_score_year = 0
    avg_score_year_amount = 0
    avg_score_year_total = 0
    avg_score_career = 0
    avg_score_career_amount = 0
    avg_score_career_total = 0
    top_five_year = [None, None, None, None, None]
    top_five_career = [None, None, None, None, None]
    tournaments = []
    def rd_to_json(self):
        return json.dumps([
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
        ])
    def t_to_json(self):
        return json.dumps(self.tournaments)
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

class RankData_Series:
    series_id = None

    attended = 0
    total = 0
    wins = 0
    rank = 0

    rank_points = 0

def store_rank_data(rank_datas):
    try:
        datas = []
        pwd = os.path.dirname(__file__)
        for rank_data in rank_datas:
            datas.append(rank_data.to_list())
        file = open(pwd + '/rankings.dat', 'w')
        file.write(json.dumps(datas))
        file.close()
    except FileNotFoundError:
        return None

def load_rank_data():
    try:
        pwd = os.path.dirname(__file__)
        file = open(pwd + '/rankings.dat', 'r')
        datas = json.loads(file.read())
        rank_datas = []
        for data in datas:
            rank_data = RankData()
            rank_data.user_id = data[0]
            rank_data.rank = data[1]
            rank_data.rank_points = data[2]
            rank_data.wins = data[3]
            rank_data.attended = data[4]
            rank_data.total_games_year = data[5]
            rank_data.total_games_career = data[6]
            rank_data.avg_score_year = data[7]
            rank_data.avg_score_career = data[8]
            rank_data.top_five_year = data[9]
            rank_data.top_five_career = data[10]
            rank_datas.append(rank_data)
        return rank_datas
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

def run_statistics():
    tournaments = Tournament.objects.all()
    rank_datas = []
    count = 0
    length = tournaments.count()
    past_prog = 0
    print('RankingSys - Starting Statistics Calculations')
    for tournament in tournaments:
        count += 1
        progress = int((count / length ) * 100)
        if past_prog != progress:
            past_prog = progress
            print('RankingSys - Running Statistics - Progress: ' + str(progress) + '%')
        in_season = False
        if tournament.tournament_date.year == datetime.now().date().year:
            in_season = True
        placements = get_placements(tournament)
        if placements is None:
            continue
        for placement in placements:
            rank_data = get_rank_data(rank_datas, placement.user_id)

            average = task_get_average(placement)

            # get rank points
            if in_season:
                rank_data.rank_points = task_get_rank_points(placement, average, len(placements), tournament.tournament_date)

            # get avg score year
            if in_season:
                rank_data.avg_score_year_total += average
                rank_data.avg_score_year_amount += 1
                rank_data.avg_score_year = round(rank_data.avg_score_year_total / rank_data.avg_score_year_amount, 2)

            # get avg score career
            rank_data.avg_score_career_total += average
            rank_data.avg_score_career_amount += 1
            rank_data.avg_score_career = round(rank_data.avg_score_career_total / rank_data.avg_score_career_amount, 2)

            # get total wins
            if placement.place == 1:
                rank_data.wins += 1

            # get attended
            rank_data.attended += 1

            # get total games year
            rank_data.total_games_year = rank_data.avg_score_year_amount

            # get total games career
            rank_data.total_games_career = rank_data.avg_score_career_amount

            # get best games year
            if in_season:
                rank_data.top_five_year = task_best_score(rank_data.top_five_year, placement.scores, tournament.tournament_id)

            # get best games career
            rank_data.top_five_career = task_best_score(rank_data.top_five_career, placement.scores,tournament.tournament_id)

            # add tournament to list
            rank_data.tournaments.append(str(tournament.tournament_id))


    rank_datas = sorted(rank_datas, key=lambda x: x.rank_points, reverse=True)
    store_rank_data(rank_datas)
    apply_rank_data_to_accounts_in_batches(rank_datas, 300)
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
            write_user.statistics = data.rd_to_json()
            write_user.tournaments = data.t_to_json()
            write_user.save()
    return data_count

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

def task_get_average(placement):
    amount = len(placement.scores)
    total = sum(placement.scores)
    average = round(total / amount, 2)
    return average

def task_best_score(top_five, scores, tournament_id):
    best_score = 0
    for score in scores:
        if score > best_score:
            best_score = score

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


if __name__ == "__main__":
    run_statistics()