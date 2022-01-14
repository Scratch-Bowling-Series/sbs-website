from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from centers.models import Center
from tournaments.models import Tournament

User = get_user_model()

class Command(BaseCommand):
    help = 'Run Master Scraper'

    def handle(self, *args, **options):
        logging = args[0]
        User.update_all(logging)
        Center.update_all(logging)
        Tournament.update_all(logging)
        #Tournament.only_eat_all(logging)
        Tournament.populate_datas(logging)

