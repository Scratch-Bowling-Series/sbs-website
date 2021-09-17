from django.core.management.base import BaseCommand, CommandError

from tournaments.transfer import TransferT


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        TransferT()