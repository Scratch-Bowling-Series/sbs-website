import uuid
import quickle
from django.db import models

# Create your models here.
from ScratchBowling.sbs_utils import is_valid_uuid


class Oil_Pattern(models.Model):
    pattern_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    pattern_name = models.TextField(default=0)
    pattern_cache = models.BinaryField(blank=True, null=True)
    pattern_db_id = models.IntegerField(default=0)
    pattern_length = models.IntegerField(default=0)
    pattern_volume = models.FloatField(default=0)
    pattern_forward = models.FloatField(default=0)
    pattern_backward = models.FloatField(default=0)
    pattern_ratio = models.TextField(default='')

    @classmethod
    def create(cls, pattern_db_id):
        return cls(pattern_db_id=pattern_db_id)

    @classmethod
    def get_pattern_by_id(cls, pattern_id):
        pattern_id = is_valid_uuid(pattern_id)
        if not pattern_id: return None
        return cls.objects.filter(pattern_id=pattern_id).first()

    @classmethod
    def get_pattern_by_db_id(cls, pattern_db_id):
        return cls.objects.filter(pattern_db_id=pattern_db_id).first()

    @classmethod
    def get_all_patterns_converted(cls, amount, offset):
        patterns = cls.objects.all()[offset:offset+amount]
        output = []
        for oil_pattern in patterns:
            output.append(oil_pattern.convert_to_list())
        return output

    @classmethod
    def get_oil_pattern_converted_uuid(cls, uuid):
        oil_pattern = cls.get_pattern_by_id(uuid)
        if oil_pattern:
            return oil_pattern.convert_to_list()
        return None

    def convert_to_list(self):
        return [self.pattern_id,
        self.pattern_name,
        self.load_pattern_cache(),
        self.pattern_db_id,
        self.pattern_length,
        self.pattern_volume,
        self.pattern_forward,
        self.pattern_backward,
        self.pattern_ratio]

    def load_pattern_cache(self):
        if self != None and self.pattern_cache != None:
            return quickle.loads(self.pattern_cache)
        return None

    def set_pattern_cache(self, data, dont_save=False):
        if self != None and data != None:
            self.pattern_cache = quickle.dumps(data)
            if dont_save:
                return self
            self.save()
            return True
        return False


