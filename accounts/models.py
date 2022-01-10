import datetime
import json
import os
import uuid
import random
from urllib.request import urlopen
from PIL import Image
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.db import models, transaction
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.functional import classproperty
from phonenumber_field.modelfields import PhoneNumberField
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError, PushServerError
)
from requests.exceptions import ConnectionError, HTTPError
from ScratchBowling import settings
from ScratchBowling.models import WebData
from ScratchBowling.sbs_utils import is_valid_uuid
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

    ## PROFILE
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(default='profile-pictures/default.jpg', upload_to='profile-pictures/')

    ## CONTACT
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, null=True)
    phone = PhoneNumberField(null=True, unique=True)

    ## GEO
    street = models.CharField(blank=True, null=True, max_length=150)
    city = models.CharField(blank=True, null=True, max_length=150)
    state = models.CharField(blank=True, null=True, max_length=150)
    zip = models.IntegerField(default=0, null=False, blank=True)
    country = models.CharField(blank=True, null=True, max_length=150)

    ## PREFERENCES
    class Chirality(models.IntegerChoices):
        UNKNOWN = 0,
        LEFT = 1,
        RIGHT = 2,
        BOTH = 3,

    chirality = models.IntegerField(choices=Chirality.choices, default=Chirality.UNKNOWN)
    medals = models.JSONField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now, editable=False)

    ## BANKING
    balance = models.IntegerField(default=0)
    pending_balance = models.IntegerField(default=0)

    ## Tournaments
    # m2o - tournament_datas
    # m2o - teams
    # m2o - team_invites_sent
    # m2o - team_invites_received

    ## Scoreboard/Ranking
    # o2o - statistics

    ## FRIENDS
    # m2o - friend_requests_sent
    # m2o - friend_requests_received

    ## Notifications
    # m2o - notifications
    # m2o - push_tokens

    ## Transaction
    # m2o - transactions_received
    # m2o - transactions_received







    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    blocked_users = models.ManyToManyField('self', blank=True, symmetrical=True)
    is_bowler_of_month = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    finish_profile = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    ask_for_claim = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_drawer_manager = models.BooleanField(default=False)




    modified_account = models.BooleanField(default=True)






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

    @property
    def top_notify(self):
        if not self.is_verified:
            return 'verify_email'
        elif not self.modified_account:
            return 'finish_account'
        elif self.ask_for_claim:
            return 'claim_data'

    ## TRANSACTIONS
    @property
    def recent_transactions(self):
        return self.transactions.all().order_by('-datetime')[:20]


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
    @property
    def has_notifications(self):
        return True if self.notifications.all().count() > 0 else False
    def add_push_token(self, token):
        if PushToken.create(self, token):
            return True
        return False
    def remove_push_tokens(self, tokens):
        for token in tokens:
            self.push_tokens.filter(token=token).delete()


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
    def rank_badge(self):
        statistics = None
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
        statistics = None
        if statistics:
            return statistics.rank
        return 0
    @property
    def rank_ordinal(self):
        statistics = None
        if statistics:
            return statistics.rank_ordinal
        return 0


    ## FRIENDS ##
    def is_friends(self, user_id):
        if self.friends.filter(id=user_id).first():
            return True
        return False
    @classmethod
    def send_friend_request(cls, user_id, friend_id):
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend and not user.is_friends(friend.id):
            return FriendRequest.send(user, friend)
        return False
    @classmethod
    def accept_friend_request(cls, user_id, friend_id):

        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend and not user.is_friends(friend.id):
            return FriendRequest.accept(user, friend)
        return False
    @classmethod
    def cancel_friend_request(cls, user_id, friend_id):
        user = cls.get_user_by_uuid(user_id)
        friend = cls.get_user_by_uuid(friend_id)
        if user and friend and not user.is_friends(friend.id):
            return FriendRequest.cancel(user, friend)
        return False
    @classmethod
    def remove_friend(cls, user_id, friend_id):
        user = cls.get_user_by_uuid(user_id)
        if user:
            friend_id = is_valid_uuid(friend_id)
            if user and friend_id:
                user.friends.remove(friend_id)
                return True
        return False
    @classmethod
    def search_friends_extra(cls, user_id, search_args):
        user = cls.get_user_by_uuid(user_id)
        users = []
        statuses = []

        if user:
            qs = User.objects.all()
            for search_arg in search_args.split():
                qs = qs.filter(Q(first_name__icontains=search_arg) |
                                Q(last_name__icontains=search_arg) |
                                Q(city__icontains=search_arg) |
                                Q(state__icontains=search_arg))

            print(len(qs))
            users = qs[:100]
            requests_sent = user.friend_requests_sent.all()
            requests_received = user.friend_requests_received.all()
            friends = user.friends.all()
            for query_user in users:
                status = 'stranger'
                if query_user.id == user.id:
                    status = 'self'
                else:
                    for friend in friends:
                        if friend.id == query_user.id:
                            status = 'friends'
                            break
                    for friend in requests_sent:
                        if friend.id == query_user.id:
                            status = 'request_inbound'
                            break
                    for friend in requests_received:
                        if friend.id == query_user.id:
                            status = 'request_outbound'
                            break
                statuses.append(status)
        return users,statuses


    ## LOCATION ##
    @property
    def short_location(self):
        if self.city and self.state:
            return self.city + ', ' + self.state
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

    @classmethod
    def active_user_count(cls):
        return cls.objects.filter(is_active=True).count()



