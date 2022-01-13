from django.contrib.auth import get_user_model
from django.core.cache import cache

from ScratchBowling.sbs_utils import make_ordinal
from accounts.models import User
from scoreboard.models import Statistics
from tournaments.models import Tournament


def update_all_cache():
    print('updating all of cache')
    cache.set('top_rankings', top_rankings())
    cache.set('tournament_winners', tournament_winners())
    cache.set('upcoming_tournaments', Tournament.get_upcoming_tournaments(5))
    cache.set('bowler_of_month', User.objects.filter(is_bowler_of_month=True) or User.objects.all().first())
    cache.set('user_count', User.objects.all().count())
    cache.set('tournament_count', Tournament.objects.all().count())
    cache.set('donation_count', 12500)
    cache.set('featured_tournament', Tournament.objects.all().first())
    cache.set('featured_series', Tournament.objects.all()[200:203])
    cache.set('featured_live', Tournament.objects.all().last())
    print('finished updating cache')




def tournament_winners():
    datas = []
    tournament_datas = Tournament.past_winners(10)
    for data in tournament_datas:
        datas.append([
            data.tournament.id,
            data.tournament.name,
            data.tournament.datetime,
            data.user.id,
            data.user.first_name,
            data.user.last_name,
        ])

    ##TEMP PLACEHOLDER
    users = User.objects.all().order_by('last_name')[200:205]
    for x in range(1, 6):
        datas.append([
            1,
            'data.tournament.name',
            '12/1',
            2,
            users[x - 1].first_name,
            users[x - 1].last_name,
        ])
    return datas

def top_rankings():
    datas = []
    statistics = Statistics.get_top(10)
    for stat in statistics:
        datas.append([
            stat.user.id,
            stat.user.first_name,
            stat.user.last_name,
            stat.user.rank_badge,
            stat.user.rank_ordinal,
        ])

    ##TEMP PLACEHOLDER
    users = User.objects.all().order_by('last_name')[200::10]
    for x in range(1, 11):
        datas.append([
            users[x - 1].first_name,
            users[x - 1].first_name,
            users[x - 1].last_name,
            users[x - 1].first_name,
            make_ordinal(x),
        ])
    return datas