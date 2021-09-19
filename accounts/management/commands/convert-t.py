from django.core.management.base import BaseCommand, CommandError

from scoreboard.ranking import convert_tournaments


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        convert_tournaments()