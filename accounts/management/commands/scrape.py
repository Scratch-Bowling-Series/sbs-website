from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from centers.models import Center
from oils.models import Oil_Pattern
from oils.oil_pattern_scraper import update_library
from tournaments.models import Tournament

User = get_user_model()

class Command(BaseCommand):
    help = 'Run Master Scraper'

    def handle(self, *args, **options):
        #User.update_all(True)
        Center.update_all(True)
        #Tournament.update_all(True)
        #Tournament.only_eat_all(True)
        #Tournament.populate_datas(True)
        #update_library()
        #print(Oil_Pattern.objects.all().count())