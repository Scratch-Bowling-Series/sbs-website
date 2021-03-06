# Generated by Django 3.1.6 on 2022-01-14 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(default='profile-pictures/default.jpg', upload_to='profile-pictures/')),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('zip', models.IntegerField(blank=True, default=0)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('chirality', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Left'), (2, 'Right'), (3, 'Both')], default=0)),
                ('medals', models.JSONField(blank=True, null=True)),
                ('date_joined', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('balance', models.IntegerField(default=0)),
                ('pending_balance', models.IntegerField(default=0)),
                ('is_bowler_of_month', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('finish_profile', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('ask_for_claim', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_drawer_manager', models.BooleanField(default=False)),
                ('modified_account', models.BooleanField(default=True)),
                ('scraped', models.BooleanField(default=False)),
                ('unclaimed', models.BooleanField(default=False)),
                ('soup_url', models.TextField(default='')),
                ('soup', models.TextField(default='')),
                ('blocked_users', models.ManyToManyField(blank=True, related_name='_user_blocked_users_+', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, related_name='_user_friends_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('datetime', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shorten',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='PushToken',
            fields=[
                ('token', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='push_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('persistent', models.BooleanField(default=False)),
                ('type', models.IntegerField(choices=[(0, 'Basic'), (1, 'Friend Invite'), (2, 'Team Invite')], default=0)),
                ('priority', models.SmallIntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=120)),
                ('body', models.CharField(max_length=300)),
                ('read', models.BooleanField(default=False)),
                ('data', models.TextField(default='')),
                ('sent', models.BooleanField(default=False)),
                ('push_receipt_id', models.CharField(max_length=200, null=True)),
                ('team_invite', models.CharField(default='', max_length=100)),
                ('friend_invite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.friendrequest')),
                ('recipients', models.ManyToManyField(related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
