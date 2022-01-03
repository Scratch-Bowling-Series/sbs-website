import time

from django.core.management.base import BaseCommand, CommandError

from accounts.models import Notification


class Command(BaseCommand):
    help = 'Run Notifications'

    def handle(self, *args, **options):
        while True:
            Notification.perform_sends()
            time.sleep(2)