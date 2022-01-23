from django.core.management.base import BaseCommand, CommandError

from scoreboard.ranking import calculate_statistics


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        calculate_statistics(True)