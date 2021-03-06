# Generated by Django 3.1.6 on 2022-01-14 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oils', '0001_initial'),
        ('centers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('format_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField(default='')),
                ('is_qualifiers', models.BooleanField()),
                ('qualifier_games', models.SmallIntegerField(default=0)),
                ('cashers', models.SmallIntegerField(default=0)),
                ('is_carryover', models.BooleanField(default=False)),
                ('is_bonus_pins', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('sponsor_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('sponsor_name', models.CharField(blank=True, max_length=60, null=True)),
                ('sponsor_display_name', models.CharField(blank=True, max_length=60, null=True)),
                ('sponsor_balance', models.IntegerField(blank=True, default=0)),
                ('sponsor_image', models.ImageField(default='sponsor-pictures/default.png', upload_to='sponsor-pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('scoring_data_id', models.UUIDField(blank=True, null=True)),
                ('format_id', models.UUIDField(blank=True, null=True, unique=True)),
                ('vod_id', models.UUIDField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('datetime', models.DateField(default=django.utils.timezone.now)),
                ('picture', models.ImageField(default='tournament-pictures/default.jpg', upload_to='tournament-pictures/')),
                ('entry_fee', models.FloatField(blank=True, null=True)),
                ('total_games', models.IntegerField(blank=True, default=0)),
                ('qualifiers', models.JSONField(blank=True, null=True)),
                ('matchplay', models.JSONField(blank=True, null=True)),
                ('sponsor', models.UUIDField(blank=True, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('live', models.BooleanField(default=False)),
                ('team_size', models.SmallIntegerField(default=1)),
                ('stream_available', models.BooleanField(default=False)),
                ('tournament_data', models.BinaryField(blank=True, null=True)),
                ('placement_data', models.BinaryField(blank=True, null=True)),
                ('data_scoring', models.BinaryField(blank=True, null=True)),
                ('spots_reserved', models.IntegerField(blank=True, default=0)),
                ('live_status_header', models.TextField(blank=True, null=True)),
                ('live_status_leader', models.UUIDField(blank=True, null=True)),
                ('live_status_leader_score', models.FloatField(blank=True, default=0)),
                ('scraped', models.BooleanField(default=False)),
                ('soup_url', models.TextField(default='')),
                ('soup', models.TextField(default='')),
                ('center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournaments', to='centers.center')),
                ('oil_pattern', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournaments', to='oils.oil_pattern')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('checked_in', models.BooleanField(default=False)),
                ('start_lane', models.SmallIntegerField(default=0)),
                ('looking_for_team', models.BooleanField(default=False)),
                ('is_winner', models.BooleanField(default=False)),
                ('place', models.IntegerField(default=0)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournament_datas', to='tournaments.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_datas', to='tournaments.tournament')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_datas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamInvite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('datetime', models.DateField(default=django.utils.timezone.now, editable=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invites_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invites_sent', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invites', to='tournaments.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='tournaments.tournament'),
        ),
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('game_number', models.SmallIntegerField(default=0)),
                ('match_number', models.SmallIntegerField(default=0)),
                ('lane', models.SmallIntegerField(default=0)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('data_raw_scores', models.BinaryField()),
                ('data_scores', models.BinaryField()),
                ('bonus', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('tournament_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_datas', to='tournaments.tournamentdata')),
            ],
        ),
    ]