class PushToken(models.Model):
    token = models.CharField(max_length=200, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_tokens')

    @classmethod
    def create(cls, user, token):
        cls.objects.filter(token=token).delete()
        push_token = cls(token=token, user=user)
        push_token.save()
        return push_token


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    recipients = models.ManyToManyField(User, related_name='notifications')
    persistent = models.BooleanField(default=False) ## cant be deleted unless false

    class NotificationType(models.IntegerChoices):
        BASIC = 0,
        FRIEND_INVITE = 1,
        TEAM_INVITE = 2,
    type = models.IntegerField(default=NotificationType.BASIC, choices=NotificationType.choices)

    class NotificationPriority(models.IntegerChoices):
        DEFAULT = 0,
        URGENT = 1,
        SCHEDULED = 4,
    priority = models.SmallIntegerField(default=0)

    datetime = models.DateTimeField(default=timezone.now, editable=True)
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=300)
    read = models.BooleanField(default=False)
    data = models.TextField(default='')

    sent = models.BooleanField(default=False)
    push_receipt_id = models.CharField(max_length=200, null=True)
    friend_invite = models.ForeignKey('accounts.FriendRequest', on_delete=models.CASCADE, blank=True, null=True)
    team_invite = models.ForeignKey('tournaments.TeamInvite', on_delete=models.CASCADE, blank=True, null=True)
    ##team_invite = models.CharField(default='', max_length=100)
    @classmethod
    def create(cls, type, title, body, data, recipients, priority, persistent):
        data = json.dumps(data)
        notification = cls(type=type, title=title, body=body, data=data, priority=priority, persistent=persistent)
        notification.save()
        notification.recipients.set(recipients)
        notification.save()
        return notification

    @classmethod
    def perform_sends(cls):
        cls.send_bulk_notifications(cls.objects.filter(priority=cls.NotificationPriority.URGENT, sent=False))

        cls.send_bulk_notifications(cls.objects.filter(priority=cls.NotificationPriority.DEFAULT, sent=False))

        cls.send_bulk_notifications(cls.objects.filter(priority=cls.NotificationPriority.SCHEDULED, sent=False, datetime__gte=timezone.now()))
    @classmethod
    def send_bulk_notifications(cls, notifications):
        batch_size = 50
        batch = 0
        while True:
            offset = batch * batch_size
            batch += 1
            notifications_ = notifications[offset:offset+batch_size]
            if notifications_:
                cls.bulk_send_task(notifications_)
            else:
                break
    @classmethod
    def bulk_send_task(cls, notifications):
        push_messages = []
        for notification in notifications:
            push_messages += notification.to_push_message()
        responses = []
        if len(push_messages) > 0:
            try:
                responses = PushClient().publish_multiple(push_messages)
            except PushServerError as exc:
                print(exc.errors)
            except (ConnectionError, HTTPError):
                print('Notification Send Task - Connection Error')

            if responses:
                index = 0
                for notification in notifications:
                    response = responses[index]
                    index += 1
                    notification.set_push_tickets(response)
    def set_push_tickets(self, response):
        try:
            response.validate_response()
            self.push_receipt_id = response.id
            self.sent = True
            self.save()
        except DeviceNotRegisteredError:
            self.push_receipt_id = response.id
            self.sent = True
            self.save()
        except PushTicketError as exc:
            print('Notification Send Task - Unknown Error')

    @classmethod
    def remove_notification(cls, user, notification_id):
        if user.notifications.filter(id=notification_id, persistent=True).delete():
            return True
        return False
    @classmethod
    def clear_notifications(cls, user):
        if user.notifications.filter(persistent=False).delete():
            return True
        return False

    def to_push_message(self):
        push_messages = []
        recipients = self.recipients.all()
        for recipient in recipients:
            tokens = list(recipient.push_tokens.all().values_list('token', flat=True))
            if tokens:
                for token in tokens:
                    push_messages.append(PushMessage(title=self.title, body=self.body, data=self.data, to=token))

        return push_messages


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    datetime = models.DateField(default=timezone.now, editable=False)


    @classmethod
    def create(cls, user, friend):
        friend_request = cls(sender=user, receiver=friend)
        friend_request.save()
        return friend_request

    @classmethod
    def send(cls, user, friend):
        invite = friend.friend_requests_sent.filter(receiver=user.id).first()
        if not invite and user.friend_requests_sent.filter(receiver=friend.id).count() == 0:
            request = cls.create(user, friend)
            if request:
                title = 'SBS Bowler'
                body = user.full_name + ' sent you a friend request.'
                data = {'invite_id': str(request.id), 'user_id': str(user.id), 'picture': user.picture.url}
                notification = Notification.create(Notification.NotificationType.FRIEND_INVITE, title, body, data, [friend.id],
                                    Notification.NotificationPriority.DEFAULT, False)
                notification.friend_invite = request
                notification.save()
                return True
        return False

    @classmethod
    def accept(cls, user, friend):

        request = friend.friend_requests_sent.filter(receiver=user).first()
        if request:
            user.friends.add(friend)
            title = 'SBS Bowler'
            body = user.full_name + ' accepted your friend request.'
            data = {'user_id': str(user.id), 'picture': user.picture.url}
            Notification.create(Notification.NotificationType.BASIC, title, body, data, [friend.id],
                                Notification.NotificationPriority.DEFAULT, True)
            request.delete()
            return True
        return False

    @classmethod
    def cancel(cls, user, friend):
        if user.friend_requests_sent.filter(receiver=friend).delete() or friend.friend_requests_sent.filter(receiver=user).delete():
            return True
        return False






class Shorten(models.Model):
    code = models.CharField(max_length=5)
    url = models.CharField(max_length=300)