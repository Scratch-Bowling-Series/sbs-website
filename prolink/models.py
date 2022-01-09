import uuid

from django.contrib.auth import get_user_model
from django.db import models, transaction

# Create your models here.
from django.utils import timezone

User = get_user_model()



class Drawer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    opened_datetime = models.DateField(default=timezone.now, editable=False)
    closed_datetime = models.DateField(default=timezone.now, editable=False)
    amount = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='drawers')
    opened = models.BooleanField(default=True)

    @classmethod
    def create(cls, owner):
        drawer = cls(owner=owner)
        drawer.save()
        return drawer

    @classmethod
    def get_open_drawer(cls, user):
        return user.drawers.filter(opened=True).first()

    @classmethod
    def make_transaction(cls, drawer_owner, user, amount):
        drawer = drawer_owner.drawers.filter(opened=True).first()
        if not drawer:
            drawer = cls.create(drawer_owner)
        return Transaction.create(user, amount, drawer)

    @property
    def recent_transactions(self):
        return self.transactions.all().order_by('-datetime')[:10]


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    datetime = models.DateTimeField(default=timezone.now, editable=False)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='transactions')
    drawer = models.ForeignKey(Drawer, on_delete=models.CASCADE, blank=True, related_name='transactions')

    @classmethod
    def get_last_transactions(cls, count):
        return cls.objects.all().order_by('datetime')[:count]

    @classmethod
    @transaction.atomic
    def create(cls, user, amount, drawer=None):
        amount = try_int(amount)

        if user and user.balance + amount >= 0:
            user.balance = user.balance + amount
            if drawer:
                transaction = cls(user=user, amount=amount, drawer=drawer)
                drawer.amount -= amount
            else:
                transaction = cls(user=user, amount=amount)
            transaction.save()
            drawer.save()
            user.save()
            return transaction
        return None


def try_int(value):
    try:
        return int(value)
    except ValueError:
        return 0