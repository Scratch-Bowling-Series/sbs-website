from django.core.management.base import BaseCommand, CommandError

from tournaments.models import Tournament
from tournaments.transfer import TransferT, Gather


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        print(str(Tournament.objects.all().count()))