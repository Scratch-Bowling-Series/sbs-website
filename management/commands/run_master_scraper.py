from django.core.management.base import BaseCommand, CommandError

from scraper import master_scrape


class Command(BaseCommand):
    help = 'Run Master Scraper'

    def add_arguments(self, parser):
        parser.add_argument('update', nargs='+', type=bool)

    def handle(self, *args, **options):
        update = options['update']
        master_scrape(update)