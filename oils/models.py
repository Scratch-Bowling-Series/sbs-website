import uuid

from django.db import models

# Create your models here.

class Oil_Pattern(models.Model):
    pattern_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    pattern_name = models.TextField(default=0)
    pattern_cache = models.BinaryField(blank=True, null=True)
    pattern_db_id = models.IntegerField(default=0)
    pattern_length = models.IntegerField(default=0)
    pattern_volume = models.FloatField(default=0)
    pattern_forward = models.FloatField(default=0)
    pattern_backward = models.FloatField(default=0)
    pattern_ratio = models.TextField(default='')

    @classmethod
    def create(cls, pattern_db_id):
        tournament = cls(pattern_db_id=pattern_db_id)
        return tournament