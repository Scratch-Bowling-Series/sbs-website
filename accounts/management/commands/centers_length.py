from django.core.management.base import BaseCommand, CommandError

from ScratchBowling.sbs_utils import is_valid_uuid
from ScratchBowling.views import User
from centers.center_utils import get_center
from centers.models import Center
from scoreboard.ranking import convert_tournaments
from scraper import convert_to_new_scrape_cache
from tournaments.models import Tournament


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        return None