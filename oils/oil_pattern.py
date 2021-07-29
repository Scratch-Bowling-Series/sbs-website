import json

from ScratchBowling.sbs_utils import is_valid_uuid
from oils.models import Oil_Pattern
from oils.oil_pattern_scraper import update_library


def get_oil_pattern_data(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        pattern = Oil_Pattern.objects.filter(pattern_id=uuid).first()
        return pattern
    return None

def get_oil_display_data(display_id):
    data = Oil_Pattern.objects.filter(pattern_db_id=display_id).first()
    data = data.pattern_cache
    if data is not None:
        return json.loads(data)
    return None



def update_oil_pattern_library(full_update=False):
    update_library(full_update)
