from django.core.management.base import BaseCommand, CommandError

from scraper import run_sync_cycle


class Command(BaseCommand):
    help = 'Run Master Sync Cycle'

    def handle(self, *args, **options):
        run_sync_cycle()