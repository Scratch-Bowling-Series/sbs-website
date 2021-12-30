import datetime
import json
import os
import uuid
import random
from urllib.request import urlopen

import quickle
from PIL import Image
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.functional import classproperty
from django.utils.http import urlsafe_base64_encode
from exponent_server_sdk import PushMessage

from ScratchBowling import settings
from ScratchBowling.models import WebData
from ScratchBowling.sbs_utils import is_valid_uuid, load_quickle_array, dump_quickle_array, del_uuid_from_array, \
    add_uuid_to_array, is_uuid_in_array
from accounts.notify import send_push_message
from accounts.scraping.soup_parser import update_user_with_soup
from accounts.tokens import account_activation_token
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
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(default='profile-pictures/default.jpg', upload_to='profile-pictures/')

    street = models.CharField(blank=True, null=True, max_length=150)
    city = models.CharField(blank=True, null=True, max_length=150)
    state = models.CharField(blank=True, null=True, max_length=150)
    zip = models.IntegerField(default=0, null=False, blank=True)
    country = models.CharField(blank=True, null=True, max_length=150)

    handed = models.SmallIntegerField(default=0)
    medals = models.JSONField(blank=True, null=True)
    date_joined = models.DateField(default=datetime.date.today, editable=False)

    balance = models.IntegerField(default=0)
    pending_balance = models.IntegerField(default=0)

    data_tournaments = models.BinaryField(blank=True, null=True)
    data_friends = models.BinaryField(blank=True, null=True)
    data_friend_requests_outbound = models.BinaryField(blank=True, null=True)
    data_friend_requests_inbound = models.BinaryField(blank=True, null=True)
    data_blocked = models.BinaryField(blank=True, null=True)
    data_push_tokens = models.BinaryField(blank=True, null=True)


    is_bowler_of_month = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    finish_profile = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    ask_for_claim = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

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


    @property
    def full_name(self):
        first = str(self.first_name)
        last = str(self.last_name)
        return first + ' ' + last


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

    ## EMAIL VERIFICATION ##
    def send_verification_email(self):
        subject = 'Please verify your account.'
        from_email = 'christianjstarr@icloud.com'

        uuid = str(self.id)
        token = account_activation_token.make_token(self)

        raw_message = render_to_string('acc_active_email_plain.html', {
            'uid': uuid,
            'token': token,
        })
        html_message = render_to_string('acc_active_email.html', {
            'uid': uuid,
            'token': token,
        })

        send_mail(
            subject,
            raw_message,
            from_email,
            [self.email],
            fail_silently=True,
            html_message=html_message
        )
    def verify_email(self, token):
        if account_activation_token.check_token(self, token):
            self.is_verified = True
            return True
        return False


    ## NOTIFICATIONS
    @property  ## returns array of notifications
    def notifications(self):
        return Notification.get_notifications(self.id)
    @property
    def has_notifications(self):
        if self and self.id:
            return Notification.has_notification(self.id)
        return False


    ## NOTIFICATIONS
    @property  ## returns array of notifications
    def push_tokens(self):
        return load_quickle_array(self.data_push_tokens)
    @push_tokens.setter
    def push_tokens(self, data):
        self.data_push_tokens = dump_quickle_array(data)
    def add_push_token(self, uuid):
        array = add_uuid_to_array(uuid, self.push_tokens)
        if array != None:
            print(array)
            self.push_tokens = array
            return True
        return False
    def remove_push_token(self, uuid):
        array = del_uuid_from_array(uuid, self.push_tokens)
        if array != None:
            self.push_tokens = array
            return True
        return False


    ## PICTURE ##
    def setPictureFromRest(self, pictureData):
        if pictureData:
            img = Image.open(pictureData)
            img = img.convert('RGB')
            randomKey = random.randrange(0,999)
            path = 'profile-pictures/' + str(self.id) + '-' + str(randomKey) + '.jpg'
            img.save(os.path.join(settings.MEDIA_ROOT, path), format="jpeg")
            self.picture = path
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




    # <editor-fold desc="FRIENDS">
    ## FRIENDS ##
    @property ## returns friends list ids
    def friends(self):
        return load_quickle_array(self.data_friends)
    @friends.setter
    def friends(self, data):
        self.data_friends = dump_quickle_array(data)
    def is_friends(self, uuid):
        friends = self.friends
        friend_id = str(uuid)
        if friends and friend_id in friends:
            return True
        return False
    def add_friend(self, uuid):
        print('adding friend ' + str(uuid))
        friends = self.friends
        friend_id = str(uuid)
        if friend_id not in friends:
            friends.append(friend_id)
            self.friends = friends
            print('friends added ' + str(friends))
            return True
        return False
    def del_friend(self, uuid):
        friends = self.friends
        friend_id = str(uuid)
        if friends and friend_id in friends:
            friends.remove(friend_id)
            self.friends = friends
            return True
        return False

    ## FRIEND REQUESTS -- OUTBOUND GETS/SETS ##
    @property  ## returns outbound friend request list ids
    def friend_requests_outbound(self):
        return load_quickle_array(self.data_friend_requests_outbound)
    @friend_requests_outbound.setter
    def friend_requests_outbound(self, data):
        self.data_friend_requests_outbound = dump_quickle_array(data)

    ## FRIEND REQUESTS -- INBOUND GETS/SETS ##
    @property  ## returns inbound friend request list ids
    def friend_requests_inbound(self):
        return load_quickle_array(self.data_friend_requests_inbound)
    @friend_requests_inbound.setter
    def friend_requests_inbound(self, data):
        self.data_friend_requests_inbound = dump_quickle_array(data)

    ## FRIEND REQUESTS -- INBOUND/OUTBOUND LOGIC ##
    def add_friend_request_to_data(self, friend):
        outbound = self.friend_requests_outbound
        inbound = friend.friend_requests_inbound
        friend_id = str(friend.id)
        user_id = str(self.id)
        if user_id not in inbound:
            inbound.append(user_id)
            friend.friend_requests_inbound = inbound
        if friend_id not in outbound:
            outbound.append(friend_id)
            self.friend_requests_outbound = outbound
        else:
            return False
        return True


    def remove_friend_request_data(self, friend):
        outbound = friend.friend_requests_outbound
        inbound = self.friend_requests_inbound
        friend_id = str(friend.id)
        user_id = str(self.id)
        if inbound and friend_id in inbound:
            inbound.remove(friend_id)
            self.friend_requests_inbound = inbound
        if outbound and user_id in outbound:
            outbound.remove(user_id)
            friend.friend_requests_outbound = outbound
            return True
        return False

    ## FRIEND REQUESTS -- PRIMARY LOGIC ##
    @classmethod
    def send_friend_request(cls, user_id, friend_id):
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend:
            if user.add_friend_request_to_data(friend):
                Notification.notify_friend_request(user, friend)
                user.save()
                friend.save()
                return True
            elif user.remove_friend_request_data(friend):
                friend.add_friend(user_id)
                user.add_friend(friend_id)
                Notification.notify_friend_accept(user, friend)
                user.save()
                friend.save()
                return True
        return False

    @classmethod
    def accept_friend_request(cls, user_id, friend_id, notification_id=None):
        print(notification_id)
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend:
            if user.remove_friend_request_data(friend):
                friend.add_friend(user_id)
                user.add_friend(friend_id)
                Notification.remove_notification(user_id)
                Notification.notify_friend_accept(user, friend)
                friend.save()
                user.save()

                if notification_id:
                    Notification.remove_notification(notification_id)
                return True
        return False

    @classmethod
    def cancel_friend_request(cls, user_id, friend_id, notification_id=None):
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend:
            if user.remove_friend_request_data(friend):
                friend.save()
                user.save()
                if notification_id:
                    Notification.remove_notification(notification_id)
                return True
        if notification_id:
            Notification.remove_notification(notification_id)
        return False


    @classmethod
    def remove_friend(cls, user_id, friend_id):
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend and user.is_friends(friend_id):
            user.del_friend(friend_id)
            friend.del_friend(user_id)
            user.save()
            friend.save()
            return True
        return False

    ## SEARCH FOR FRIENDS
    @classmethod
    def search_friends_extra(cls, user_id, search_args):
        user = cls.get_user_by_uuid(user_id)
        output = []
        if user:
            requests_inbound = user.friend_requests_inbound
            requests_outbound = user.friend_requests_outbound
            friends = user.friends

            qs = User.objects.all()
            for search_arg in search_args.split():
                qs = qs.filter(Q(first_name__icontains=search_arg) |
                                Q(last_name__icontains=search_arg) |
                                Q(city__icontains=search_arg) |
                                Q(state__icontains=search_arg))

            for user in qs:
                user_id = str(user.id)
                status = 'stranger'
                if user_id in requests_inbound:
                    status = 'request_inbound'
                elif user_id in requests_outbound:
                    status = 'request_outbound'
                elif user_id in friends:
                    status = 'friends'
                output.append(user.convert_to_friend_extra(status))
        return output

    ## FRIENDS -- API SERIALIZING  ##
    @property
    def friends_objects(self):
        friends = self.friends
        users = []
        for friend_id in friends:
            user = User.get_user_by_uuid(friend_id)
            if user:
                users.append(user)
        return users

    @property
    def friends_outbound_objects(self):
        friends = self.friend_requests_outbound
        users = []
        for friend_id in friends:
            user = User.get_user_by_uuid(friend_id)
            if user:
                users.append(user)
        return users
    @property
    def friends_inbound_objects(self):
        friends = self.friend_requests_inbound
        users = []
        for friend_id in friends:
            user = User.get_user_by_uuid(friend_id)
            if user:
                users.append(user)
        return users







    @property ## returns friends list with some extra info (for rest)
    def friends_extra(self):
        friends = self.friends
        users = []
        for friend in friends:
            user = User.get_user_by_uuid(friend)
            if user:
                users.append(user.convert_to_friend_extra())

        return users
    @property  ## returns inbound friend request list ids
    def friend_requests_inbound_extra(self):
        output = []
        friends = self.friend_requests_inbound
        if friends:
            for friend in friends:
                user = User.get_user_by_uuid(friend)
                if user:
                    output.append(user.convert_to_friend_extra())
        return []
    @property  ## returns outbound friend request list ids
    def friend_requests_outbound_extra(self):
        output = []
        friends = self.friend_requests_outbound
        if friends:
            for friend in friends:
                user = User.get_user_by_uuid(friend)
                if user:
                    output.append(user.convert_to_friend_extra())
        return []
    def convert_to_friend_extra(self, status=None):
        picture = ''
        if self.picture:
            picture = self.picture.url

        if status:
            return {'id': self.id, 'first_name': self.first_name,
                    'last_name': self.last_name, 'picture': picture, 'status': status}
        else:
            return {'id': self.id, 'first_name': self.first_name,
                    'last_name': self.last_name, 'picture': picture}

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
    # </editor-fold>




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







