from django.core.management.base import BaseCommand, CommandError

from scraper import master_scrape


class Command(BaseCommand):
    help = 'Run Master Scraper'

    def handle(self, *args, **options):
        master_scrape(True)