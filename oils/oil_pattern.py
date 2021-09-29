import quickle
from ScratchBowling.sbs_utils import is_valid_uuid
from oils.models import Oil_Pattern



def get_oil_pattern_uuid(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid != None:
        return Oil_Pattern.objects.filter(pattern_id=uuid).first()
    return None

def get_oil_pattern_db_id(db_id):
    return Oil_Pattern.objects.filter(pattern_db_id=db_id).first()


def get_oil_pattern_data(uuid):
    oil_pattern = get_oil_pattern_uuid(uuid)
    if oil_pattern != None:
        data = Oil_Pattern.objects.filter(pattern_id=uuid).first()
        if data != None:
            data = data.pattern_cache
            if data != None:
                return quickle.loads(data)
    return None

def get_oil_display_data_db_id(db_id):
    oil_pattern = get_oil_pattern_db_id(db_id)
    if oil_pattern != None:
        data = oil_pattern.pattern_cache
        if data != None:
            return quickle.loads(data)
    return None

def get_oil_display_data_uuid(uuid):
    oil_pattern = get_oil_pattern_uuid(uuid)
    if oil_pattern != None:
        data = oil_pattern.pattern_cache
        if data != None:
            return quickle.loads(data)
    return get_oil_display_data_db_id(824)

