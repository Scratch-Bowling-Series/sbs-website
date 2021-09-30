import uuid

from django.db import models

# Create your models here.


class Vod(models.Model):
    vod_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    video = models.FileField(default='vods/default.mp4', upload_to='vods/')
    poster = models.ImageField(default='vod-posters/default.jpg', upload_to='vod-posters/')
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)