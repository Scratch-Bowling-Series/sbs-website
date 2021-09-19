from django.core.management.base import BaseCommand, CommandError

from ScratchBowling.sbs_utils import is_valid_uuid
from centers.center_utils import get_center
from centers.models import Center
from scoreboard.ranking import convert_tournaments
from tournaments.models import Tournament


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            center_id = is_valid_uuid(tournament.center)
            center = get_center(center_id)
            if center != None:
                print(str(center_id) + ' : ' + str(center.center_name))
                break