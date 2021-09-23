import uuid

from django.db import models

class Series(models.Model):
    series_id = models.CharField(max_length=30)
    series_name = models.TextField()
    series_description = models.TextField()
    use_decay = models.BooleanField()
    count_placement = models.BooleanField()
    count_score = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tournaments = models.JSONField()


class Medal(models.Model):
    medal_id = models.CharField(max_length=30)
    medal_name = models.TextField()
    medal_description = models.TextField()
    icon = models.URLField()


class SeasonRanking(models.Model):
    season_id = models.CharField(max_length=30)
    total_games = models.IntegerField()
    total_bowlers = models.IntegerField()
    tournaments = models.JSONField()
    bowlers = models.JSONField()


class SeriesRanking(models.Model):
    series_id = models.CharField(max_length=30)
    total_games = models.IntegerField()
    total_bowlers = models.IntegerField()
    tournaments = models.JSONField()
    bowlers = models.JSONField()




class Sponsor(models.Model):
    sponsor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sponsor_name =  models.CharField(max_length=60, blank=True, null=True)
    sponsor_display_name = models.CharField(max_length=60, blank=True, null=True)
    sponsor_balance = models.IntegerField(default=0, null=False, blank=True)
    sponsor_image = models.ImageField(default='sponsor-pictures/default.jpg', upload_to='sponsor-pictures/')