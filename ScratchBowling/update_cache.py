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
    cache.set('tournament_winners', Tournament.ss_recent_winners())
    cache.set('upcoming_tournaments', Tournament.get_upcoming(5))
    cache.set('bowler_of_month', User.ss_bowler_of_month())
    cache.set('user_count', User.objects.all().count())
    cache.set('tournament_count', Tournament.objects.all().count())
    cache.set('donation_count', 12500)
    cache.set('featured_tournament', Tournament.ss_featured_tournament())
    cache.set('featured_series', Tournament.featured_series())
    cache.set('featured_live', Tournament.objects.all().last())
    print('finished updating cache')
    user = User.objects.filter(last_name__icontains='Snodgrass').first()
    user.is_bowler_of_month = True
    print(user.first_name)
    user.save()


def top_rankings():
    datas = []
    statistics = Statistics.get_top(10)
    for stat in statistics:
        datas.append({
        'id': stat.user.id,
        'rank': stat.rank_ordinal,
        'name':stat.user.full_name,
    })
    return datas

