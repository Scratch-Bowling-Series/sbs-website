
from django.contrib.auth import get_user_model
from centers.models import Center
from tournaments.models import Tournament

User = get_user_model()

def run_sync_cycle():
    Center.update_all()
    User.update_all()
    Tournament.update_all()

def master_scrape(logging=False):
    Tournament.only_eat_all(logging)

    #Center.objects.all().delete()
    #Center.update_all(logging)

    #User.objects.all().delete()
    #User.update_all(logging)

    #Tournament.objects.all().delete()
    #Tournament.update_all(logging)