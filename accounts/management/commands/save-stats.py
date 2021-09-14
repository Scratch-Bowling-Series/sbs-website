from django.core.management.base import BaseCommand, CommandError

from scoreboard.ranking import save_statistics


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        save_statistics()