import uuid
from django.db import models

from ScratchBowling.sbs_utils import is_valid_uuid


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
    picture = models.ImageField(default='center-pictures/default.jpg', upload_to='center-pictures/')

    @classmethod
    def find_center_by_name(cls, name):
        return cls.objects.filter(center_name=name).first()

    @classmethod
    def get_center_by_uuid(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            return cls.objects.filter(center_id=uuid).first()
        return None

    @classmethod
    def get_name_and_location_by_uuid(cls, uuid):
        center = cls.get_center_by_uuid(uuid)
        if center:
            return [center.center_name, center.location_city, center.location_state]


    # CENTER PICTURE
    def get_picture(self):
        return'/media/' + str(self.picture)
    def has_default_picture(self):
        if self.picture == 'center-pictures/default.jpg':
            return True
        return False
