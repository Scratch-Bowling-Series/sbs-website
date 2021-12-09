import uuid
from django.utils.timezone import now
from django.db import models

# Create your models here.

class Stream(models.Model):
    stream_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tournament_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    vod_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    stream_source = models.TextField(default='')
    stream_mirror = models.TextField(default='')
    thumbnail_image = models.ImageField(default='broadcast-thumbnails/streams/default.jpg', upload_to='broadcast-thumbnails/streams/')
    title = models.TextField(default='Default Stream Title')
    description = models.TextField(default='Default Stream Description')
    datetime = models.DateTimeField(default=now, editable=False)
    uptime = models.IntegerField(default=0)

class FullVod(models.Model):
    vod_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    stream_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    vod_source = models.TextField(default='')
    vod_mirror = models.TextField(default='')
    thumbnail_image = models.ImageField(default='broadcast-thumbnails/vods/default.jpg', upload_to='broadcast-thumbnails/vods/')
    title = models.TextField(default='Default Vod Title')
    description = models.TextField(default='Default Vod Description')
    datetime = models.DateTimeField(default=now, editable=False)
    duration = models.IntegerField(default=0)

class Clip(models.Model):
    clip_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    vod_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    clip_source = models.TextField(default='')
    thumbnail_image = models.ImageField(default='broadcast-thumbnails/clips/default.jpg', upload_to='broadcast-thumbnails/clips/')
    title = models.TextField(default='Default Clip Title')
    description = models.TextField(default='Default Clip Description')
    datetime = models.DateTimeField(default=now, editable=False)
    duration = models.IntegerField(default=0)


    @classmethod
    def get_most_recent(cls, amount):
        if amount:
            return cls.objects.all().order_by('datetime')[:amount]
        return None
