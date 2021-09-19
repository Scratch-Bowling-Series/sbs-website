import uuid

from django.db import models


class Tournament(models.Model):
    tournament_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tournament_name = models.CharField(max_length=100)
    tournament_description = models.TextField(blank=True, null=True)
    tournament_date = models.DateField(blank=True, null=True)
    tournament_time = models.TimeField(blank=True, null=True)
    picture = models.ImageField(blank=True)
    center = models.UUIDField(editable=True, unique=True, blank=True, null=True)
    format = models.UUIDField(editable=True, unique=True, blank=True, null=True)
    entry_fee = models.FloatField(blank=True, null=True)
    total_games = models.IntegerField(null=False, blank=True, default=0)
    qualifiers = models.JSONField(blank=True, null=True)
    matchplay = models.JSONField(blank=True, null=True)
    sponsor_image = models.ImageField(blank=True)

    tournament_data = models.BinaryField(blank=True, null=True)
    placement_data = models.BinaryField(blank=True, null=True)

    @classmethod
    def create(cls, name):
        tournament = cls(tournament_name=name)
        return tournament