class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipient = models.UUIDField(editable=True, unique=False, null=True, blank=True)
    sender = models.UUIDField(editable=True, unique=False, null=True, blank=True)

    datetime = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=5)
    body = models.CharField(max_length=300)

    type = models.CharField(max_length=20)

    read = models.BooleanField(default=False)

    data = models.TextField(default='')



    @classmethod
    def get_notifications(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            return cls.objects.filter(recipient=uuid).order_by('-datetime')

    @classmethod
    def has_notification(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            count = cls.objects.filter(recipient=uuid, read=False).count()
            return False if count == 0 else True
        return False



    @classmethod
    def notify_friend_request(cls, user, friend):
        body = user.full_name + ' sent you a friend request.'
        data = {'notification_id': None, 'picture': user.picture.url}
        cls.send_notification_p2p(user.id, friend.id, 'SBS Bowler', body, 'friend_request', data)

    @classmethod
    def notify_friend_accept(cls, user, friend):
        body = user.full_name + ' accepted your friend request.'
        data = {'picture': user.picture.url}
        cls.send_notification_p2p(user.id, friend.id, 'SBS Bowler', body, 'friend_accept', data)


    @classmethod
    def send_notification_p2p(cls, sender_id, recipient_id, title, body, type, data):
        notification = cls(sender=sender_id, recipient=recipient_id,title=title, body=body, type=type)
        if data:
            notification.data = json.dumps(data)
        notification.save()
        sendNotificationToExpo(notification)

    @classmethod
    def remove_notification(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            cls.objects.filter(id=uuid).delete()
            return True
        return False

    @classmethod
    def clear_notifications(cls, user_id):
        user_id = is_valid_uuid(user_id)
        if user_id:
            cls.objects.filter(recipient=user_id).delete()


    def to_push_message(self, token):
        return PushMessage(title=self.title, body=self.body, data=self.data, to=token)



def sendNotificationToExpo(notification):
    recipient = User.get_user_by_uuid(notification.recipient)
    if recipient:
        tokens = recipient.push_tokens
        for token in tokens:
            send_push_message(notification.to_push_message(token))





class Shorten(models.Model):
    code = models.CharField(max_length=5)
    url = models.CharField(max_length=300)