from django.db import models

# Create your models here.
class Homepage_Cache(models.Model):
    cache_id = models.IntegerField(primary_key=True, default=0)
    tournament_winners = models.BinaryField(blank=True, null=True)
    top_ten_rankings = models.BinaryField(blank=True, null=True)
    recent_tournament = models.BinaryField(blank=True, null=True)
    bowler_of_month = models.BinaryField(blank=True, null=True)