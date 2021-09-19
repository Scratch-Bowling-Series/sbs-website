from django.core.management.base import BaseCommand, CommandError

from centers.models import Center
from scoreboard.ranking import convert_tournaments


class Command(BaseCommand):
    help = 'Run Statistics'

    def handle(self, *args, **options):
        length = Center.objects.all().count()
        print(str(length))