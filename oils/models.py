import uuid

from django.db import models

# Create your models here.

class Oil_Pattern(models.Model):
    pattern_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    pattern_name = models.TextField()
    pattern_cache = models.JSONField()
    pattern_db_id = models.IntegerField()
    @classmethod
    def create(cls, pattern_db_id):
        tournament = cls(pattern_db_id=pattern_db_id)
        return tournament