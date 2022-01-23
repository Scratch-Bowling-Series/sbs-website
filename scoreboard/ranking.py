import datetime
from datetime import datetime
from itertools import islice
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from scoreboard.models import Statistics
from scoreboard.rank_data import store_rank_data, serialize_rank_data, RankData
from tournaments.models import Tournament, GameData, TournamentData

User = get_user_model()

## RUN STATISTICS FUNCTION ##

@transaction.atomic
def calculate_statistics(logging=False):
    decay = False
    if logging:
        print("RankingSys - Initializing...")
        progress = 0
        total = User.objects.all().count()

    for user in User.objects.all():
        try:
            statistics = user.statistics
        except:
            statistics = Statistics.create(user)

        if statistics:
            statistics = user.statistics
            statistics.rank_points = 0
            statistics.rank = 0
            statistics.wins = 0
            statistics.attended = 0
            statistics.total_games = 0
            statistics.total_score = 0
        else:
            statistics = Statistics.create(user)

        for tournament_data in user.tournament_datas.all():
            tournament = tournament_data.tournament
            game_datas = tournament_data.game_datas.all()
            games_count = game_datas.count()

            is_winner = tournament_data.place == 1
            total_score = 0
            for game_data in game_datas:
                total_score += game_data.total

            statistics.wins += 1 if is_winner else 0
            statistics.attended += 1
            statistics.total_games += games_count
            statistics.total_score += total_score

            avg_score = 0
            if games_count > 0:
                avg_score = total_score / games_count
            statistics.rank_points += task_get_rank_points(tournament_data.place, avg_score, tournament.tournament_datas.count(),
                                                           tournament.datetime, decay)
            if tournament.in_season():
                statistics.year_wins += 1 if is_winner else 0
                statistics.year_attended += 1
                statistics.year_total_games += games_count
                statistics.year_total_score += total_score

        statistics.last_calculated = timezone.now()
        statistics.save()
        if logging:
            progress += 1
            print('Calculating Statistics (',progress,'/',total,')')

    statistics = Statistics.objects.order_by('-rank_points')
    rank = 1
    for statistic in statistics:
        statistic.rank = rank
        if logging:
            print('Saving Ranks #', rank,'-',statistic.rank_points)
        rank += 1
        statistic.save()
    if logging:
        print('RankingSys - Finished')






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
                rank_data.rank_points = task_get_rank_points(placement, t_score_average, qualifying_objects_length,tournament.datetime)
                # get avg score year
                rank_data.avg_score_year_total += t_score_average
                rank_data.avg_score_year_amount += 1
                rank_data.avg_score_year = round(rank_data.avg_score_year_total / rank_data.avg_score_year_amount, 2)
                # get best games year
                rank_data.top_five_year = task_best_score(rank_data.top_five_year, placement.scores, tournament.id)
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
            rank_data.top_five_career = task_best_score(rank_data.top_five_career, placement.scores, tournament.id)
            # add tournament to list
            rank_data.tournaments = task_store_tournament(tournament.id, rank_data.tournaments)
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
    decay = False
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
                rank_data.rank_points = task_get_rank_points(placement, placement.average_score, placements_length,tournament.datetime, decay)
                print(str(rank_data.rank_points) + '   :     ' + str(rank_data.user_id))
                # get avg score year
                rank_data.avg_score_year_total += placement.average_score
                rank_data.avg_score_year_amount += 1
                rank_data.avg_score_year = round(rank_data.avg_score_year_total / rank_data.avg_score_year_amount, 2)
                # get best games year
                rank_data.top_five_year = task_best_score(rank_data.top_five_year, placement.high_score, tournament.id)
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
            rank_data.top_five_career = task_best_score(rank_data.top_five_career, placement.high_score, tournament.id)
            # add tournament to list
            rank_data.tournaments = task_store_tournament(tournament.id, rank_data.tournaments)
    return sorted(rank_data_lib, key=lambda x: x.rank_points, reverse=True)

def get_rank_data(rank_datas, user_id):
    for rank_data in rank_datas:
        if rank_data.user_id == user_id:
            return rank_data
    instance = RankData()
    instance.user_id = user_id
    rank_datas.append(instance)
    return instance

def task_get_rank_points(place, avgerage, length, date, decay):
    # calculate points
    place_points = 0
    score_points = 0
    if place != 0:
        place_points = (4000 / place) * (length / 50)
    if avgerage !=  0:
        score_points = (((avgerage / 10) * avgerage) / 10)
    total_points = place_points + score_points

    # apply decay
    if decay:
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