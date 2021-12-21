from rest_framework import serializers

from tournaments.models import Tournament


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ['tournament_id', 'name']