import uuid
from django.db import models


class Center(models.Model):
    center_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    center_name = models.TextField()
    center_description = models.TextField()
    location_street = models.TextField()
    location_city = models.TextField()
    location_state = models.TextField()
    location_zip = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)
    oil_machine = models.TextField(default='')
    tournaments = models.JSONField(default='')