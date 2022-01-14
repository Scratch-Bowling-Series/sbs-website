import random
import string

from django.contrib.auth import get_user_model
from django.core.cache import cache

from ScratchBowling.sbs_utils import make_ordinal
from accounts.models import User
from scoreboard.models import Statistics
from tournaments.models import Tournament


def update_all_cache():
    print('updating all of cache')
    cache.set('cache_id', '#' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
    cache.set('top_rankings', top_rankings())
    cache.set('tournament_winners', tournament_winners())
    cache.set('upcoming_tournaments', Tournament.get_upcoming(5))
    cache.set('bowler_of_month', User.ss_bowler_of_month())
    cache.set('user_count', User.objects.all().count())
    cache.set('tournament_count', Tournament.objects.all().count())
    cache.set('donation_count', 12500)
    cache.set('featured_tournament', Tournament.featured_tournament_data())
    cache.set('featured_series', Tournament.objects.all()[200:203])
    cache.set('featured_live', Tournament.objects.all().last())
    print('finished updating cache')





def tournament_winners():
    datas = []
    tournament_datas = Tournament.past_winners(10)
    for data in tournament_datas:
        datas.append({
            'tournament_id':data.tournament.id,
            'tournament_name': data.tournament.name,
            'date': data.tournament.datetime,
            'user_id': data.user.id,
            'name': data.user.full_name
        })
    return datas

def top_rankings():
    datas = []
    statistics = Statistics.get_top(10)
    for stat in statistics:
        datas.append(user_to_rank_display(stat.user))
    return datas

def user_to_rank_display(user):
    return {
        'id':user.id,
        'rank':user.rank_ordinal,
        'name':user.full_name,
    }
