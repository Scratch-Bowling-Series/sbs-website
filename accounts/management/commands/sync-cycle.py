from django.core.management.base import BaseCommand, CommandError

from ScratchBowling.update_cache import update_all_cache


class Command(BaseCommand):
    help = 'Run Master Sync Cycle'
    def handle(self, *args, **options):
       update_all_cache()