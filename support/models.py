import uuid

from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='donations')
    amount = models.IntegerField(default=0)
    datetime = models.DateField(default=timezone.now, editable=False)


    @classmethod
    def get_total(cls):
        total = cls.objects.aggregate(total_amount=Sum('amount'))
        if 'total_amount' in total:
            return total['total_amount']
        return 0
