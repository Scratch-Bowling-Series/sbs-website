import datetime
import uuid
from urllib.request import urlopen

import quickle
from bs4 import BeautifulSoup
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.functional import classproperty

from ScratchBowling.models import WebData
from ScratchBowling.sbs_utils import is_valid_uuid
from accounts.scraping.soup_parser import update_user_with_soup
from scoreboard.models import Statistics


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name='', last_name=''):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            id=uuid.uuid4(),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True, null=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_joined = models.DateField(default=datetime.date.today, editable=False)

    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(default='profile-pictures/default.jpg', upload_to='profile-pictures/')
    street = models.CharField(blank=True, null=True, max_length=150)
    city = models.CharField(blank=True, null=True, max_length=150)
    state = models.CharField(blank=True, null=True, max_length=150)
    zip = models.IntegerField(default=0, null=False, blank=True)
    handed = models.SmallIntegerField(default=0)
    medals = models.JSONField(blank=True, null=True)

    data_tournaments = models.BinaryField(blank=True, null=True)
    data_friends = models.BinaryField(blank=True, null=True)
    data_blocked = models.BinaryField(blank=True, null=True)

    is_bowler_of_month = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    finish_profile = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    ask_for_claim = models.BooleanField(default=True)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    # <editor-fold desc="SCRAPING">
    scraped = models.BooleanField(default=False)
    unclaimed = models.BooleanField(default=False)
    soup_url = models.TextField(default='')
    soup = models.TextField(default='')
    @classmethod
    def update_all(cls, logging=False):
        base_url = 'https://scratchbowling.com'
        soup_urls = []

        # GET ALL ACCOUNT URLS
        page = 0
        while True:
            with urlopen('http://www.scratchbowling.com/bowler-bios?page=' + str(page)) as response:
                if logging:
                    print('Scanning Page ' + str(page))
                soup = BeautifulSoup(response, 'lxml')
                titles = soup.find_all(class_='views-field views-field-title')
                if titles:
                    for title in titles:
                        tag = title.find('a')
                        if tag:
                            url = tag.get('href')
                            if url and '/bowler/' in url:
                                soup_urls.append(base_url + url)
                    page += 1
                else:
                    break

        if logging:
            print('Found ' + str(len(soup_urls)) + ' soup urls.')

        users = []
        for soup_url in soup_urls:
            user = cls.objects.filter(soup_url=soup_url).first()
            if user:
                continue
            user = cls(soup_url=soup_url, scraped=True, unclaimed=True)
            if user.make_soup() and user.eat_soup():
                users.append(user)

        if logging:
            print('Saving ' + str(len(users)) + ' Users')

        # SAVE ACCOUNTS
        cls.objects.bulk_create(users, 500)

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
            return update_user_with_soup(self, soup)
        return False
    # </editor-fold>


    ## GET USER ##
    @classmethod
    def get_user_by_uuid(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            return cls.objects.filter(id=uuid).first()
    @classmethod
    def get_user_by_email(cls, email):
        if email:
            return cls.objects.filter(email=email).first()

    ## PICTURE ##
    @property
    def full_picture_url(self):
        if self.picture:
            return '/media/' + str(self.picture)
        return '/media/profile-pictures/default.jpg'

    ## STATISTICS ##
    @property
    def statistics(self):
        data = Statistics.get_user_statistics(self.id)
        if not data:
            data = Statistics.create(self.id)
        return data
    @property
    def rank_badge(self):
        statistics = self.statistics
        if statistics:
            return statistics.rank_badge
    @property
    def rank_badge_html(self):
        rank_badge = self.rank_badge
        diamond_icon = 'shield2'
        diamond_color = '#8AD2E2'
        gold_icon = 'shield2'
        gold_color = '#f5d442'
        silver_icon = 'shield2'
        silver_color = '#c2c2c2'
        bronze_icon = 'shield2'
        bronze_color = '#d7995b'
        icon = ''
        color = ''
        if rank_badge == 1:
            icon = diamond_icon
            color = diamond_color
        elif rank_badge == 2:
            icon = gold_icon
            color = gold_color
        elif rank_badge == 3:
            icon = silver_icon
            color = silver_color
        elif rank_badge == 4:
            icon = bronze_icon
            color = bronze_color
        return '<i class="icon-' + icon + ' rank-color" style="color:' + color + ';"></i>'
    @property
    def rank(self):
        statistics = self.statistics
        if statistics:
            return statistics.rank
        return 0
    @property
    def rank_ordinal(self):
        statistics = self.statistics
        if statistics:
            return statistics.rank_ordinal
        return 0

    ## TOURNAMENTS ##
    @property
    def tournaments(self):
        if self.data_tournaments:
            return quickle.loads(self.data_tournaments)
        return []
    @tournaments.setter
    def tournaments(self, data):
        if data:
            self.data_tournaments = quickle.dumps(data)
    def has_attended_tournament(self, tournament_id):
        tournament_id = is_valid_uuid(tournament_id)
        if tournament_id:
            tournaments = self.tournaments
            if tournament_id in tournaments:
                return True
        return False
    def add_tournament(self, tournament_id):
        tournament_id = is_valid_uuid(tournament_id)
        if tournament_id:
            tournaments = self.tournaments
            if tournament_id not in tournaments:
                tournaments.append(tournament_id)
                self.tournaments = tournaments
    def remove_tournament(self, tournament_id):
        tournament_id = is_valid_uuid(tournament_id)
        if tournament_id:
            tournaments = self.tournaments
            if tournament_id in tournaments:
                tournaments.remove(tournament_id)
                self.tournaments = tournaments
    def data_tournaments_list(self):
        from tournaments.models import Tournament
        tournaments_data = []  ## [id, date, name, location, place]
        tournament_ids = self.tournaments
        if tournament_ids:
            tournaments = Tournament.get_tournaments_by_uuid_list(tournament_ids)
            for tournament in tournaments:
                tournaments_data.append([tournament.tournament_id, tournament.datetime, tournament.name, tournament.center_short_location, 0])
        return tournaments_data

    ## FRIENDS ##
    @property
    def friends(self):
        return quickle.loads(self.data_friends)
    @friends.setter
    def friends(self, data):
        if data:
            self.data_friends = quickle.dumps(data)
    def is_friends(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            friends_list = self.data_friends
            if user_id in friends_list:
                return True
        return False
    def add_friend(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            friends_list = self.friends
            if user_id not in friends_list:
                friends_list.append(user_id)
                self.friends = friends_list
    def remove_friend(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            friends_list = self.friends
            if user_id in friends_list:
                friends_list.remove(user_id)
                self.friends = friends_list

    ## BLOCKED USERS ##
    @property
    def blocked(self):
        return quickle.loads(self.data_blocked)
    @blocked.setter
    def blocked(self, data):
        if data:
            self.data_blocked = quickle.dumps(data)
    def is_blocked(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            blocked_list = self.data_friends
            if user_id in blocked_list:
                return True
        return False
    def block_user(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            blocked_list = self.blocked
            if user_id not in blocked_list:
                blocked_list.append(user_id)
                self.blocked = blocked_list
    def unblock_user(self, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            blocked_list = self.blocked
            if user_id in blocked_list:
                blocked_list.remove(user_id)
                self.blocked = blocked_list

    ## LOCATION ##
    @property
    def short_location(self):
        if self.location_city and self.location_state:
            return self.location_city + ', ' + self.location_state
        return 'Location Unknown'

    ## SINGLE ACCOUNT VIEW DATA##
    def data_single_account_view(self):
        return None

    ## BOWLER OF MONTH ##
    @classproperty
    def get_bowler_of_month(cls):
        return cls.objects.filter(is_bowler_of_month=True).first()
    @classproperty
    def set_bowler_of_month(cls, uuid):
        user = cls.get_user_by_uuid(uuid)
        if user:
            cls.objects.filter(is_bowler_of_month=True).update(is_bowler_of_month=False)
            user.is_bowler_of_month = True
            user.save()
    @classmethod
    def data_bowler_of_month(cls):
        data = {}
        user = cls.objects.filter(is_bowler_of_month=True).first()
        if user:
            if user.statistics:
                statistics = user.statistics
                if statistics:
                    data = {'user_id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'picture': user.full_picture_url,
                            'location': user.short_location,
                            'badge': user.rank_badge_html,

                            'avg_score': statistics.avg_score,
                            'wins': statistics.wins,
                            'attended': statistics.attended,
                            'top_five': statistics.top_five_tournaments,
                            'year_avg_score': statistics.year_avg_score,
                            'year_wins': statistics.year_wins,
                            'year_attended': statistics.year_attended,
                            'year_top_five': statistics.year_top_five_tournaments}
        return data




    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
















class Shorten(models.Model):
    code = models.CharField(max_length=5)
    url = models.CharField(max_length=300)