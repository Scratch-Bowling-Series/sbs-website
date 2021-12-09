import base64
import io
import os
import uuid
from datetime import datetime
from time import strptime

import requests
import PIL.Image
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.core.files import File
from django.utils import timezone

from ScratchBowling import settings
from ScratchBowling.sbs_utils import is_valid_uuid
import quickle

class Tournament(models.Model):
    tournament_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tournament_name = models.CharField(max_length=100)
    tournament_description = models.TextField(blank=True, null=True)
    tournament_date = models.DateField(blank=True, null=True)
    tournament_time = models.TimeField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(default='tournament-pictures/default.jpg', upload_to='tournament-pictures/')
    picture_scrape = models.TextField(default='')
    center = models.UUIDField(editable=True, blank=True, null=True)
    format = models.UUIDField(editable=True, unique=True, blank=True, null=True)
    entry_fee = models.FloatField(blank=True, null=True)
    total_games = models.IntegerField(null=False, blank=True, default=0)
    qualifiers = models.JSONField(blank=True, null=True)
    matchplay = models.JSONField(blank=True, null=True)
    sponsor =  models.UUIDField(editable=True, unique=False, null=True, blank=True)
    finished = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    double = models.BooleanField(default=False)
    stream_available = models.BooleanField(default=False)
    vod_id = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    soup = models.TextField(default='')
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

    @classmethod
    def get_tournament_by_uuid(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            return cls.objects.filter(tournament_id=uuid).first()

    @classmethod
    def get_upcoming_tournaments(cls, amount=10, offset=0):
        return cls.objects.all().exclude(finished=True).exclude(live=True)[offset:offset+amount]


    # TOURNAMENT GET SPONSOR INFO
    def get_sponsor_image(self):
        return Sponsor.get_sponsor_image_uuid(self.sponsor)

    # TOURNAMENT HEADER PICTURE
    def get_picture(self):
        if self.has_default_picture():
            try:
                return '/media/' + str(self.download_scraped_image())
            except:
                return '/media/' + str(self.picture)
        else:
            return'/media/' + str(self.picture)
    def has_default_picture(self):
        if self.picture == 'tournament-pictures/default.jpg':
            return True
        return False
    def download_scraped_image(self, remove_bkg=True):
        response = requests.get('https://scratchbowling.com' + self.picture_scrape)
        original = Image.open(io.BytesIO(response.content))
        if original:
            print('opened')

            ## remove bkg from original
            if remove_bkg:
                api_key = '1ec8d33f744b07af2de3ebd0e11e21996f3b2841'
                url = 'https://sdk.photoroom.com/v1/segment'
                files = {'image_file': io.BytesIO(response.content)}
                headers = {'x-api-key': api_key}
                response = requests.post(url, files=files, headers=headers)
                response.raise_for_status()
                modified = Image.open(io.BytesIO(response.content))
            else:
                modified = original

            master = Image.new(modified.mode, modified.size)
            width, height = modified.size



            ## get bkg, resize it, and paste to master
            background = Image.open(os.path.join(settings.MEDIA_ROOT, 'tournament-pictures/background.png'))
            if height > width: resize = height
            else: resize = width
            background.thumbnail((resize, resize))
            bkg_width, bkg_height = background.size
            bkg_x = int((width - bkg_width) / 2)
            bkg_y = int((height - bkg_height) / 2)
            print('bkg_width: ' + str(bkg_width) + ' bkg_height: ' + str(bkg_height) + ' bkg_x: ' + str(bkg_x) + ' bkg_y: ' + str(bkg_y))
            master.paste(background, (bkg_x, bkg_y), background)


            master.paste(modified, (0,0), modified)
            path = 'tournament-pictures/' + str(self.tournament_id)
            xpath = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(xpath):
                os.makedirs(xpath)
            master.save(xpath + '/primary.png')
            self.picture = path + '/primary.png'
            self.save()
            return self.picture

    # ROSTER
    def get_roster(self):
        if self.roster:
            return quickle.loads(self.roster)
        return []
    def set_roster(self, roster):
        if roster:
            self.roster = quickle.dumps(roster)
        else:
            self.roster = quickle.dumps([])
        self.save()
    def get_roster_length(self):
        if self.roster:
            roster = quickle.loads(self.roster)
            if roster:
                return len(roster)
        return 0
    def get_spots_available(self):
        return self.spots_reserved - self.get_roster_length()
    def add_to_roster(self, uuid):
        uuid = is_valid_uuid(uuid)
        roster = self.get_roster()
        if uuid and roster != None and not self.exists_in_roster(uuid, roster):
            roster.append(str(uuid))
            self.set_roster(roster)
            return True
        return False
    def remove_from_roster(self, uuid):
        uuid = is_valid_uuid(uuid)
        roster = self.get_roster()
        if uuid and roster != None:
            on_roster = self.exists_in_roster(uuid, roster)
            if on_roster:
                roster.remove(str(uuid))
                self.set_roster(roster)
                return True
        return False
    def exists_in_roster(self, uuid, roster=None):
        uuid = is_valid_uuid(uuid)
        exists = False
        if uuid:
            uuid = str(uuid)
            if roster:
                for id in roster:
                    if str(id) == uuid:
                        exists = True
                        break
            else:
                roster = self.get_roster()
                for id in roster:
                    if str(id) == uuid:
                        exists = True
                        break
        return exists




    # TAGS
    def get_tags(self):
        tags = []
        if 'Double' in self.tournament_name or 'double' in self.tournament_name:
            tags.append(1)
        if 'Sweep' in self.tournament_name or 'sweep' in self.tournament_name:
            tags.append(2)
        if 'Open' in self.tournament_name or 'open' in self.tournament_name:
            tags.append(3)
        if 'Challenge' in self.tournament_name or 'challenge' in self.tournament_name:
            tags.append(4)
        if 'Sprummer' in self.tournament_name or 'sprummer' in self.tournament_name:
            tags.append(5)
        return tags








class Sponsor(models.Model):
    sponsor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sponsor_name =  models.CharField(max_length=60, blank=True, null=True)
    sponsor_display_name = models.CharField(max_length=60, blank=True, null=True)
    sponsor_balance = models.IntegerField(default=0, null=False, blank=True)
    sponsor_image = models.ImageField(default='sponsor-pictures/default.png', upload_to='sponsor-pictures/')

    @classmethod
    def get_sponsor(cls, uuid):
        if is_valid_uuid(uuid):
            return cls.objects.filter(sponsor_id=uuid).first()
        return None

    @classmethod
    def get_sponsor_image_uuid(cls, uuid):
        sponsor = cls.get_sponsor(uuid)
        if sponsor:
            return sponsor.get_sponsor_image()
        else:
            return '/media/sponsor-pictures/default.png'

    def get_sponsor_image(self):
        if self.sponsor_image:
            return '/media/' + self.sponsor_image.path
        else:
            return '/media/sponsor-pictures/default.png'