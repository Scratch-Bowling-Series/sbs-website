import quickle
from django.db import models
from ScratchBowling.sbs_utils import is_valid_uuid, make_ordinal


class Statistics(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True,related_name='statistics')
    last_calculated = models.DateTimeField()

    rank = models.IntegerField(default=0)
    rank_points = models.IntegerField(default=0)

    wins = models.IntegerField(default=0)
    attended = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    year_wins = models.IntegerField(default=0)
    year_attended = models.IntegerField(default=0)
    year_total_games = models.IntegerField(default=0)
    year_total_score = models.IntegerField(default=0)

    data_tournaments = models.BinaryField()
    data_top_five_tournaments = models.BinaryField()
    data_year_top_five_tournaments = models.BinaryField()


    @classmethod
    def get_user_statistics(cls, uuid):
        uuid = is_valid_uuid(uuid)
        if uuid:
            return cls.objects.filter(user_id=uuid).first()
        return None

    @classmethod
    def create(cls, user):
        return cls(user=user)

    @property
    def rank_ordinal(self):
        return make_ordinal(self.rank)

    @property
    def rank_badge(self):
        total_users = 10000
        diamond = total_users / 10
        gold = total_users / 5
        silver = total_users / 2.5

        rank = self.rank
        if rank > 0 and rank <= silver:
            if rank <= diamond:
                return 1
            elif rank <= gold:
                return 2
            return 3
        return 4


    def calculate(self):
        #calculate the statistics
        self.save()

    def to_dict(self):
        return {'user_id': self.user_id,
                'last_calculated': self.last_calculated,
                'rank': self.rank,
                'rank_points': self.rank_points,
                'wins': self.wins,
                'attended': self.attended,
                'total_games': self.total_games,
                'avg_score': self.avg_score,
                'year_wins': self.year_wins,
                'year_attended': self.year_attended,
                'year_total_games': self.year_total_games,
                'year_avg_score': self.year_avg_score}

    @property
    def tournaments(self):
        if self.data_tournaments:
            return quickle.loads(self.data_tournaments)
        return []

    @property
    def top_five_tournaments(self):
        if self.data_top_five_tournaments:
            return quickle.loads(self.data_top_five_tournaments)
    @top_five_tournaments.setter
    def top_five_tournaments(self, data):
        if data:
            self.data_top_five_tournaments = quickle.dumps(data)

    @property
    def year_top_five_tournaments(self):
        if self.data_year_top_five_tournaments:
            return quickle.loads(self.data_year_top_five_tournaments)

    @year_top_five_tournaments.setter
    def year_top_five_tournaments(self, data):
        if data:
            self.data_year_top_five_tournaments = quickle.dumps(data)


    @property
    def avg_score(self):
        if self.total_games != 0:
            return round(self.total_score / self.total_games, 2)
        return 0

    @property
    def year_avg_score(self):
        if self.year_total_games != 0:
            return round(self.year_total_score / self.year_total_games, 2)
        return 0
















