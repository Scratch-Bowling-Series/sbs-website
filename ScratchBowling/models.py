import uuid

from django.db import models


class WebData(models.Model):
    preview_tournament = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    bowler_of_month = models.UUIDField(editable=True, unique=False, null=True, blank=True)


    @classmethod
    def get_current(cls):
        web_data = cls.objects.all().first()
        if web_data:
            return web_data
        return WebData()

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




