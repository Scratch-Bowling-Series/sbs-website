import uuid
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.db import models
from ScratchBowling.sbs_utils import is_valid_uuid
from centers.scraping.soup_parser import update_center_with_soup


class Center(models.Model):
    center_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField(max_length=200)
    center_description = models.TextField()
    location_street = models.TextField()
    location_city = models.TextField()
    location_state = models.TextField()
    location_zip = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)
    oil_machine = models.TextField(default='')
    picture = models.ImageField(default='center-pictures/default.jpg', upload_to='center-pictures/')


    # <editor-fold desc="SCRAPING">
    scraped = models.BooleanField(default=False)
    soup_url = models.TextField(default='')
    soup = models.TextField(default='')
    @classmethod
    def update_all(cls, logging=False):
        base_url = 'https://scratchbowling.com'
        page = 0
        soup_urls = []
        while True:
            with urlopen( base_url + '/bowling-centers?page=' + str(page)) as response:
                if logging:
                    print('Scanning Page ' + str(page))
                soup = BeautifulSoup(response, 'lxml')
                data = soup.find_all(class_="views-row")
                if data:
                    for node in data:
                        title = node.find(class_="node__title")
                        if title:
                            tag = title.find('a')
                            if tag:
                                url = tag.get('href')
                                if url and '/bowling-center/' in url:
                                    soup_urls.append(base_url + str(url))
                    page += 1
                else:
                    break
        if logging:
            print('Found ' + str(len(soup_urls)) + ' soup urls.')

        centers = []
        for soup_url in soup_urls:
            center = cls.objects.filter(soup_url=soup_url).first()
            if not center:
                center = cls(soup_url=soup_url, scraped=True)
            if center.make_soup() and center.eat_soup():
                centers.append(center)

        if logging:
            print('Saving ' + str(len(centers)) + ' Centers')

        for center in centers:
            center.save()

        if logging:
            print('Update All Complete')
    def make_soup(self):
        if self.soup_url:
            with urlopen(self.soup_url) as response:
                soup = BeautifulSoup(response, 'lxml')
                if soup:
                    body = soup.find('body')
                    if body:
                        self.soup = str(body)
                        return True
        return False
    def eat_soup(self):
        if self.soup:
            soup = BeautifulSoup(self.soup, 'html.parser')
            return update_center_with_soup(self, soup)
        return False
    # </editor-fold>


    @classmethod
    def find_center_by_name(cls, name):
        return cls.objects.filter(name=name).first()
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
            return [center.name, center.location_city, center.location_state]




    @property
    def short_location(self):
        if self.location_city and self.location_state:
            return self.location_city + ', ' + self.location_state
        return 'Location Unknown'


    # CENTER PICTURE
    def get_picture(self):
        return'/media/' + str(self.picture)
    def has_default_picture(self):
        if self.picture == 'center-pictures/default.jpg':
            return True
        return False
