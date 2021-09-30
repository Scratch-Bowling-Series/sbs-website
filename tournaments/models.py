import uuid

from django.db import models


class Tournament(models.Model):
    tournament_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tournament_name = models.CharField(max_length=100)
    tournament_description = models.TextField(blank=True, null=True)
    tournament_date = models.DateField(blank=True, null=True)
    tournament_time = models.TimeField(blank=True, null=True)
    picture = models.ImageField(default='tournament-pictures/default.jpg', upload_to='tournament-pictures/')
    center = models.UUIDField(editable=True, blank=True, null=True)
    format = models.UUIDField(editable=True, unique=True, blank=True, null=True)
    entry_fee = models.FloatField(blank=True, null=True)
    total_games = models.IntegerField(null=False, blank=True, default=0)
    qualifiers = models.JSONField(blank=True, null=True)
    matchplay = models.JSONField(blank=True, null=True)
    sponsor =  models.UUIDField(editable=True, unique=False, null=True, blank=True)
    finished = models.BooleanField(default=False)
    live = models.BooleanField(default=False)

    stream_available = models.BooleanField(default=False)
    vod_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)


    tournament_data = models.BinaryField(blank=True, null=True)
    placement_data = models.BinaryField(blank=True, null=True)
    roster = models.BinaryField(blank=True, null=True)
    spots_reserved = models.IntegerField(null=False, blank=True, default=0)
    oil_pattern = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    live_status_header = models.TextField(blank=True, null=True)
    live_status_leader = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    live_status_leader_score = models.FloatField(default=0, blank=True)
    @classmethod
    def create(cls, name):
        tournament = cls(tournament_name=name)
        return tournament


class Sponsor(models.Model):
    sponsor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sponsor_name =  models.CharField(max_length=60, blank=True, null=True)
    sponsor_display_name = models.CharField(max_length=60, blank=True, null=True)
    sponsor_balance = models.IntegerField(default=0, null=False, blank=True)
    sponsor_image = models.ImageField(default='sponsor-pictures/default.jpg', upload_to='sponsor-pictures/')