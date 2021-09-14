from django.core.management.base import BaseCommand, CommandError

from scoreboard.ranking import run_statistics
from scraper import master_scrape


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        run_statistics()