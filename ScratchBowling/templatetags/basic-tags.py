import string
import random

from django import template
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.safestring import mark_safe

from ScratchBowling.sbs_utils import make_ordinal
from scoreboard.models import Statistics
from tournaments.models import Tournament

register = template.Library()
User = get_user_model()



@register.simple_tag
def session_id(input):
    return '#' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

@register.simple_tag
def web_version(input):
    return ''

@register.filter()
def badge(badge):
    diamond_icon = 'shield2'
    diamond_color = '#8AD2E2'
    gold_icon = 'shield2'
    gold_color = '#f5d442'
    silver_icon = 'shield2'
    silver_color = '#c2c2c2'
    bronze_icon = 'shield2'
    bronze_color = '#d7995b'
    icon = ''
    color = ''
    if badge == 1:
        icon = diamond_icon
        color = diamond_color
    elif badge == 2:
        icon = gold_icon
        color = gold_color
    elif badge == 3:
        icon = silver_icon
        color = silver_color
    elif badge == 4:
        icon = bronze_icon
        color = bronze_color

    output_str = '<i class="icon-' + icon + ' rank-color" style="color:' + color + ';"></i>'

    return mark_safe(output_str)

@register.filter()
def space_before(value):
    if value:
        try:
            return ' ' + str(value)
        except:
            return ''
    return ''

@register.inclusion_tag('snippets/basic/recentWinners.html')
def basic_recent_winners():
    # [0]tournament id
    # [1]tournament name
    # [2]tournament date
    # [3]winner id
    # [4]winner first_name
    # [5]winner last_name

    return {'datas': cache.get('tournament_winners')}


@register.inclusion_tag('snippets/basic/topRankings.html')
def basic_top_ranks():
    # [0]winner id
    # [1]winner first_name
    # [2]winner last_name
    # [3]rank badge
    # [4]user rank

    return {'datas': cache.get('top_rankings')}


@register.inclusion_tag('snippets/basic/bowlerOfMonth.html')
def basic_bowler_of_month():
    return {'bom': cache.get('bowler_of_month')}


@register.inclusion_tag('snippets/basic/upcomingTournaments.html')
def basic_upcoming_tournaments():
    return {'tournaments': cache.get('upcoming_tournaments')}


@register.inclusion_tag('snippets/basic/topNotify.html')
def basic_top_notify(request):
    return {'user': request.user, 'notify': request.GET.get('notify', None)}

@register.inclusion_tag('snippets/basic/streamHighlights.html')
def basic_stream_highlights():
    return {'visible': True}

@register.inclusion_tag('snippets/basic/appInfo.html')
def basic_app_info():
    return {'visible': True}

@register.inclusion_tag('snippets/basic/goalSupport.html')
def basic_goal_support():
    return {'donation_count': cache.get('donation_count')}

@register.inclusion_tag('snippets/basic/featuredTournament.html')
def basic_featured_tournament():
    return {'tournament': cache.get('featured_tournament')}

@register.inclusion_tag('snippets/basic/featuredSeries.html')
def basic_featured_series():
    return {'tournaments': cache.get('featured_series')}

@register.inclusion_tag('snippets/basic/featuredLive.html')
def basic_featured_live():
    return {'tournament': cache.get('featured_live')}

@register.inclusion_tag('snippets/basic/playSteps.html')
def basic_play_steps():
    return {'visible': True}

@register.inclusion_tag('snippets/basic/siteStat.html')
def basic_site_stats():
    return {'sitestats': [
        {'title': 'Active Users', 'count': cache.get('user_count')},
        {'title': 'Tournaments', 'count': cache.get('tournament_count')}
    ]}
