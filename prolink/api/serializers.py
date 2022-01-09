from django.contrib.auth import get_user_model
from rest_framework import serializers

from prolink.models import Drawer, Transaction

User = get_user_model()


class UserIdSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = User
        fields = ['id']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    user = UserIdSerializer()
    drawer = serializers.UUIDField()
    class Meta:
        model = Transaction
        fields = ['id', 'datetime', 'amount', 'user', 'drawer']

class UserDrawerSerializer(serializers.HyperlinkedModelSerializer):
    recent_transactions = TransactionSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'balance', 'pending_balance', 'picture', 'recent_transactions', 'city', 'state']

class DrawerSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserIdSerializer()
    recent_transactions = TransactionSerializer(many=True)
    class Meta:
        model = Drawer
        fields = ['id', 'opened_datetime', 'closed_datetime', 'amount', 'owner', 'opened', 'recent_transactions']


