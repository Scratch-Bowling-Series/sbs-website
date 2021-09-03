import datetime
import uuid

from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_id=uuid.uuid4()
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
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True, null=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_joined = models.DateField(default=datetime.date.today, editable=False)
    finish_profile = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(default='profile-pictures/default.jpg', upload_to='profile-pictures/')
    location_street = models.CharField(blank=True, null=True, max_length=150)
    location_city = models.CharField(blank=True, null=True, max_length=150)
    location_state = models.CharField(blank=True, null=True, max_length=150)
    location_zip = models.IntegerField(default=0, null=False, blank=True)
    right_handed = models.BooleanField(default=False)
    left_handed = models.BooleanField(default=False)
    medals = models.JSONField(blank=True, null=True)
    tournaments = models.JSONField(blank=True, null=True)
    statistics = models.JSONField(blank=True, null=True)
    friends = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    is_online = models.BooleanField(default=False)
    unclaimed = models.BooleanField(default=False)
    objects = UserManager()
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

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